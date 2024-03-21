from web3 import Web3
from eth_account import Account

# Connect to Ethereum node, Infura is used here as an example
infura_url = 'https://mainnet.infura.io/v3/your_infura_project_id'
web3 = Web3(Web3.HTTPProvider(infura_url))

# Make sure to replace 'your_private_key' with the actual private key
private_key = 'your_private_key'
account = Account.from_key(private_key)
sender_address = account.address

# Address of the recipient
recipient_address = 'recipient_ethereum_address'

# USDT contract address on Ethereum
usdt_contract_address = web3.toChecksumAddress('0xdAC17F958D2ee523a2206206994597C13D831ec7')

# ABI to interact with an ERC20 contract
# In a production code, ensure to use the complete ABI
erc20_abi = '''
[
    {
        "constant": true,
        "inputs": [{"name":"_owner", "type":"address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {"name":"_to", "type":"address"},
            {"name":"_value", "type":"uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]
'''
erc20_contract = web3.eth.contract(address=usdt_contract_address, abi=erc20_abi)

# Amount of USDT to send
# Remember that ERC-20 tokens can have different decimals, USDT has 6
amount = web3.toWei(10, 'mwei') #must be mwei,or you will lost many eth.important!important!important!

# Constructing the transaction
nonce = web3.eth.getTransactionCount(sender_address)
txn = erc20_contract.functions.transfer(recipient_address, amount).buildTransaction({
    'chainId': 1,
    'gas': 2000000,#important,if it is small,the transaction will not execute,but the gas fee will not back.important!important!important!
    'gasPrice': web3.toWei('50', 'gwei'), #if it's more,it will return back to you.and you can see the gasPrice in website https://etherscan.io/gastracker.now it is 39
    'nonce': nonce
})

# Signing the transaction
signed_txn = web3.eth.account.signTransaction(txn, private_key)

# Sending the transaction
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)  
print("Transaction hash:", txn_hash.hex())

# Ensure to use the correct network and real USDT contract ABI
