import mysql.connector
from os import environ
from dotenv import load_dotenv

load_dotenv()

# Connect to server
cnx = mysql.connector.connect(
    host=environ.get("DB_HOST"),
    port=environ.get("DB_PORT"),
    user=environ.get("DB_USER"),
    password=environ.get("DB_PASSWORD"),
    database=environ.get("DB_NAME"),
)