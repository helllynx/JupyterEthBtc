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
                if total_value >= amout:
                    indexes.append(idx)
                    return indexes
            raise Exception(f'Not enough money: {total_value}')

        all_utxo = requests.get(f'{self.url}/{address}/utxo').json()
        indexes = utxo_calculation(sorted([v['value'] for v in all_utxo]), amount)

        return [[all_utxo[i] for i in indexes], sum([all_utxo[i]['value'] for i in indexes])]

    def send_raw_transaction(self, transaction):
        return requests.put(f'{self.url}/transactions', transaction).content.decode()

    def get_fee(self):
        return requests.get(f'{self.url}/fee').json()