import json

import paho.mqtt.client as mqtt

import multiprocessing
import time

from blockchain.add_sensor_data import add_sensor_data_to_blockchain
from utils.database_commands import get_interval_publish_to_blockchain_from_sqlite, get_low_high_temp_range


class MqttSubscriber:
    def __init__(self, address, port, topic):
        self.broker_address = address
        self.broker_port = port
        self.topic = topic
        self.mqtt_client = mqtt.Client()

    def subscribe_to_mqtt(self, blockchain_queue):
        def on_message(client, userdata, msg):
            received_data = msg.payload.decode()
            blockchain_queue.put(received_data)
            print("[Subscriber] Received data and sent to blockchain queue. Data:", received_data)

        self.mqtt_client.connect(self.broker_address, self.broker_port)
        self.mqtt_client.on_message = on_message
        self.mqtt_client.subscribe(self.topic)
        print('[Subscriber] Starting subscriber...')
        self.mqtt_client.loop_forever()


def start_subscriber(blockchain_queue, address, port, topic):
    subscriber = MqttSubscriber(address, port, topic)
    subscriber.subscribe_to_mqtt(blockchain_queue)


def start_sending_to_blockchain(blockchain_queue):
    sqlite_filepath = '../django_website/db.sqlite3'
    while True:
        data = blockchain_queue.get()
        if data is None:
            break
        print(f"[Blockchain Middleware] Received data from queue. Data: {data}")
        # Filter data:
        sensor_temperature = float(json.loads(data)['temperature'])
        # Fetch low, high temperature range from Database:
        low_temp_range, high_temp_range = get_low_high_temp_range(sqlite_filepath)
        if low_temp_range <= sensor_temperature <= high_temp_range:  # Temperature in normal range:
            res = add_sensor_data_to_blockchain(data)
            if res:
                print('[Blockchain Middleware] Successfully sent data to blockchain.')
            else:
                print('[Blockchain Middleware] Failed to send data to blockchain.')
        else:  # Temperature outside normal range (Critical):
            print(
                '[Blockchain Middleware] Critical Temperature detected. It won\'t be sent to blockchain. Temperature:',
                sensor_temperature)
        blockchain_publish_interval = get_interval_publish_to_blockchain_from_sqlite(sqlite_filepath)
        time.sleep(blockchain_publish_interval)


#
if __name__ == '__main__':
    broker_address = '127.0.0.1'
    broker_port = 1883
    broker_topic = 'weather'
    queue = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=start_subscriber, args=(queue, broker_address, broker_port, broker_topic))
    p2 = multiprocessing.Process(target=start_sending_to_blockchain, args=(queue,))
    p1.start()
    p2.start()
    while True:
        if not p1.is_alive():
            queue.put(None)
            p2.join()
            break
