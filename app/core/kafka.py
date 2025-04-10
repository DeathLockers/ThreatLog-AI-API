import asyncio
import json
import os
import logging
from kafka import KafkaConsumer, TopicPartition
from requests import Session
from ..core import connection_manager

async def kafka_consumer(db: Session):
    """Consumer de Kafka para recibir mensajes de la cola y procesarlos"""
    try:
        consumer = KafkaConsumer(
            'alert_topic',
            bootstrap_servers=os.environ.get('KAFKA_HOST', 'localhost:9092'), 
            group_id='alert_consumers',
            enable_auto_commit=False,
            auto_offset_reset='earliest',
            value_deserializer=decode,
            key_deserializer=decode
        )
        while True:
            try:
                topics = consumer.poll(timeout_ms=5000)
                for topic, values in topics.items():
                    for msg in values:
                        if msg is None:
                            continue
                        client = msg.value['client_id']
                        log = msg.value['message']
                        status = msg.value['status']

                        if status == 1:
                            await connection_manager.send_personal_message(log, client)
                        
                        # Aquí puedes procesar el mensaje y guardarlo en la base de datos
                        # db_session.insert()
                        # Enviar el mensaje al WebSocket correspondiente
                consumer.commit()
                logging.info("Esperando nuevos mensajes...")
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