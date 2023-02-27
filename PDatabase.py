import base64
import psycopg
from datetime import datetime
import sys

class PDatabase:

    def __init__(self, username, pwd, host):  # ,db):
        self.__username = username
        self.__host = host
        # self.__db = db
        self.__pwd = pwd

    def base64Decode(self, string):
        return base64.b64decode(string).decode('utf-8')

    def load_data_postgre(self, messages):
        """Function to load data to postgres"""

        # Check if "message_list" is empty
        if len(messages) == 0:
            print("Error - " + str(TypeError))
            sys.exit()

        # Connect to Postgres
        ### decode this from base64 when you feed credentials from make
        postgres_connection = psycopg.connect(
            # host = self.base64Decode(self.__host),
            # database = self.base64Decode(self.__db),
            user=self.base64Decode(self.__username),
            password=self.base64Decode(self.__pwd),
            host=self.base64Decode(self.__host)
        )

        # Create a Cursor
        cursor = postgres_connection.cursor()

        # Iterate through messages
        for message in messages:
            # Replaced 'None Type' values with 'None' string
            message['locale'] = 'None' if message['locale'] == None else message['locale']
            # Set 'create_date' field as current date
            message['create_date'] = datetime.now().strftime("%Y-%m-%d")

            # Convert dictionary values to list
            values = list(message.values())

            # Execute the insert query
            cursor.execute("INSERT INTO user_logins ( \
                user_id, \
                app_version, \
                device_type, \
                masked_ip, \
                locale, \
                masked_device_id, \
                create_date \
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)", values)

            # Commit data to Postgres
            postgres_connection.commit()

        print("All rows written in the postgres file")
        # Close connection to Postgres
        postgres_connection.close()