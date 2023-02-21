pragma solidity ^0.8.0;

contract Sensor {

    uint private index = 0;

    event AddedData(string message, bytes sensor_data, uint index);

    function emitEvent(string memory message, bytes memory data) internal {
        index += 1;
        emit AddedData(message, data, index);
    }

    function addSensorData(bytes memory data) public returns (bool) {
        emitEvent("New Sensor Data", data);
        return true;
    }

}
