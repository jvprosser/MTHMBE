import os
import json
from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for

app = Flask(__name__)

import logging
from logging.handlers import RotatingFileHandler

from settings import Config


app.config.from_object(Config)
app.url_map.strict_slashes = False

from flask_apscheduler import APScheduler


handler = RotatingFileHandler('myapp.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(module)s.%(filename)s:%(lineno)d]'))

scheduler = APScheduler()
scheduler.init_app(app)


app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.debug("__init__.py")
logger.debug(app.config)

import MTHMBE.views
import MTHMBE.core
import MTHMBE.models
import MTHMBE.controllers



