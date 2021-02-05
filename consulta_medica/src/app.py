import os
import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from api import api

def make_app():
  environment = os.environ.get("APPLICATION_ENV", "development")
  application = Flask(__name__)
  application.config.from_object("config.default")
  api.init_app(application)

  sentry_sdk.init(
    dsn=application.config["SENTRY_DSN"],
    integrations=[FlaskIntegration()],
    environment=environment
  )

  @application.route("/error")
  def error():
    error = 1 / 0
    return "Hello World!"

  return application


if __name__ == "__main__":
    app = make_app()
    app.run(host="0.0.0.0")