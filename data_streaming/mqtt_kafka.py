import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import json

#Mosquitto Conf
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "esp32/data"

kafka_broker = "kafka_service:9092"
kafka_topic = "ESP32_data"

kafka_producer = KafkaProducer(
    bootstrap_servers=kafka_broker,
    value_serializer=lambda data: json.dumps(data).encode('utf-8')
)

def on_message (client, userdata, msg)
    print(f'Message recive from MQTT: {msg.topic} {msg.payload.decode()}')
    data = {
        "topic": msg.topic,
        "payload_data": msg.payload.decode()
    }

    kafka_producer.send(kafka_topic, value=data)











