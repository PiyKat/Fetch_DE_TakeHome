#### Class to return list of messages retrieved from the SQS queue ####
import boto3
import json

class SQS:

    def __init__(self, endpoint, queue_name, max_messages,aws_region,aws_access_key, aws_secret_key):
        self.__queue_url = endpoint + queue_name
        self.__max_messages = max_messages
        self.sqs = boto3.client('sqs', region_name=aws_region, endpoint_url=endpoint,
                                aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

    def __return_message_batch(self):
        '''
        Return a batch of 'MaxNumberOfMessages' queue messages from SQS queue
        :return: List containing meesages from the queue
        '''
        return self.sqs.receive_message(QueueUrl=self.__queue_url, MaxNumberOfMessages=self.__max_messages)

    def return_messages(self):
        '''
        Function to return all the messages from the queue
        :return: list containing all the messages from the queue
        '''
        messages = []

        while True:

            # Get 'MaxNumberOfMessages' queue messages from the sqs queue
            response = self.__return_message_batch()

            try:
                ### Extract the "Body" attribute containing the data we need to feed to db
                for message in response['Messages']:
                    data = json.loads(message["Body"])
                    #### To filter out bad messages, we check if the message contains a 'user_id' attribute
                    #### If not, that means that is a bad response and we ignore it
                    if 'user_id' in data:
                        messages.append(data)
                    else:
                        print("Warning! Bad message revieved !!!!!")


            except KeyError:
                #### If we encounter a keyError, it means there is no "body" in message which
                #### means there are no more messages present in the queue, so we can stop the queue
                print("All messages successfully read!")
                break

            #### Below code is to delete messages we just read from the queue so that they are
            ### not read again.
            entries = [
                {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
                for msg in response['Messages']
            ]

            resp = self.sqs.delete_message_batch(QueueUrl=self.__queue_url,
                                                 Entries=entries)

            if len(resp['Successful']) != len(entries):
                raise RuntimeError(f"Failed to delete messages: entries={entries!r} resp={resp!r}")

        return messages