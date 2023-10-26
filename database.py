import mysql.connector

# Configure your MySQL database connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root1234",
    "database": "hft_fitness"
}

db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()