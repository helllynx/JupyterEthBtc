import requests


class BitcoinGate:

    def __init__(self, url):
        self.url = url

    def get_utxo_by_amout(self, address, amount):

        def utxo_calculation(values, amout):
            indexes = []
            total_value = 0
            for idx, val in enumerate(values):
                total_value += val
                indexes.append(idx)
                if total_value >= amout:
                    return indexes

            raise Exception(f'Not enough money: {total_value}')

        all_utxo = self.get_utxo(address)
        indexes = utxo_calculation([v['value'] for v in all_utxo], amount)

        return [[all_utxo[i] for i in indexes], sum([all_utxo[i]['value'] for i in indexes])]

    def get_utxo(self, address):
        return requests.get(f'{self.url}/{address}/utxo').json()

    def send_raw_transaction(self, transaction):
        return requests.put(f'{self.url}/transactions', transaction).content.decode()

    def get_balance(self, address):
        return requests.get(f'{self.url}/{address}/balance')

    def get_fee(self):
        return requests.get(f'{self.url}/fee').json()

    def get_transaction(self, transaction_hash):
        return requests.get(f'{self.url}/transactions?hash={transaction_hash}').json()
