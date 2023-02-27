from Crypto.Random import get_random_bytes
from Crypto import Random
from AESCipher import AESCipher
import os
import pickle

class PIIMasking:

    def __init__(self, masking_cols):
        self.masking_cols = masking_cols
        self.cipherDict = self.createCiphers(masking_cols)

    def generate_random_key(self):
        '''
        Generate unique random key for the attribute we want to encrypt
        :return: random byte stream of size 16
        '''
        return get_random_bytes(16)

    def createCiphers(self, masking_cols):
        '''
        Create the lookup table containing the cipher for each attribute we want to encrypt
        :param masking_cols: columns we want to create ciphers for
        :return: dictionary object of type {"Attribute" : AESCipher Object}
        '''

        ### If cipher object already exists, we load it
        cipherDict = None

        if os.path.exists("ciphers.pkl"):
            #### If ciphers already exist, load it up so that we do not generate new key for an
            #### already encyprted attribute
            cipherDict = pickle.load(open("ciphers.pkl","rb"))
            print("Loaded previously created ciphers !!!!!!")
        else:
            #### Create a new dictionary
            cipherDict = {}
            print("Created blank ciphers!")

        for col in masking_cols:
            #### If column is not in cipherDict, this means we have not created a corresponding
            #### cipher for this attribute. If column already exists, no need to create a new one
            if col not in cipherDict:
                print("Creating ciphers for the attribute : " + col )
                cipherDict[col] = AESCipher(self.generate_random_key())

        #### Dump the pickle file with the updated ciphers
        pickle.dump(cipherDict,open("ciphers.pkl","wb"))

        return cipherDict

    def encryptAttributes(self, messages):
        '''
        Encrypt attributes and return the new list of messages
        :param messages: list of all the messages recieved from sqs
        :return: list of messages with ip and device_id encrypted
        '''


        for message in messages:
            # Encypt attributes from every message and return the new list of messages
            for col in self.masking_cols:
                try:
                    message[col] = self.cipherDict[col].encrypt(message[col])
                except KeyError:
                    continue
        print("All messages encrypted !!!!")
        return messages