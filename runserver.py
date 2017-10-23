import os
import sys
from MTHMBE import app
from MTHMBE.core import db
from MTHMBE.models import RMStats
#from apscheduler.scheduler import Scheduler
from flask import Flask

def runserver():

        app.logger.debug("in runserver.py about to run scheduler now.")
        from MTHMBE import scheduler
        scheduler.start()

        app.logger.debug("in runserver.py app.run")       
        port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)



if __name__ == '__main__':
        if len(sys.argv) > 1:
          app.logger.debug("about to init_app")
          with app.app_context():
            db.init_app(app)
            db.create_all()
          app.logger.debug("doneinit_app")

	runserver()
