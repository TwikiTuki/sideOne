
import hmac, base64, struct, hashlib, time
key = "secure key"
msg = "hello hotp"

h = hmac.new(kye, msg, hashlib.sha1).digest()
