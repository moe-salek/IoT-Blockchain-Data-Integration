import json
import os

from web3 import Web3
from web3.contract import Contract
from typing import (
    Type,
    Tuple,
)

from blockchain.utils.load_abi import load_local_abi


def get_sensor_contract(w3, contract_address) -> Tuple[Type[Contract], Type[Web3]]:
    abi = load_local_abi()
    sensor_contract = w3.eth.contract(address=contract_address, abi=abi)

    return sensor_contract, w3


def save_sensor_contract_address(sensor_contract_address):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/../contracts/Address.txt', 'w') as f:
        f.write(json.dumps({'deployed_sensor_contract_address': sensor_contract_address}))


def load_sensor_contract_address():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/../contracts/Address.txt', 'r') as f:
        address = json.loads(f.read()).get('deployed_sensor_contract_address')

    return address
