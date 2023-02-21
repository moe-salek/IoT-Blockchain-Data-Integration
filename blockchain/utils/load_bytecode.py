import json
import os


def load_local_bytecode():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/../contracts/Sensor.bin', 'r') as f:
        file_bytecode = json.loads(f.read())

    return file_bytecode
