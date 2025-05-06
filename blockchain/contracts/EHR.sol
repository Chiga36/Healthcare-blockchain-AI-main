pragma solidity ^0.8.0;

contract EHR {
    struct Record {
        string ipfsHash; // Hash of EHR stored on IPFS
        address patient; // Patient's Ethereum address
        mapping(address => bool) authorized; // Authorized providers
        uint256 timestamp; // Creation timestamp
    }

    mapping(uint256 => Record) public records;
    uint256 public recordCount;

    event RecordAdded(uint256 recordId, string ipfsHash, address patient);
    event AccessGranted(uint256 recordId, address provider);
    event AccessRevoked(uint256 recordId, address provider);

    // Add a new EHR record
    function addRecord(string memory _ipfsHash) public {
        recordCount++;
        Record storage newRecord = records[recordCount];
        newRecord.ipfsHash = _ipfsHash;
        newRecord.patient = msg.sender;
        newRecord.timestamp = block.timestamp;
        newRecord.authorized[msg.sender] = true; // Patient has access

        emit RecordAdded(recordCount, _ipfsHash, msg.sender);
    }

    // Grant access to a provider
    function grantAccess(uint256 _recordId, address _provider) public {
        require(records[_recordId].patient == msg.sender, "Only patient can grant access");
        records[_recordId].authorized[_provider] = true;
        emit AccessGranted(_recordId, _provider);
    }

    // Revoke access from a provider
    function revokeAccess(uint256 _recordId, address _provider) public {
        require(records[_recordId].patient == msg.sender, "Only patient can revoke access");
        records[_recordId].authorized[_provider] = false;
        emit AccessRevoked(_recordId, _provider);
    }

    // Get record details (only for authorized users)
    function getRecord(uint256 _recordId) public view returns (string memory, address, uint256) {
        require(records[_recordId].authorized[msg.sender], "Not authorized");
        Record storage record = records[_recordId];
        return (record.ipfsHash, record.patient, record.timestamp);
    }

    // Placeholder for ZKP integration
    // Future enhancement: Use zk-SNARKs to verify record access without revealing data
    // Example: Verify patient eligibility for a trial without disclosing sensitive details
}