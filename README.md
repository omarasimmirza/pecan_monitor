# pecan_monitor
Monitor client machine statistics using snmp. Use paramiko modules to communicate between server and client. Use pecan to set up restful api.

pip install python-dotenv

In the model folder, you will need to create a .env file and include the database credentials in this manner:
user = '{user in database}'
password = '{database password}'
server = '{the server to connect to}'
database = '{the database name}'