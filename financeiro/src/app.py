import os
import sys
import json
import logging
import sentry_sdk

from consumers import make_consumers, listen_kill_server
from threading import Event
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from api import api
from flask_kafka import FlaskKafka
from werkzeug.exceptions import HTTPException, InternalServerError, NotFound


def make_app():
  logging.basicConfig(stream=sys.stdout, level=logging.INFO)

  environment = os.environ.get("APPLICATION_ENV", "development")
  application = Flask(__name__)
  api.init_app(application)

  sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[FlaskIntegration()],
    environment=environment
  )

  bus = make_consumers(application)
  bus.run()
  listen_kill_server(bus)

  return application


