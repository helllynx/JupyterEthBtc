import binascii

from bitcoin import SelectParams
from bitcoin.core import CTransaction
from bitcoin.core import b2lx
from bitcoin.wallet import CBitcoinAddress

SelectParams('testnet')


def get_tx_from_hex(hex_):
    tx = CTransaction.deserialize(binascii.unhexlify(hex_))
    tx_id = b2lx(tx.GetTxid())

    outs = []
    for out in tx.vout:
        out_dict = {
            'address': str(
                CBitcoinAddress.from_scriptPubKey(out.scriptPubKey)
            ),
            'value': out.nValue
        }
        outs.append(out_dict)

    ins = []
    for input_ in tx.vin:
        ins.append(
            {
                "hash": b2lx(input_.prevout.hash),
                "index": input_.prevout.n
            }
        )

    return {
        'tx_hash': tx_id,
        'tx_out': outs,
        'tx_in': ins
    }
