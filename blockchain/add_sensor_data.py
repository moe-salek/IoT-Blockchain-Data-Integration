from blockchain.utils.contract_tools import get_sensor_contract, load_sensor_contract_address
from blockchain.utils.get_w3 import get_w3


def add_sensor_data_to_blockchain(sensor_data) -> bool:
    w3 = get_w3()
    account = w3.eth.accounts[0]
    w3.eth.default_account = account

    contract_address = load_sensor_contract_address()
    sensor_contract, _ = get_sensor_contract(w3, contract_address)
    tx_hash = sensor_contract.functions.addSensorData(sensor_data.encode()).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return True


if __name__ == '__main__':
    data = 'Some Random Sample Data'
    if add_sensor_data_to_blockchain(data):
        print('Successfully sent data to to blockchain. Sent data:', data)
