from flask import Blueprint
from flask_restplus import Namespace, Resource

api = Namespace("infra", description = "Apis de gerenciamento da infraestrutura do microsserviço")

@api.route('/healthcheck')
class HealthcheckResource(Resource):
  def get(self):
    return "I'm Alive"