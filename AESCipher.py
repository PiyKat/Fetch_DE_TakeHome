from Crypto.Cipher import AES
import base64

class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.__key = key         #hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw) ### Padded data ####
        cipher = AES.new(self.__key, AES.MODE_ECB)
        return base64.b64encode( cipher.encrypt(raw.encode()) )

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.__key, AES.MODE_ECB)
        return self._unpad( cipher.decrypt(enc) ).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

'''
if __name__ == "__main__":
    cipher_obj = AESCipher(get_random_bytes(16))
    print(cipher_obj.encrypt("ABC"))
'''