import json
import os


def load_local_abi():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/../contracts/Sensor.abi', 'r') as f:
        file_abi = json.loads(f.read())

    return file_abi
