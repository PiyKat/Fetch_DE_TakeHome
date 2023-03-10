from SQS import SQS
from PIIMasking import PIIMasking
from PDatabase import PDatabase
import configparser

'''
volumes:
        - ./scripts/alter_table.sql:/docker-entrypoint-initdb.d/alter_table.sql
'''

if __name__ == "__main__":

    #### Load all the configs and sh file here #####
    config = configparser.ConfigParser()
    config.read('config.cfg')

    ### Load up sqs and get messages from queue ###
    # endpoint, queue_name, max_messages,aws_region,aws_access_key, aws_secret_key
    config.get('postgres', 'username')
    print("Loading the SHS message queue!!!")
    sqs = SQS(config.get('sqs','endpoint_url'),config.get('sqs','queue_name'),int(config.get('sqs','max_no_messages')),
              config.get('aws','aws_region'),config.get('aws','aws_access_key_id'), config.get('aws','aws_secret_access_key'))
    print("Retrieving messages from the queue")
    messages = sqs.return_messages()

    ### Encrypt messages ###
    print("Masking ip addresses and device ids !!!!")
    masking_attribs = ['ip','device_id']
    pii_mask = PIIMasking(masking_attribs)
    encrypted_messages = pii_mask.encryptAttributes(messages)

    ### Feed the encrypted messages to the postgre database ###
    print("Feeding encryped messages to the database!!!!")
    p_db = PDatabase(config.get('postgres','username'),config.get('postgres','password'),config.get('postgres','host'))
    p_db.loadData(encrypted_messages)



