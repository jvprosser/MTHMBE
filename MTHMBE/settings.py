from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

class Config(object):
    DEBUG = True
    SECRET_KEY       = '2d47ab361e97d3330ba4fafe827c0a1c915b11c9ff28292e'
#    YARN_HOST        = "172.31.3.142"
    YARN_HOST        = "bottou02.sjc.cloudera.com"
    YARN_PORT        = "8088"
    JOBS = [
        {
            'id': 'get_rmstats_trigger',
            'func': 'MTHMBE.views:get_rmstats',
            'args': (False, 60),
            'replace_existing': True,
            'trigger': 'interval',
            'seconds': 60

        }
    ]

    TZ='America/Los_Angeles'
    
    SCHEDULER_JOBSTORES = {
        #'default': SQLAlchemyJobStore(url='mysql://ec2-user:test@localhost/MTHMBE' )
        'default': SQLAlchemyJobStore(url='sqlite:///./MTHMBE.db')
    }

#    SQL_ENGINE= 'mysql://ec2-user:test@localhost/MTHMBE'
    SQL_ENGINE= 'sqlite:///./MTHMBE.db'

#    SQLALCHEMY_DATABASE_URI = 'mysql://ec2-user:test@localhost/MTHMBE'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./MTHMBE.db'
    
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
