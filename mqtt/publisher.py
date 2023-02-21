import paho.mqtt.client as mqtt

import json
from time import sleep

from sensors.sensorA import SensorA
from utils.database_commands import get_interval_publish_to_broker_from_sqlite


class MqttPublisher:

    def __init__(self, address, port, topic, interval):
        self.broker_address = address
        self.broker_port = port
        self.topic = topic
        self.interval = interval
        self.mqtt_client = mqtt.Client()
        # connect:
        self.mqtt_client.connect(address, port)

    def publish_to_mqtt(self, data):
        print(data)
        payload = json.dumps(data)
        mid = self.mqtt_client.publish(self.topic, payload)
        if mid[0] != mqtt.MQTT_ERR_SUCCESS:
            print("Error publishing message")
        else:
            print("Message published successfully")


if __name__ == '__main__':
    broker_address = '127.0.0.1'
    broker_port = 1883
    broker_topic = 'weather'
    sqlite_filepath = '../django_website/db.sqlite3'
    publish_interval = get_interval_publish_to_broker_from_sqlite(sqlite_filepath)

    # get data from sensorA and start publishing:
    sensor_a = SensorA(dataset_csv_filepath='../datasets/homeA2016.csv')
    publisher = MqttPublisher(broker_address, broker_port, broker_topic, publish_interval)
    reader = sensor_a.get_data_from_dataset()
    while True:
        # read data from sensor:
        sensor_data = next(reader)
        # publish in broker:
        publisher.publish_to_mqtt(sensor_data)
        # update broker publish interval:
        publisher.interval = get_interval_publish_to_broker_from_sqlite(sqlite_filepath)
        sleep(publisher.interval)
