#### Class to return list of messages retrieved from the SQS queue ####
import boto3
import json

# Create SQS client
AWS_REGION = "us-east-1"
endpoint_url = "http://localhost:4566/000000000000/"
queue_name = "login-queue"
max_no_messages = 10
ACCESS_KEY = "dummy_access_key"
SECRET_KEY = "dummy_secret_key"


class SQS:

    def __init__(self, endpoint, queue_name, max_messages):
        self.endpoint = endpoint
        self.queue_name = queue_name
        self.max_messages = max_messages
        self.sqs = boto3.client('sqs', region_name=AWS_REGION, endpoint_url=endpoint_url,
                                aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

    def __return_message_batch(self):
        return self.sqs.receive_message(QueueUrl=self.endpoint + self.queue_name, MaxNumberOfMessages=max_no_messages)

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
                    messages.append(json.loads(message["Body"]))
            except KeyError:
                #### If we encounter a keyError, it means there is no "body" in message which
                #### means there are no more meassages present in the queue, so we can stop the queue
                break

            entries = [
                {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
                for msg in response['Messages']
            ]

            resp = self.sqs.delete_message_batch(QueueUrl=endpoint_url + queue_name,
                                                 Entries=entries)  # aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY

            if len(resp['Successful']) != len(entries):
                raise RuntimeError(f"Failed to delete messages: entries={entries!r} resp={resp!r}")

        return messages

if __name__ == "__main__":

    sqs_obj = SQS(endpoint_url,queue_name,max_no_messages)
    messages = sqs_obj.return_messages()
    for message in messages:
        print(message)