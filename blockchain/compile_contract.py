import os

from solcx import compile_source, install_solc
import json

if __name__ == '__main__':
    install_solc("0.8.0")

    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(dir_path + '/contracts/Sensor.sol', 'r') as sol_file:
        sol_code = sol_file.read()

    compiled_sol = compile_source(sol_code)
    print('Successfully compiled Sensor.sol')
    contract_interface = compiled_sol['<stdin>:Sensor']

    with open(dir_path + '/contracts/Sensor.abi', 'w') as abi_file:
        abi_file.write(json.dumps(contract_interface['abi']))

    with open(dir_path + '/contracts/Sensor.bin', 'w') as abi_file:
        abi_file.write(json.dumps(contract_interface['bin']))

    print('Successfully saved abi and bytecode')
