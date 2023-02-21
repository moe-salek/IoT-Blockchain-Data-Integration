from web3 import Web3

import os


def load_ganache_url():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/../Ganache.txt', 'r') as f:
        url = str(f.read())

    return url


def get_w3():
    ganache_url = load_ganache_url()
    instance = Web3(Web3.HTTPProvider(ganache_url))
    assert instance.is_connected()

    return instance
