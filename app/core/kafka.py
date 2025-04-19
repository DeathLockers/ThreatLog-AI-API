import asyncio
import json
import os
import logging
from kafka import KafkaConsumer, TopicPartition
from requests import Session
from ..core import connection_manager

pred_threshold = os.environ.get("ALERT_PRED_THRESHOLD",.96)  # Umbral de predicción para enviar el mensaje al WebSocket

async def kafka_consumer(db: Session):
    """Consumer de Kafka para recibir mensajes de la cola y procesarlos"""
    from ..services.log import inser_log, insert_predicted
    try:
        consumer = KafkaConsumer(
            os.environ.get('KAFKA_CONSUMER_TOPIC', 'predicted_logs'),
            bootstrap_servers=os.environ.get('KAFKA_HOST', 'localhost:9092'), 
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
                            client = msg.value['client_id']
                            log = msg.value['message']
                            pred = msg.value['prediction']

                            id = inser_log(db, client, log)

                            if pred >= pred_threshold:
                                pred_id = insert_predicted(db, id, log)
                                await connection_manager.send_personal_message({"message":log, "id":pred_id}, client)
                            consumer.commit(msg.offset)
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


def decode(data):
    """Decodifica el mensaje recibido de Kafka"""
    try:
        if data is None:
            return None
        return json.loads(data.decode('utf-8'))
    except Exception as e:
        try:
            return json.loads(data)
        except Exception as e:
            logging.error(f"Error al decodificar el mensaje: {e}")
            return data