import logging
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import json

# Configuración de Mosquitto
mqtt_broker = "192.168.0.19"  # Cambia si es necesario
mqtt_port = 1883
mqtt_topic = "esp32/data"

# Configuración de Kafka
kafka_broker = "192.168.0.19:9092"  # Cambia por la IP de tu broker de Kafka
kafka_topic = "ESP32_data"

# Configuración del productor de Kafka
kafka_producer = KafkaProducer(
    bootstrap_servers=kafka_broker,
    value_serializer=lambda data: json.dumps(data).encode('utf-8'),
    max_block_ms=5000
)

# Callback que se ejecuta al recibir un mensaje en MQTT
def on_message(client, userdata, msg):
    try:
        print(f"Mensaje recibido de MQTT: {msg.topic} {msg.payload.decode()}")
        data = {
            "topic": msg.topic,
            "payload_data": msg.payload.decode()
        }
        print(f"Enviando mensaje a Kafka: {data}")
        # Enviar el mensaje a Kafka
        kafka_producer.send(kafka_topic, value=data)
    except Exception as ex:
        logging.error(f"Excepción al procesar el mensaje: {ex}")

# Configuración del cliente MQTT
client_mqtt = mqtt.Client()
client_mqtt.on_message = on_message

# Conectar al broker MQTT y suscribirse al tema
client_mqtt.connect(mqtt_broker, mqtt_port, 60)
client_mqtt.subscribe(mqtt_topic)

# Iniciar el bucle de escucha de MQTT
try:
    client_mqtt.loop_forever()
except KeyboardInterrupt:
    print("Proceso interrumpido por el usuario")
finally:
    client_mqtt.disconnect()
    kafka_producer.close()
