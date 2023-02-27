from Crypto.Random import get_random_bytes
from Crypto import Random
import AESCipher

class PIIMasking:

    def __init__(self, masking_cols):
        self.masking_cols = masking_cols
        self.cipherDict = self.createCiphers(masking_cols)

    def generate_random_key(self):
        '''
        Generate unique random key for the attribute we want to encrypt
        '''
        return get_random_bytes(16)

    def createCiphers(self, masking_cols):
        '''
        Create the lookup table containing the cipher for each attribute we want to encrypt
        '''
        cipherDict = {}
        for col in masking_cols:
            if col not in cipherDict:
                cipherDict[col] = AESCipher(self.generate_random_key())
        return cipherDict

    def encryptAttributes(self, messages):
        '''
        Encrypt attributes and retuen the new list of messages
        '''

        for message in messages:

            for col in self.masking_cols:
                try:
                    message[col] = self.cipherDict[col].encrypt(message[col])
                except KeyError:
                    continue

        return messages