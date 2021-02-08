import logging
from datetime import datetime
from flask import Blueprint
from flask_restplus import Namespace, Resource, fields
from infrastructure.kafka import publish_message
from model import db, Consulta

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
    # Precisa ter uma validação do schema da consulta
    data = api.payload
    logging.info("Criando nova consulta: "+data['id'])

    consulta = Consulta(
      id = data['id'],
      start_date = datetime.strptime(data['start_date'], '%Y-%m-%d %H:%M:%S'),
      end_date = datetime.strptime(data['end_date'], '%Y-%m-%d %H:%M:%S'),
      physician_id = data['physician_id'],
      patient_id = data['patient_id'],
      price = data['price']
    )
    db.session.add(consulta)
    db.session.commit()
    publish_message("consulta-atualizada", data)
    return "OK"

  @api.doc('Atualiza consulta')
  def put(self, data):
    # Precisa ter uma validação do schema da consulta
    # Precisa ter uma validação do schema da consulta
    dado = {
      "id": "84ab6121-c4a8-4684-8cc2-b03024ec0f1d",
      "start_date": "2020-12-01 13:00:00",
      "end_date": "2020-12-01 14:00:00",
      "physician_id": "ea959b03-5577-45c9-b9f7-a45d3e77ce82",
      "patient_id": "86158d46-ce33-4e3d-9822-462bbff5782e",
      "price": 200.00
    }
    logging.info("Criando nova consulta.")
    publish_message("consulta-atualizada", dado)
    return "OK"

  @api.doc('lista_consultas')
  def get(self):
    return "listando consultas"
