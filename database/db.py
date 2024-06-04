import mysql.connector
from mysql.connector import Error
from settings import get_config


def create_connection():
    config = get_config()
    try:
        connection = mysql.connector.connect(
            host=config.get('DB_HOST'),
            user=config.get('DB_USER'),
            password=config.get('DB_PASSWORD'),
            database=config.get('DB_NAME')
        )
        if connection.is_connected():
            print(f"Connection to MySQL database '{config.get('DB_NAME')}' is successful")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
