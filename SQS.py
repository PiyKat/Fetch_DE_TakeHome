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
        return self.sqs.receive_message(QueueUrl=self.__queue_url, MaxNumberOfMessages=self.__max_messages)

    def return_messages(self):
        '''
        Function to return a list containing the information present in the "Body" attribute of the sqs response
        '''
        messages = []

        while True:
            ### We run this loop until we reach the break condition ###

            # Get n responses from the sqs queue
            response = self.__return_message_batch()

            try:
                ### We extract the "Body" attribute from each json object
                for message in response['Messages']:
                    data = json.loads(message["Body"])
                    if 'user_id' in data:
                        messages.append(data)

            except KeyError:
                #### If we encounter a keyError, it means there is no "body" in message which
                #### means there are no more messages present in the queue, so we can stop the queue
                break

            entries = [
                {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
                for msg in response['Messages']
            ]

            resp = self.sqs.delete_message_batch(QueueUrl=self.__queue_url,
                                                 Entries=entries)

            if len(resp['Successful']) != len(entries):
                raise RuntimeError(f"Failed to delete messages: entries={entries!r} resp={resp!r}")

        return messages