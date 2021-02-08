import os
import json
import logging
import signal

from threading import Event
from flask_kafka import FlaskKafka


def make_consumers(application):
  INTERRUPT_EVENT = Event()
  logging.info("Conectando no Kafka: "+os.environ.get("KAFKA_BROKERS")+" / "+os.environ.get("KAFKA_SECURITY_PROTOCOL"))

  bus = FlaskKafka(
      INTERRUPT_EVENT,
      security_protocol=os.environ.get("KAFKA_SECURITY_PROTOCOL"),
      bootstrap_servers=os.environ.get("KAFKA_BROKERS"),
      group_id="financeiro",
      value_deserializer=lambda v: json.loads(v),
  )

  @bus.handle("consulta-atualizada")
  def handler_consulta_atualizada(msg):
    logging.info("mensagem recebida "+msg)

  return bus

def listen_kill_server(bus):
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGINT, bus.interrupted_process)
    signal.signal(signal.SIGQUIT, bus.interrupted_process)
    signal.signal(signal.SIGHUP, bus.interrupted_process)