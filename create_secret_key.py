import os
import binascii

# Generate a random 24-byte string
secret_key = binascii.hexlify(os.urandom(24)).decode()
print(secret_key)