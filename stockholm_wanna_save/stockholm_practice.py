import nacl.secret
import nacl.utils

# Encrypt the stuff
key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
box = nacl.secret.SecretBox(key)
with open("inp.txt", "rb") as f:
    message = f.read()
print("The message is: >>", message, end = "<<\n")
encrypted = box.encrypt(message, nonce=(1).to_bytes(24, 'little'))
with open("out.txt", "wb") as f:
    f.write(encrypted)

# Read the encripted stuff
with open("out.txt", "rb") as f:
    enc_message = f.read()
with open("key.key", "bw") as f:
    f.write(key)
with open("key.key", "br") as f:
    keyd = f.read()
box2 = nacl.secret.SecretBox(keyd)
decripted = box2.decrypt(enc_message)
print("The encrypted message is: >>", decripted, end="<<\n")
