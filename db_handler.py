from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

db_user = config.get('database', 'db_user')
db_password = config.get('database', 'db_password')
db_host = config.get('database', 'db_host')
db_name = config.get('database', 'db_name')

#I have SQLITE, поэтому подключение не защищено, для postgresql будет выглядить так engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')
SQLALCHEMY_DATABASE_URL = "sqlite:///./Warehouse.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
