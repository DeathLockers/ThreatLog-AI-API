import asyncio
import ast
import logging
from requests import Session
from kafka import KafkaConsumer, TopicPartition
from kafka.structs import OffsetAndMetadata
from ..core import connection_manager, getenv
from ..schemas import (LogKafkaConsumser as SchemaLogKafkaConsumser,
                       LogRawKafkaConsumer as SchemaLogRawKafkaConsumer,
                       PredictedLogKafkaConsumser as SchemaPredictedLogKafkaConsumser)


async def kafka_consumer(db: Session):
  from ..services import insert_log, insert_predicted_log, insert_notification

  """Consumer de Kafka para recibir mensajes de la cola y procesarlos"""
  try:

    consumer = KafkaConsumer(
        getenv('KAFKA_CONSUMER_TOPIC', 'predicted_logs'),
        bootstrap_servers=getenv('KAFKA_HOST', 'localhost:9092'),
        group_id='alert_consumers',
        enable_auto_commit=False,
        auto_offset_reset='earliest',
        value_deserializer=decode,
        key_deserializer=decode
    )

    logging.info("Esperando nuevos mensajes...")

    while True:
      try:
        topics = consumer.poll(timeout_ms=500)
        for topic, values in topics.items():
          for msg in values:
            if msg is None:
              continue
            try:

              log_dict = decode(msg)

              log = SchemaLogKafkaConsumser(
                  host=log_dict['log_host'],
                  service=log_dict['log_service'],
                  pid=log_dict['log_pid'],
                  message=log_dict['log_message'],
                  datetime=log_dict['log_datetime'],
                  time_execution=log_dict['log_time_execution'],
                  user_id=log_dict['log_user_id']
              )

              log_id, log_datetime = insert_log(db, log)

              if (log_dict['predicted_log_target']):
                predicted_log_target = True
              else:
                predicted_log_target = False

              predicted_log = SchemaPredictedLogKafkaConsumser(
                  host=log_dict['predicted_log_host'],
                  service=log_dict['predicted_log_service'],
                  pid=log_dict['predicted_log_pid'],
                  message=log_dict['predicted_log_message'],
                  timestamp=log_dict['predicted_log_timestamp'],
                  time_execution=log_dict['predicted_log_time_execution'],
                  target=predicted_log_target,
                  log_id=log_id
              )

              insert_predicted_log(db, predicted_log)

              if predicted_log_target:
                notification_id = insert_notification(db, log_id)

                await connection_manager.send_personal_message(
                  {"id": notification_id,
                   "log": {"message": log_dict['log_message'], "datetime": log_datetime}
                   },
                  log_dict['log_user_id']
                )

              tp = TopicPartition(topic.topic, msg.partition)
              consumer.commit({tp: OffsetAndMetadata(msg.offset, None, msg.leader_epoch)})

              # Aquí puedes procesar el mensaje y guardarlo en la base de datos
              # db_session.insert()
              # Enviar el mensaje al WebSocket correspondiente

            except Exception as ex:
              logging.error(f"Error recuperant kafka message: {str(ex)}", ex)
        logging.debug("Esperando nuevos mensajes...")
        await asyncio.sleep(5)
      except asyncio.CancelledError:
        logging.info("Consumo de Kafka detenido.")
        break
      except Exception as e:
        logging.error(f"Error al procesar el mensaje: {e}")
  except Exception as ex:
    logging.error(f"Error al iniciar el consumidor de Kafka: {ex}")


def decode(data) -> SchemaLogRawKafkaConsumer:
  """Decodifica el mensaje recibido de Kafka"""
  try:
    if data is None:
      return None

    log_bytes = data.value
    log_str = log_bytes.decode('UTF-8')
    return ast.literal_eval(log_str)

  except Exception as e:
    logging.error(f"Error al decodificar el mensaje: {e}")
    return data
