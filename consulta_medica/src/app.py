import os
import sys
import sentry_sdk
import logging
from flask import Flask
from model import init_db
from flask_sqlalchemy import SQLAlchemy
from sentry_sdk.integrations.flask import FlaskIntegration
from infrastructure.kafka import connect_producer
from api import api

def make_app():
  logging.basicConfig(stream=sys.stdout, level=logging.INFO)
  environment = os.environ.get("APPLICATION_ENV", "development")
  application = Flask(__name__)
  application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
  api.init_app(application)

  # inicia banco de dados
  init_db(application)

  # Configuração do Sentry
  sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[FlaskIntegration()],
    environment=environment
  )

  # Producer do Kafka
  logging.info("Conectando no Kafka: "+os.environ.get("KAFKA_BROKERS")+" / "+os.environ.get("KAFKA_SECURITY_PROTOCOL"))
  connect_producer(os.environ.get("KAFKA_BROKERS"),
                  security_protocol=os.environ.get("KAFKA_SECURITY_PROTOCOL"))
  return application
