import re
import sys
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging
import pymysql
from dotenv import load_dotenv
load_dotenv()

#set path for data fetch and store
script_dir=os.path.dirname(os.path.abspath(__file__))
project_root=os.path.dirname(script_dir)
data_path=os.path.join(project_root,'data','employees.csv')
output_path=os.path.join(project_root,'data')

os.makedirs(output_path, exist_ok=True)

#logging for tracking every step in data processing
log_dir=os.path.join(project_root,".logs")
os.makedirs(log_dir, exist_ok=True)

log_file=os.path.join(log_dir,"validate_import_csv.log")

logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s - %(levelname)s - %(message)s",
      handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
      ]
)
logging.info("Logging is started")

#validating the email row by row using regex and seggregate in valid and invalid
email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

try:
      df=pd.read_csv(data_path)
      logging.info(f"Data loaded successfully")
except:
      logging.error("Error in loading data")
      sys.exit(1)

valid_rows=[]
invalid_rows=[]

for i,row in df.iterrows():
      email=str(row["email"]).strip()
      if email_pattern.match(email):
            valid_rows.append(row)
            logging.info(f"Email {email} is valid")
      else:
            invalid_rows.append(row)
            logging.info(f"Email {email} is invalid")

logging.info(f"total valid rows{len(valid_rows)} | total invalid_rows {len(invalid_rows)}")

#connecting the csv file to database
username=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
host=os.getenv("DB_HOST")
port=os.getenv("DB_PORT")
database=os.getenv("DB_NAME")

db_url=f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

try:
      engine=create_engine(db_url)
      connection=engine.connect()
      logging.info("Database connected successfully")
except SQLAlchemyError as e:
      logging.error("Error in connecting database")
      sys.exit(1)

if valid_rows:
      valid_df=pd.DataFrame(valid_rows)
      try:
            valid_df.to_sql("employees",con=engine,if_exists="append",index=False)
            logging.info("Data imported successfully")
      except SQLAlchemyError as e:
            logging.error("Error in importing data")
            sys.exit(1)
else:
      logging.warning("No valid rows found")

connection.close()
logging.info("Database connection closed.")

