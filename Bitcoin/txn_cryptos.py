from bitcoinutils.keys import P2pkhAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput

from Bitcoin.bitcoin_gate_api import BitcoinGate


def main():
    # always remember to setup the network
    setup('testnet')

    url = 'https://testgate.geniepay.io'

    api = BitcoinGate(url)

    address_from = 'mtQbvrrZd9kDLLNfJHaHHhu1t3jHx1c3Jh'
    address_to = 'mssTb1GWSotwnq4UVxhKashVhZLo1zLqEC'

    amount = 0.0000001

    fee_per_byte = 10

    utxo = api.get_utxo_by_amout(address_from, amount)

    txin = [TxInput(u['tx_hash'], u['tx_pos']) for u in utxo[0]]

    # create transaction output using P2PKH scriptPubKey (locking script)
    txout = TxOutput(amount, Script(['OP_DUP', 'OP_HASH160', P2pkhAddress(address_to).to_hash160(),
                                     'OP_EQUALVERIFY', 'OP_CHECKSIG']))

    change_addr = P2pkhAddress(address_from)

    # fee calculation
    change_txout = TxOutput(amount, change_addr.to_script_pub_key())  # this is dumb data, just for fee calculation

    tx = Transaction(txin, [txout, change_txout])

    calculated_fee = (fee_per_byte * (len(tx.serialize()) / 2)) / 10 ** 8

    # setup change out
    change_txout = TxOutput((utxo[1] - int((amount + calculated_fee) * 10 ** 8)) / 10 ** 8,
                            change_addr.to_script_pub_key())

    tx = Transaction(txin, [txout, change_txout])

    # print raw transaction
    print("\nRaw unsigned transaction:\n" + tx.serialize())

    # sign transaction
    sk = PrivateKey(secret_exponent=0x02ef7b9791c17f35bb7f18f46209c984dc8a0317813166e5c00e7c06af5bdb9b)

    from_addr = P2pkhAddress(address_from)
    sig = sk.sign_input(tx, 0, Script(['OP_DUP', 'OP_HASH160',
                                       from_addr.to_hash160(), 'OP_EQUALVERIFY',
                                       'OP_CHECKSIG']))

    pk = sk.get_public_key()
    pk = pk.to_hex()

    for t in txin:
        t.script_sig = Script([sig, pk])

    signed_tx = tx.serialize()

    print("\nRaw signed transaction:\n" + signed_tx)


if __name__ == "__main__":
    main()
