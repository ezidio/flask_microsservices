import logging

from bson.json_util import dumps, loads
from kafka import KafkaProducer

_producer = None

def connect_producer(servers, security_protocol="PLAINTEXT"):
    global _producer
    try:
        _producer = KafkaProducer(
            bootstrap_servers=servers,
            value_serializer=lambda v: dumps(v).encode("utf-8"),
            security_protocol=security_protocol,
        )
    except Exception as ex:
        logging.error(ex)
    finally:
        return _producer


def close_producer():
    if _producer:
        _producer.close()


def producer():
    return _producer

# Publica uma mensagem
def publish_message(topic, value, origin=""):
  prod = producer()
  try:
    prod.send(topic, value=value)
  except Exception as e:
    create_deadletter(topic, value, e, origin)

# Envia para a deadletter
def create_deadletter(topic, value, exception, origin=""):
    prod = producer()
    metadata = {"topic": topic, "raw": value, "exception": str(exception), "origin": origin}
    try:
        prod.send("dead_letter_queue", value=metadata)
    except Exception as e:
        logging.error(e)