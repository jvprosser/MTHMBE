from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from MTHMBE import app
from models import RMStats,Impala_Stats
import core
#import time
from time import mktime, strftime,localtime
from pytz import timezone

#import datetime
from datetime import timedelta,datetime,time

import collections
import urllib2
import base64
import json
import kerberos as k
import urllib2_kerberos as ul2k


import logging

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.DEBUG)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)


db = SQLAlchemy()

app.logger.debug("views.py")

def unix_timestamp_secs():
  dt = datetime.now()
  epoch = datetime.utcfromtimestamp(0)
  return int((dt - epoch).total_seconds() )
#  return int((dt - epoch).total_seconds() * 1000.0)

def format_timestamp(t):
  return datetime.fromtimestamp(float(t)/1000).strftime("%Y%m%d-%H:%M:%S")

def format_elapsedime(millis):
  m, s = divmod(millis/1000, 60)
  h, m = divmod(m, 60)
  return  "%d:%02d:%02d" % (h, m, s)


# curl 'http://bottou01.sjc.cloudera.com:25000/queries?json' | more
def get_impala_stats():
  return 1

def get_rmstats(kerb,period_secs,rm_host):
  app.logger.debug("In get_rmstats")
  nKey='queue'

  timenow =  unix_timestamp_secs()


  app.logger.debug("TIMENOW is " + str(timenow) )
  app.logger.debug("Checking URL   http://"+rm_host +":" + app.config['YARN_PORT'] +"/ws/v1/cluster/apps")

  opener = urllib2.build_opener()

  if kerb==True:
    opener.add_handler(ul2k.HTTPKerberosAuthHandler())

  jobdict = json.load(opener.open("http://"+rm_host+":" + app.config['YARN_PORT'] +"/ws/v1/cluster/apps"))

#  app.logger.debug("In get_rmstats 5 " + json.dumps(jobdict) )



  if jobdict['apps']:
    alljobs = jobdict['apps']['app']

    batch_offset=timedelta(seconds=period_secs)
    periodBegin_dt =  datetime.now() - batch_offset

    periodBegin_secs = periodBegin_dt.strftime('%s')


    runningOrFinished  = filter(lambda x: (x['progress'] < 100.0 and x['progress'] > 0) or int(x['finishedTime']/1000) > periodBegin_secs, alljobs)

    app.logger.debug("In get_rmstats 6 " + json.dumps(runningOrFinished) )

    if len(runningOrFinished):
      for x in runningOrFinished:
        x.update({"periodBegin_dt"   : datetime.fromtimestamp(periodBegin_secs) })
        x.update({"host"             : rm_host})
        x.update({"startedTime_dt"   : datetime.fromtimestamp( x['startedTime']/1000 ) } )
        x.update({"finishedTime_dt"  : datetime.fromtimestamp( x['finishedTime']/1000 ) } )
        x.pop('startedTime',None)
        x.pop('finishedTime',None)
        app.logger.debug("job " + x['id']  + " periodBegin " + str(x['periodBegin_dt']) + " " + " finishedTime " + str(x['finishedTime_dt'])   )
#        app.logger.debug("job " + item['id']  + " periodBegin " + str(periodBegin) + " " + " finishedTime " + str(int(item['finishedTime']/1000))+ " finished time + 3 hours" + str(st)   )

 
#     app.logger.debug("about to insert"  )
      with app.app_context():
        db.engine.execute(RMStats.__table__.insert(),runningOrFinished)
#      app.logger.debug("back from insert"  )

  else:
    app.logger.debug("No jobs found"  )



def get_impala_stats(kerb,period_secs,impalad):
  app.logger.debug("In get_impala_stats for " + impalad)
  nKey='queue'


  app.logger.debug("Checking URL   http://"+impalad +":" + app.config['IMPALA_PORT'] +app.config['IMPALA_URI'])
  batch_offset=timedelta(seconds=period_secs)
  periodBegin_dt =  datetime.now() - batch_offset

  opener = urllib2.build_opener()

  if kerb==True:
    opener.add_handler(ul2k.HTTPKerberosAuthHandler())

  impala_dict = json.load(opener.open("http://"+impalad+":" + app.config['IMPALA_PORT'] +app.config['IMPALA_URI']))

#  app.logger.debug("In get_impala_stats 5 " + json.dumps(impala_dict) )
#num_in_flight_queries
  if impala_dict['num_in_flight_queries'] > 0:
    app.logger.debug("num_in_flight_queries is " + str(impala_dict['num_in_flight_queries']) )

  if impala_dict['num_executing_queries'] > 0:
    app.logger.debug("num_executing_queries is " + str(impala_dict['num_executing_queries']) )

  if impala_dict['num_waiting_queries'] > 0:
    app.logger.debug("num_waiting_queries is " + str(impala_dict['num_waiting_queries']) )

  if impala_dict['completed_log_size'] > 0:

    entries = impala_dict['completed_queries']

    add_impala_records(entries,(lambda x: ( x['end_time_dt'] > periodBegin_dt)),'COMPLETED',periodBegin_dt,impalad)


def add_impala_records(entries,filter_func,state,periodBegin_dt,impalad):


  for x in entries:
    start_time_dt  = datetime.strptime( x['start_time'][:-3],"%Y-%m-%d %H:%M:%S.%f") # trim off last 3 000s from timestamp string
    end_time_dt    = datetime.strptime( x['start_time'][:-3],"%Y-%m-%d %H:%M:%S.%f")

    
    x.update({'duration_ms'     : conv_duration_to_millis(x['duration']     ) })
    x.update({'waiting_time_ms' : conv_duration_to_millis(x['waiting_time'] ) })
    x.update({'start_time_dt'   : start_time_dt                               })
    x.update({'end_time_dt'     : end_time_dt                                 })
    x.update({"periodBegin_dt"  : periodBegin_dt                              })
    x.update({"state"           : state                                       })
    x.update({"host"             : impalad                                     })
    del x['start_time'  ] 
    del x['end_time'    ] 
    del x['duration'    ] 
    del x['waiting_time']
#    app.logger.debug(impalad + " COMPARE                                           PERIODBEGIN_DT " +  str(periodBegin_dt)+ "      END_TIME_DT  "  +  str(x['end_time_dt'])  + " DIFF:  " + str(periodBegin_dt - x['end_time_dt']) )
    if x['end_time_dt'] > periodBegin_dt:
      app.logger.debug(" end time was AFTER periodbegin")
 #   else:
#      app.logger.debug(" end time was BEFORE periodbegin")

  keepers  = filter(lambda x: filter_func(x), entries)

#  app.logger.debug("In get_impala_stats 6 " + json.dumps(keepers) )

  if len(keepers):
    for item in keepers:
      app.logger.debug("inserting query " + item['stmt'] )

    app.logger.debug("about to insert"  )
    with app.app_context():
      db.engine.execute(Impala_Stats.__table__.insert(),keepers)
    app.logger.debug("back from insert"  )

  else:
    app.logger.debug("No queries found"  )

import re
def conv_duration_to_millis(ds):
  matches=re.match(r"(?P<hours>(\d+h)*)(?P<minutes>(\d+m)*(?!s))(?P<seconds>(\d+s)*)(?P<millis>(\d+ms)*)", ds)
  md=matches.groupdict()
  dur_ms=0
  if md['millis']:
    dur_ms=int(md['millis'][:-2])  # strip off the 'ms'
  if md['seconds']:
    dur_ms += int(md['seconds'][:-1]) * 1000 # strip of the 's'
  if md['minutes']:
    dur_ms += int(md['minutes'][:-1]) * 60000  # strip of the 'm'
  if md['hours']:
    dur_ms += int(md['hours'][:-1]) * 3600000
  return dur_ms



## query_summary?json&query_id=
#def compute_impala_resource_consumption():
#
