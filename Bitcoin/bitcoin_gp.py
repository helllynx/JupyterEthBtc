from enum import Enum

from bitcoin_gp_gate import BitcoinGate
from bitcoinutils.keys import P2pkhAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput


# from Bitcoin.bitcoin_gp_gate import BitcoinGate


class Fee(Enum):
    SLOW = 'min'
    AVERAGE = 'median'
    FAST = 'max'


class BitcoinGP:
    decimals = 10 ** 8

    def __init__(self, gate_url: str, main_net=True):
        self._api = BitcoinGate(gate_url)

        if main_net:
            setup('mainnet')
        else:
            setup('testnet')

    def get_balance(self, address):
        balance = self._api.get_balance(address)
        if balance:
            return balance.json()
        raise Exception('Can\'t retrieve balance')

    def build_transaction(self, private_key: str, address_from: str, address_to: str, amount: float, fee: Fee):
        fee_per_byte = self._api.get_fee()[fee.value]
        utxo = self._api.get_utxo_by_amout(address_from, amount)
        transaction_inputs = [TxInput(u['tx_hash'], u['tx_pos']) for u in utxo[0]]

        # create transaction output using P2PKH scriptPubKey (locking script)
        transaction_output = TxOutput(amount, Script(['OP_DUP', 'OP_HASH160', P2pkhAddress(address_to).to_hash160(),
                                                      'OP_EQUALVERIFY', 'OP_CHECKSIG']))
        change_address = P2pkhAddress(address_from)

        # fee calculation
        change_transaction_output = TxOutput(amount,
                                             change_address.to_script_pub_key())  # this is dumb data, just for fee calculation

        transaction = Transaction(transaction_inputs, [transaction_output, change_transaction_output])

        calculated_fee = (fee_per_byte * (len(transaction.serialize()) / 2)) / 10 ** 8

        # setup change out
        change_transaction_output = TxOutput((utxo[1] - int((amount * 10 ** 8 + calculated_fee * 10 ** 8))) / 10 ** 8,
                                             change_address.to_script_pub_key())
        transaction = Transaction(transaction_inputs, [transaction_output, change_transaction_output])
        # sign transaction
        signing_key = PrivateKey(secret_exponent=int(private_key, 16))
        from_address = P2pkhAddress(address_from)
        sig = signing_key.sign_input(transaction, 0, Script(['OP_DUP', 'OP_HASH160',
                                                             from_address.to_hash160(), 'OP_EQUALVERIFY',
                                                             'OP_CHECKSIG']))
        pk = signing_key.get_public_key().to_hex()

        for t in transaction_inputs:
            t.script_sig = Script([sig, pk])

        return transaction.serialize()

    def send_transaction(self, signed_transaction):
        return self._api.send_raw_transaction(signed_transaction)

    def build_transaction_all_assets_to_address(self, private_key: str, address_from: str, address_to: str, fee: Fee):
        # get address_from balance and send all bitcoins to address_to
        # transaction output contains just one output, without change output

        balance = self.get_balance(address_from)
        balance = balance['confirmed'] + balance['unconfirmed']
        fee_per_byte = self._api.get_fee()[fee.value]
        utxo = self._api.get_utxo_by_amout(address_from, balance)
        transaction_inputs = [TxInput(u['tx_hash'], u['tx_pos']) for u in utxo[0]]
        transaction_output = TxOutput(balance / self.decimals,
                                      Script(['OP_DUP', 'OP_HASH160', P2pkhAddress(address_to).to_hash160(),
                                              'OP_EQUALVERIFY', 'OP_CHECKSIG']))

        transaction = Transaction(transaction_inputs, [transaction_output])

        calculated_fee = (fee_per_byte * (len(transaction.serialize()) / 2))

        amount = balance / self.decimals - calculated_fee / self.decimals
        amount = round(amount, 8)

        transaction_output = TxOutput(amount, Script(['OP_DUP', 'OP_HASH160', P2pkhAddress(address_to).to_hash160(),
                                                      'OP_EQUALVERIFY', 'OP_CHECKSIG']))

        transaction = Transaction(transaction_inputs, [transaction_output])

        signing_key = PrivateKey(secret_exponent=int(private_key, 16))
        from_address = P2pkhAddress(address_from)
        sig = signing_key.sign_input(transaction, 0, Script(['OP_DUP', 'OP_HASH160',
                                                             from_address.to_hash160(), 'OP_EQUALVERIFY',
                                                             'OP_CHECKSIG']))
        pk = signing_key.get_public_key().to_hex()

        for t in transaction_inputs:
            t.script_sig = Script([sig, pk])

        return transaction.serialize()
