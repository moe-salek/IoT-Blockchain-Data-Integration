import requests

import base64
import json

from blockchain.utils.get_w3 import get_w3
from blockchain.utils.contract_tools import get_sensor_contract, load_sensor_contract_address

if __name__ == "__main__":
    w3 = get_w3()
    contract_address = load_sensor_contract_address()
    contract, w3 = get_sensor_contract(w3, contract_address)
    event_filter = contract.events.AddedData.create_filter(fromBlock='latest')


    def handle_event(event):
        index = event['args']['index']
        message = event['args']['message']
        sensor_data = json.loads(event['args']['sensor_data'].decode())
        print(index, message + ':', sensor_data)
        # Send notification to Django Server:
        url = 'http://127.0.0.1:8000/core/notification/'
        params = {
            'idx': index,
            'msg': message,
            'data': base64.urlsafe_b64encode(json.dumps(sensor_data).encode()),
        }
        try:
            res = requests.get(url=url, params=params)
            if res.status_code == 201:
                print('Successfully sent notification to django server.')
            else:
                print('Failed to send notification to django server. Server response:', res.text)
        except Exception:
            print('Failed to send notification to django server. Is Django Server running?')


    print('Running event-handler for "AddedData" events...')
    while True:
        events = event_filter.get_new_entries()
        for e in events:
            handle_event(e)
