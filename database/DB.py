from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL = "postgresql://zhanat:1@localhost/test"

engine = create_engine(URL)

Base = declarative_base()

Session = sessionmaker(engine)
