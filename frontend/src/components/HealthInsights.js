import React, { useState, useEffect } from "react";
import { getWeb3, getContract } from "../web3";

function PatientPortal({ language }) {
  const [web3, setWeb3] = useState(null);
  const [contract, setContract] = useState(null);
  const [account, setAccount] = useState("");
  const [records, setRecords] = useState([]);

  useEffect(() => {
    async function init() {
      const web3Instance = await getWeb3();
      const contractInstance = await getContract(web3Instance);
      const accounts = await web3Instance.eth.getAccounts();
      setWeb3(web3Instance);
      setContract(contractInstance);
      setAccount(accounts[0]);

      // Fetch records
      const recordCount = await contractInstance.methods.recordCount().call();
      const fetchedRecords = [];
      for (let i = 1; i <= recordCount; i++) {
        try {
          const record = await contractInstance.methods.getRecord(i).call({ from: accounts[0] });
          fetchedRecords.push({ id: i, ...record });
        } catch (error) {
          console.error(`Error fetching record ${i}:`, error);
        }
      }
      setRecords(fetchedRecords);
    }
    init();
  }, []);

  const addRecord = async (ipfsHash) => {
    await contract.methods.addRecord(ipfsHash).send({ from: account });
    // Refresh records
  };

  const grantAccess = async (recordId, providerAddress) => {
    await contract.methods.grantAccess(recordId, providerAddress).send({ from: account });
  };

  return (
    <div className="bg-white p-6 rounded shadow-md">
      <h2 className="text-xl mb-4">{language === "en" ? "Patient Portal" : "Portal del Paciente"}</h2>
      <div className="mb-4">
        <input
          type="text"
          placeholder="IPFS Hash"
          className="border p-2 mr-2"
          onChange={(e) => setIpfsHash(e.target.value)}
        />
        <button
          className="bg-blue-500 text-white p-2 rounded"
          onClick={() => addRecord(ipfsHash)}
        >
          Add Record
        </button>
      </div>
      <h3 className="text-lg mb-2">Your Records</h3>
      <ul>
        {records.map((record) => (
          <li key={record.id} className="mb-2">
            Record {record.id}: {record.ipfsHash} (Created: {new Date(record.timestamp * 1000).toLocaleString()})
            <button
              className="ml-2 bg-green-500 text-white p-1 rounded"
              onClick={() => grantAccess(record.id, prompt("Enter provider address"))}
            >
              Grant Access
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PatientPortal;