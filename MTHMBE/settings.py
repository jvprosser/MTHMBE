from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# grant all privileges on MTHMBE.* to 'mthmbe'@'localhost' identified by 'cloudera';
class Config(object):
    DEBUG = True
    SECRET_KEY       = '2d47ab361e97d3330ba4fafe827c0a1c915b11c9ff28292e'
#    YARN_HOST        = "172.31.3.142"
    YARN_HOST        = "bottou02.sjc.cloudera.com"
    YARN_PORT        = "8088"
    YARN_URI         = "/ws/v1/cluster/apps"
    JOBS = [
        {
            'id': 'get_impala_stats_trigger_02',
            'func': 'MTHMBE.views:get_impala_stats',
            'args': (False, 120,"bottou02.sjc.cloudera.com"),
            'replace_existing': True,
            'trigger': 'interval',
            'seconds': 120
        }
    ]

    IMPALA_DAEMONS=[ "bottou01.sjc.cloudera.com","bottou02.sjc.cloudera.com", "bottou03.sjc.cloudera.com","bottou04.sjc.cloudera.com","bottou05.sjc.cloudera.com"]
    IMPALA_PORT="25000"
    IMPALA_URI="/queries?json"

    TZ='America/Los_Angeles'
    SQLURL='mysql://mthmbe:cloudera@localhost/MTHMBE'
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=SQLURL )
        #'default': SQLAlchemyJobStore(url='sqlite:///./MTHMBE.db')
    }

    #    SQL_ENGINE= 'mysql://ec2-user:test@localhost/MTHMBE'
# SQL_ENGINE= 'sqlite:///./MTHMBE.db'
    SQL_ENGINE=SQLURL

#    SQLALCHEMY_DATABASE_URI = 'mysql://ec2-user:test@localhost/MTHMBE'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///./MTHMBE.db'
    SQLALCHEMY_DATABASE_URI = SQLURL
    
#    SCHEDULER_EXECUTORS = {
#        'default': {'type': 'threadpool', 'max_workers': 20}
#    }
#
#    SCHEDULER_JOB_DEFAULTS = {
#        'coalesce': False,
#        'max_instances': 3
#    }
#
    SCHEDULER_API_ENABLED = True


    SQLALCHEMY_TRACK_MODIFICATIONS=False


#          'trigger': {
#               'type': 'cron',
#               'second': 300
#            }


#        {
#            'id': 'get_rmstats_trigger',
#            'func': 'MTHMBE.views:get_rmstats',
#            'args': (False, 60,"bottou02.sjc.cloudera.com" ),
#            'replace_existing': True,
#            'trigger': 'interval',
#            'seconds': 60
#
#        },
#        {
#           'id': 'get_impala_stats_trigger_01',
#           'func': 'MTHMBE.views:get_impala_stats',
#           'args': (False, 60,"bottou01.sjc.cloudera.com"),
#           'replace_existing': True,
#           'trigger': 'interval',
#           'seconds': 60
#
#       },
#       {
#           'id': 'get_impala_stats_trigger_03',
#           'func': 'MTHMBE.views:get_impala_stats',
#           'args': (False, 60,"bottou03.sjc.cloudera.com"),
#           'replace_existing': True,
#           'trigger': 'interval',
#           'seconds': 60
#
#       },
#       {
#           'id': 'get_impala_stats_trigger_04',
#           'func': 'MTHMBE.views:get_impala_stats',
#           'args': (False, 60,"bottou04.sjc.cloudera.com"),
#           'replace_existing': True,
#           'trigger': 'interval',
#           'seconds': 60
#
#       },
#       {
#           'id': 'get_impala_stats_trigger_05',
#           'func': 'MTHMBE.views:get_impala_stats',
#           'args': (False, 60,"bottou05.sjc.cloudera.com"),
#           'replace_existing': True,
#           'trigger': 'interval',
#           'seconds': 60
#
#       }
