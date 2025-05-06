from web3 import Web3
import json
import os

class BlockchainUtils:
    def __init__(self, eth_node_url, contract_address):
        self.w3 = Web3(Web3.HTTPProvider(eth_node_url))
        with open("blockchain/build/contracts/EHR.json") as f:
            contract_data = json.load(f)
        self.contract = self.w3.eth.contract(address=contract_address, abi=contract_data["abi"])
        self.account = self.w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

    def add_record(self, ipfs_hash, patient_address):
        tx = self.contract.functions.addRecord(ipfs_hash).buildTransaction({
            "from": self.account.address,
            "nonce": self.w3.eth.getTransactionCount(self.account.address),
            "gas": 2000000,
            "gasPrice": self.w3.toWei("50", "gwei")
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.privateKey)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def get_record(self, record_id, address):
        return self.contract.functions.getRecord(record_id).call({"from": address})