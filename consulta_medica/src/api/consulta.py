import logging
from datetime import datetime
from flask import Blueprint
from flask_restplus import Namespace, Resource, fields
from infrastructure.kafka import publish_message
from model.consulta import persist, load_all

api = Namespace("consultas", description = "Endpoints relacionados a consulta")

consulta_model = api.model('consulta', {
  'id' : fields.String(required=True, description='Identificador da consulta'),
  'start_date' : fields.String(required=True, description='Data/hora inicio da consulta'),
  'end_date' : fields.String(required=False, description='Data/hora fim da consulta'),
  'physician_id' : fields.String(required=True, description='Identificador do médico'),
  'patient_id' : fields.String(required=True, description='Identificador do paciente'),
  'price' : fields.String(required=True, description='Preço da consulta')
})

@api.route('/')
class ConsultaResource(Resource):
  @api.doc('cria_consulta')
  @api.expect(consulta_model)
  def post(self):
    data = api.payload
    persist(data)
    publish_message("consulta-atualizada", data)
    return "OK"

  @api.doc('Atualiza consulta')
  @api.expect(consulta_model)
  def put(self, data):
    data = api.payload
    persist(data)
    publish_message("consulta-atualizada", data)
    return "OK"

  @api.doc('lista_consultas')
  def get(self):
    return load_all()