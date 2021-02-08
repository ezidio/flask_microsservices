from flask import Blueprint
from flask_restplus import Namespace, Resource

api = Namespace("consultas", description = "Endpoints relacionados a consulta")

@api.route('/')
class ConsultaResource(Resource):
  @api.doc('cria_consulta')
  def post(self):
    return "Criando consulta"

  @api.doc('lista_consultas')
  def get(self):
    return "listando consultas"
