from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from model.db_connection import engine

base = declarative_base()
class Stats(base):
    __tablename__ = "machines"
    ip = Column(String(255), primary_key=True)
    port = Column(Integer)
    username = Column(String(255))
    mail = Column(String(255))
    cpu_uptime = Column(Float)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    # alert_type = Column(String(255))
    # alert_limit = Column(String(255))

base.metadata.create_all(engine)