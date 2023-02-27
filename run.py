import SQS
import PIIMasking
import PDatabase
import configparser

if __name__ == "__main__":

    #### Load all the configs and sh file here #####
    config = configparser.ConfigParser()
    config.read('config.cfg')

    ### Load up sqs and get messages from queue ###
    # endpoint, queue_name, max_messages,aws_region,aws_access_key, aws_secret_key
    sqs = SQS(config['sqs']['endpoint'],config['sqs']['queue_name'],config['sqs']['max_messages'],
              config['aws']['aws_region'],config['aws']['aws_access_key_id'], config['aws']['aws_secret_access_key'])
    messages = sqs.return_messages()

    ### Encrypt messages ###
    masking_attribs = ['ip','device_id']
    pii_mask = PIIMasking(masking_attribs)
    encrypted_messages = pii_mask.encryptAttributes(messages)

    ### Feed the encrypted messages to the postgre database ###
    p_db = PDatabase(config['postgres']['username'],config['postgres']['password'],config['postgres']['host'])
    p_db.load_data_postgre(encrypted_messages)



