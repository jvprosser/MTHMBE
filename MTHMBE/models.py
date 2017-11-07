# Put models here


from sqlalchemy import PrimaryKeyConstraint
import datetime
from MTHMBE.core import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class RMStats(db.Model):
        __tablename__ = 'rmstats'
        __table_args__ = (
                PrimaryKeyConstraint('id', 'periodBegin_dt','host'),
        )
        user               = db.Column( db.String( 32 ) )
        queue              = db.Column( db.String( 32 ) )
        id                 = db.Column( db.String( 64 ) )
        allocatedVCores    = db.Column( db.Integer )
        allocatedMB        = db.Column( db.Integer )
        runningContainers  = db.Column( db.Integer )
        startedTime_dt     = db.Column( db.DateTime )
        finishedTime_dt    = db.Column( db.DateTime )
        memorySeconds      = db.Column( db.Integer )
        vcoreSeconds       = db.Column( db.Integer )
        name               = db.Column( db.String( 1024 ) )
        progress           = db.Column( db.Integer )
        finalStatus        = db.Column( db.String( 32 ) )
        applicationType    = db.Column( db.String( 64 ) )
        periodBegin_dt     = db.Column( db.DateTime )
        host               = db.Column( db.String( 64 ) )


        def __repr__(self):
              return '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(self.user, self.queue, self.id, self.allocatedVCores, 
                                                                           self.allocatedMB, self.runningContainers, format_timestamp(self.startedTime_dt,"%Y-%m-%d %H:%M:%S.%f" ),
                                                                           format_timestamp(self.finishedTime_dt,"%Y-%m-%d %H:%M:%S.%f" ),self.memorySeconds, self.vcoreSeconds, 
                                                                           self.name, self.progress, self.finalStatus, self.applicationType, str(self.periodBegin_dt))


class Impala_Stats(db.Model):
        __tablename__  = 'impalastats'
        __table_args__ = (
                PrimaryKeyConstraint('query_id','host'),
        )
        effective_user = db.Column( db.String( 64 ) ) 
        default_db     = db.Column( db.String( 64 ) )
        stmt           = db.Column( db.String( 4096 ) )
        stmt_type      = db.Column( db.String( 32 ) )
        start_time_dt  = db.Column( db.DateTime )  # "2017-10-18 03:17:31.711271000",
        end_time_dt    = db.Column( db.DateTime )  # "2017-10-18 03:17:31.723423000",
        duration       = db.Column( db.BigInteger )  #": "12ms",
        progress       = db.Column( db.String( 64 ) )
        state          = db.Column( db.String( 64 ) )
        rows_fetched   = db.Column( db.BigInteger )
        query_id       = db.Column( db.String( 64 ) )
        last_event     = db.Column( db.String( 64 ) )
        waiting        = db.Column( db.Boolean ) #": true,
        executing      = db.Column( db.Boolean ) #": false,
        waiting_time   = db.Column( db.BigInteger )  #: "133h40m",
        resource_pool  = db.Column( db.String(128) )  #": ""
        periodBegin_dt     = db.Column( db.DateTime )
        host               = db.Column( db.String( 64 ) )

     


        def __repr__(self):
              return '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(self.effective_user, self.default_db, self.stmt,
                                                                              self.stmt_type, self.start_time, self.end_time, self.duration,
                                                                              self.progress, self.state, self.rows_fetched, self.query_id,
                                                                              self.last_event, self.waiting,self.executing, self.waiting_time,self.resource_pool)
