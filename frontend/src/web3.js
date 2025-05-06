import Web3 from "web3";

const getWeb3 = async () => {
  if (window.ethereum) {
    const web3 = new Web3(window.ethereum);
    await window.ethereum.request({ method: "eth_requestAccounts" });
    return web3;
  } else {
    throw new Error("Please install MetaMask");
  }
};

const getContract = async (web3) => {
  const response = await fetch("/contracts/EHR.json");
  const contractData = await response.json();
  const networkId = await web3.eth.net.getId();
  const deployedNetwork = contractData.networks[networkId];
  return new web3.eth.Contract(contractData.abi, deployedNetwork && deployedNetwork.address);
};

export { getWeb3, getContract };