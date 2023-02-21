from blockchain.utils.contract_tools import save_sensor_contract_address
from blockchain.utils.get_w3 import get_w3
from blockchain.utils.load_abi import load_local_abi
from blockchain.utils.load_bytecode import load_local_bytecode

if __name__ == '__main__':
    w3 = get_w3()
    abi = load_local_abi()
    bytecode = load_local_bytecode()
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    account = w3.eth.accounts[0]
    w3.eth.default_account = account

    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    save_sensor_contract_address(contract_address)
    sensor_contract = w3.eth.contract(address=contract_address, abi=abi)

    print('Successfully deployed Sensor contract')
