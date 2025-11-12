from sqlalchemy import create_engine, text

# Replace with your actual credentials
USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
PORT = '3306'  # Default MySQL port

# Connect to MySQL server (but not a specific database yet)
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}")

# Establish the connection
connection = engine.connect()

# Create a new database (you can change 'new_database_name' to your desired database name)
database_name = 'paras_ads'
connection.execute(text(f"CREATE DATABASE {database_name}"))

# Print success message
print(f"Database '{database_name}' created successfully!")

# Close the connection
connection.close()
