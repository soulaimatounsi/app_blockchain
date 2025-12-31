// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

contract Traceability {
    struct Record {
        string contractIdentifier;  // e.g., contract address or code hash
        string resultType;          // "LLM" or "ML"
        string resultHash;          // SHA-256 hash
        string modelName;           // Model used
        uint256 timestamp;          // When stored
        address sender;             // Who stored it
    }

    Record[] public records;

    event RecordStored(
        uint256 indexed id,
        string contractIdentifier,
        string resultType,
        string resultHash,
        string modelName,
        uint256 timestamp,
        address sender
    );

    function storeRecord(
        string memory _contractIdentifier,
        string memory _resultType,
        string memory _resultHash,
        string memory _modelName
    ) public {
        Record memory newRecord = Record({
            contractIdentifier: _contractIdentifier,
            resultType: _resultType,
            resultHash: _resultHash,
            modelName: _modelName,
            timestamp: block.timestamp,
            sender: msg.sender
        });

        records.push(newRecord);

        emit RecordStored(
            records.length - 1,
            _contractIdentifier,
            _resultType,
            _resultHash,
            _modelName,
            block.timestamp,
            msg.sender
        );
    }

    function getRecord(uint256 id) public view returns (Record memory) {
        require(id < records.length, "Record does not exist");
        return records[id];
    }

    function getRecordsCount() public view returns (uint256) {
        return records.length;
    }
}
