# Fetch_DE_TakeHome
Solution to the take home assignment for the DE Engineering interview at Fetch
## Steps to run the application ##
1. Install the necessary python modules for the assignment
```
make pip-install
```
2. Install docker images
```
make docker-start
```
3. Run alter_table.sql file to convert "app_version" from integer to varchar
```
make alter-table
```
This step would require you to enter the password for the database

4. Initiate the process of extracting messages, encryption and data loading
```
make run
```

In order to check the results, we can type the following in the terminal:
```
psql -d postgres -U postgres -p 5432 -h localhost -W
```
After entering the password, we type the following
```
select COUNT(*) from user_logins;
```
You sould see 99 records in the database

## Code Structure ##

Our code consist of 5 python files

1. SQS.py which contains code to load SQS Queue object and retrieve messages from the queue. For this, I used Boto3 module in Python.
2. AESCipher.py which is used to create a cipher for AES Encryption of an attribute
3. PDatabase.py which contains code to feed encrypted messages to our database. I used psycopg for connecting and quering the database.

We also have the following files
1. alter_table.sql in the scripts folder which contains SQl statement to change datatype of "app_version" attribute.
2. docker-compose.yaml containing the docker config to be used by our application
3. config.cfg which contains all the config details for AWS, SQS and PostgreSQL Database

## PII Masking ##

For PII Masking, we wanted a method that would allow analysts to easily recognize duplicate values while securely hiding the infrmation.

1. We need some kind of encryption method where the same plaintext would produce the same result all the time. This is called deterministic
encryption. 
2. It's mentioned in the assignment that PII may be need to be recovered later on.

Based on the above criteria, I came up with two methods :

1. SHA256 hashing which is deterministic, but recovering original PII values is practically impossible unless we maintain a lookup table for every value in the table.
2. AES encryption with ECB mode, which is also deterministic, but unline hashing, requires us to only create a random key for each unique attribute we want to encrypt.

Ultimately, I went with the second one because it is more memory and space efficient.

### Answers ###

1. How will the application run in production?

    For production, I would want to 
    - dockerize the application instead of directly running a python script
    - Use module level logging to log any error or warning we get at any step of the pipeline
    - Create a log every time the application is run for easier debugging
   

2. What other components to add to make this production ready?
   1. Use Apache Airflow or any other orchestration tool for managing the whole pipeline
   2. Consider replacing postgreSQL with a cloud data warehouse as data grows.
   3. Have a highly secure cloud storage to store & retrieve ciphers when done using the application.


3. How can this application scale with growing dataset?
   1. Moving from postgreSQL to a cloud data warehouse as data grows.
   2. Use Spark for all data-preprocessing and data transformations.
   3. The current application works on batches of data, with growing data we may consider moving to streaming ETL.


4. How can PII be recovered later on?

    Since we are using key-based encryption, we can use the same key to decrypt our data. Please note that we have one unique key per attribute, so even if data grows, we don't need to recompute the key and can use the same cipher to encrypt/decrypt.


5. What are the assumptions you made?

   There was an error in our database where the "app_version" attribute table was assigned an integer type.
In the messages, it was of the form "x.x.x", where x is a number. I assume this was intentional and I was able to correct it with an SQL script.