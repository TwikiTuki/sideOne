import base64, struct, hashlib, time, sys
from cryptography.fernet import Fernet
HEX_BASE = "0123456789ABCDEF"
def my_custom_hmac(key,  msg, hashf):
    while (len(key) < 64):
        key += b'\x00'

    while (len(msg) < 8):
        msg = b'\x00' + msg

    ipad = bytearray(len(key))
    opad = bytearray(len(key))
    for i in range(len(key)):
        ipad[i] = key[i] ^ 0x36
        opad[i] = key[i] ^ 0x5c
    midle_result = hashf()
    midle_result.update(ipad + msg)
    midle_result = midle_result.digest()
    result = hashf()
    result.update(opad + midle_result)
    result = result.digest()
    return (result)

def get_totp(hashf, secret = 'JZCVMRKSEBDU6TSBEBDUSVSFEBMU6VJAKVICATKBIRAUMS2LIFAQ===='):
    '''
        Generets a totp key aplaying the 32 base secret key  to ashf function
    '''
    key = base64.b16decode(secret, True)
    interval = int(time.time()/30) 
    msg = bytearray(8)
    for i in range(7, -1, -1):
        msg[i] = interval & 0xff
        interval = interval >> 8
    custom = my_custom_hmac(key, msg, hashf)
    # Cut the key to generate otp
    offset = custom[-1] & 0xf
    result = 0
    result += custom[offset] & 0x7f
    result = result << 8
    result += custom[offset + 1]
    result = result << 8
    result += custom[offset + 2]
    result = result << 8
    result += custom[offset + 3]
    result %= 1000000
    result = str(result)
    while(len(result) < 6):
        result = '0' + result
    return(result)

def make_key():
    '''
        Asks for a hexadecimal key longer than 64 characters.
        Stores the key in ft_otp.key.
        The key is encripted with a key which is stored in .encryptkey (not the ideal solution) 
    '''
    print("Making key")
    key = ""    
    while (len(key) < 64 or len([c for c in key if c not in HEX_BASE])):
        key = input("Introduce a 64 characters hexadecimal key: ")
        key = key.upper()
    encrypt_key = Fernet.generate_key()
    f = Fernet(encrypt_key)
    key = key.encode()
    encrypted = f.encrypt(key)
    try:
        encrypt_file = open(".encryptkey", 'w')    
    except Exception:
        print("Couldnt open key loader file")
        exit()
    try:
        key_file = open("ft_otp.key", 'w')
    except Exception:
        print("Couldnt open key file")
        close(encrypt_file)
        exit()
    encrypt_file.write(encrypt_key.decode())
    key_file.write(encrypted.decode())
    encrypt_file.close()
    key_file.close()
    
def get_key():
    try:
        encrypt_file = open(".encryptkey", 'r')    
    except Exception:
        print("Couldnt open key loader file")
        exit()
    try:
        key_file = open("ft_otp.key", 'r')
    except Exception:
        print("Couldnt open key file")
        encrypt_file.close()
        exit()
    decript_key = encrypt_file.read()
    f = Fernet(decript_key) 
    key = f.decrypt(key_file.read())
    encrypt_file.close()
    key_file.close()
    return (key)

if (__name__ == '__main__'):
    usage = '''
    hotp.py [-g | -k | -s]
    -g Generate new key
    -k Get new value
    -s Get values continiously
    '''
    if (len(sys.argv) != 2):
        print(usage)
        exit()
    if(sys.argv[1] == '-g'):
        make_key()
    if(sys.argv[1] == '-k'):
        key = get_key()
        print("Human key: ", base64.b16decode(key))
        print("Base16 key: ", key)
        print("Bse32 key: ", base64.b32encode(base64.b16decode(key)))
        totp = get_totp(hashlib.sha1, key)
        print("TOTP value: ", totp)
    if (sys.argv[1] == '-s'):
        key = get_key()
        print("Human key: ", base64.b16decode(key))
        print("Base16 key: ", key)
        print("Bse32 key: ", base64.b32encode(base64.b16decode(key)))
        totp = get_totp(hashlib.sha1, key)
        print()
        while (True): 
            print(" TOTP value: ", totp, end = '\r')
            time.sleep(30 - (time.time() % 30))
            totp = get_totp(hashlib.sha1, key)
