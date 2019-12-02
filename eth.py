# Деривирует BTC и ETH адреса из фразы
# Показывает балансы табличкой
# Умеет делать переводы Mainnet BTC и ETH c одного адреса на другой (через gBTC сервер)
from typing import List

from web3 import Web3

from crypto_eth import HDPrivateKey, HDKey

master_key = HDPrivateKey.master_key_from_mnemonic(
    'trade icon company use feature fee order double inhale gift news long')
root_keys = HDKey.from_path(master_key, "m/44'/60'/0'")
acct_priv_key = root_keys[-1]

private_keys = List[HDPrivateKey]

# derivation example for Ethereum generate first 10 addresses
for i in range(10):
    keys = HDKey.from_path(acct_priv_key, '{change}/{index}'.format(change=0, index=i))
    private_key = keys[-1]
    public_key = private_key.public_key
    private_keys.append(private_key)
    print(f'Index {i}:')
    print(f'\tPrivate key (hex, compressed): {private_key._key.to_hex()}')
    print(f'\tAddress: {private_key.public_key.address()}')

# send Ethereum

# use infura endpoint
endpoint_url = 'wss://ropsten.infura.io/ws/ea2841e43f2c4f3bb00e54892e820864'

# setup connection
w3 = Web3(Web3.WebsocketProvider(endpoint_url))
if not w3.isConnected():
    print('Can\'t connect WEB3 to endpoint')

# get current block
block = w3.eth.getBlock('latest')
print(f'Current block: {block}')

nonce = w3.eth.getTransactionCount(private_keys[0]._key.to_hex())

transaction = {
    'to': private_keys[1]._key.to_hex(),
    'value': 10000000,
    'gas': 2_000_000_000,
    'gasPrice': 100_000,
    'nonce': nonce,
    'chainId': 1
}

signed = w3.eth.account.sign_transaction(transaction, private_keys[0])

print(f'Signed transaction: {signed.rawTransaction}')

transaction_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

print(f'Transaction hash: {transaction_hash}')
