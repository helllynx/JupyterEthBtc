from Bitcoin.transaction import keyUtils

private_key = 'ec798cf1eef765ba48d732ee93b1856e8b5fcbe75c9f3914e7f38d321c2d4168'

print(keyUtils.privateKeyToWif(private_key))
print(keyUtils.keyToAddr(private_key))
