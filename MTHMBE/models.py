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
                PrimaryKeyConstraint('id', 'periodBegin'),
        )
        user               = db.Column( db.String( 32 ) )
        queue              = db.Column( db.String( 32 ) )
        id                 = db.Column( db.String( 64 ) )
        allocatedVCores    = db.Column( db.Integer )
        allocatedMB        = db.Column( db.Integer )
        runningContainers  = db.Column( db.Integer )
        startedTime        = db.Column( db.BigInteger )
        finishedTime       = db.Column( db.BigInteger )
        memorySeconds      = db.Column( db.Integer )
        vcoreSeconds       = db.Column( db.Integer )
        name               = db.Column( db.String( 64 ) )
        progress           = db.Column( db.Integer )
        finalStatus        = db.Column( db.String( 32 ) )
        applicationType    = db.Column( db.String( 64 ) )
        periodBegin                 = db.Column( db.BigInteger )

        def __repr__(self):
              return '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(self.user, self.queue, self.id, self.allocatedVCores, 
                                                                           self.allocatedMB, self.runningContainers, format_timestamp(self.startedTime, ),
                                                                           format_timestamp(self.finishedTime, ),self.memorySeconds, self.vcoreSeconds, 
                                                                           self.name, self.progress, self.finalStatus, self.applicationType, self.periodBegin)
