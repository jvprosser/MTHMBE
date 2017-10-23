from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from MTHMBE import app
from models import RMStats
import core
import time
from time import mktime, strftime
from pytz import timezone

import datetime
from datetime import timedelta,datetime

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

def get_rmstats(kerb,period_secs):
  app.logger.debug("In get_rmstats")
  nKey='queue'

  timenow =  unix_timestamp_secs()
  app.logger.debug("TIMENOW is " + str(timenow) )
  app.logger.debug("Checking URL   http://"+app.config['YARN_HOST'] +":" + app.config['YARN_PORT'] +"/ws/v1/cluster/apps")

  opener = urllib2.build_opener()

  if kerb==True:
    opener.add_handler(ul2k.HTTPKerberosAuthHandler())

  jobdict = json.load(opener.open("http://"+app.config['YARN_HOST']+":" + app.config['YARN_PORT'] +"/ws/v1/cluster/apps"))

#  app.logger.debug("In get_rmstats 5 " + json.dumps(jobdict) )

  if jobdict['apps']:
    alljobs = jobdict['apps']['app']
#    periodBegin = timenow - (period_secs*1000)
    periodBegin = (timenow - period_secs)

    runningOrFinished  = filter(lambda x: (x['progress'] < 100.0 and x['progress'] > 0) or int(x['finishedTime']/1000) > periodBegin, alljobs)

#    app.logger.debug("In get_rmstats 6 " + json.dumps(runningOrFinished) )

    if len(runningOrFinished):
      for item in runningOrFinished:
        item.update({"periodBegin" : periodBegin})
        pbts=datetime.fromtimestamp(periodBegin )
        st=datetime.fromtimestamp(int(item['finishedTime']/1000) )
        sfst = datetime.fromtimestamp(int(item['finishedTime']/1000))
#        app.logger.debug("job " + item['id']  + " periodBegin " + str(pbts) + " " + " finishedTime " + str(sfst)+ " finished time + 3 hours" + str(st)   )
        app.logger.debug("job " + item['id']  + " periodBegin " + str(periodBegin) + " " + " finishedTime " + str(int(item['finishedTime']/1000))+ " finished time + 3 hours" + str(st)   )

 
#     app.logger.debug("about to insert"  )
      with app.app_context():
        db.engine.execute(RMStats.__table__.insert(),runningOrFinished)
#      app.logger.debug("back from insert"  )

  else:
    app.logger.debug("No jobs found"  )
    app.logger.debug("In get_rmstats 7 " + json.dumps(jobdict) )




