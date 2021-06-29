# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
from bipwallet import wallet
from web3 import Web3
from eth_account import Account
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
import pprint

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
# YOUR CODE HERE
from constants import *

# connect to local ETH/ geth
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
 
# Create a function called `derive_wallets`
def derive_wallets(coin=BTC,mnemonic=mnemonic, depth=3):
    command = f'php ./derive -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {ETH:derive_wallets(coin=ETH),BTCTEST:derive_wallets(coin=BTCTEST)}
numderive = 3


# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
keys = {}
for coin in coins:
    keys[coin]= derive_wallets(mnemonic, coin, numderive=3)

eth_PrivateKey = keys["eth"][0]['privkey']
btc_PrivateKey = keys['btc-test'][0]['privkey']

print(json.dumps(eth_PrivateKey, indent=4, sort_keys=True))
print(json.dumps(btc_PrivateKey, indent=4, sort_keys=True))
print(json.dumps(keys, indent=4, sort_keys=True))

def priv_key_to_account(coin, priv_key):
    print(coin)
    print(priv_key)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin,account, recipient, amount):
    if coin == ETH: 
        gasEstimate = w3.eth.estimateGas(
            {"from":eth_acc.address, "to":recipient, "value": amount}
        )
        return { 
            "from": eth_acc.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(eth_acc.address)
        }
    
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])
# create a function to hold Ethereum 
eth_acc = priv_key_to_account(ETH, derive_wallets(mnemonic, ETH,5)[0]['privkey'])       

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_txn(coin,account,recipient, amount):
    txn = create_tx(coin, account, recipient, amount)
    if coin == ETH:
        signed_txn = eth_acc.sign_transaction(txn)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        tx_btctest = create_tx(coin, account, recipient, amount)
        signed_txn = account.sign_transaction(txn)
        print(signed_txn)
        return NetworkAPI.broadcast_tx_testnet(signed_txn)

# Test transaction


btc_acc = priv_key_to_account(BTCTEST,btc_PrivateKey)
create_tx(BTCTEST,btc_acc,"mzAVYRCct8qM4pKbUDPr6JJZeC3vsEDMsz", 0.1)
send_txn(BTCTEST,btc_acc,"mzAVYRCct8qM4pKbUDPr6JJZeC3vsEDMsz", 0.1)

#ETH Transaction
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/0x662541feec10852e7ec7179ad607366c51993142c467765223ba3f7715aed1b3"))
w3.isConnected()
w3.eth.getBalance("0x1445a2385fF2cd7A116F30a9d7d4C4871aA57D3a")
create_tx(ETH,eth_acc,"0x1445a2385fF2cd7A116F30a9d7d4C4871aA57D3a", 1000)
send_txn(ETH, eth_acc,"0x1445a2385fF2cd7A116F30a9d7d4C4871aA57D3a", 1000)
w3.eth.getBalance("0x1445a2385fF2cd7A116F30a9d7d4C4871aA57D3a")