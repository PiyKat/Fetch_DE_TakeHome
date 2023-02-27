import base64
import psycopg
from datetime import datetime
import sys

class PDatabase:

    def __init__(self, username, pwd, host):  # ,db):
        self.__username = username
        self.__host = host
        self.__pwd = pwd

    def base64Decode(self, string):
        '''
        :param string: string for decoding
        :return: decoded string
        '''
        return base64.b64decode(string).decode('utf-8')

    def loadData(self, messages):
        '''
        Function to feed the encrypted messages to postgreSQL database
        :param messages: list of encrypted messages
        :return:
        '''
        if len(messages) == 0:
            print("Empty message list! Aborting the operation")
            sys.exit()

        # Connect to Postgres
        postgres_connection = psycopg.connect(
            user=self.base64Decode(self.__username),
            password=self.base64Decode(self.__pwd),
            host=self.base64Decode(self.__host)
        )

        # Feed all the messages to our postgresql
        cursor = postgres_connection.cursor()

        for message in messages:
            # If locale is None, we set it to "None" as local is varchar type
            if not message['locale']:
                message['locale'] = "None"

            # Create a timestamp for create_date attribute
            message['create_date'] = datetime.now().strftime("%Y-%m-%d")

            # Convert dictionary values to list
            message_values = list(message.values())

            # Execute the insert query & feed the messages to database
            cursor.execute("INSERT INTO user_logins ( \
                user_id, \
                app_version, \
                device_type, \
                masked_ip, \
                locale, \
                masked_device_id, \
                create_date \
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)", message_values)

            # Commit data to Postgres
            postgres_connection.commit()

        print("All rows written in the postgres file")
        # Close connection to Postgres
        postgres_connection.close()