from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
user = os.environ.get("user")
password = os.environ.get("password")
server = os.environ.get("server")
database = os.environ.get("database")
engine = create_engine(f'mysql://{user}:{password}@{server}/{database}')
Session = sessionmaker(bind=engine)
session = Session()