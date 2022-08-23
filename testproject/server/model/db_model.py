from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from .db_connection import engine

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

    def __repr__(self):
        return(f'<ip = {self.ip}, port = {self.port}, username = {self.username}, mail = '
                + f'{self.mail}, cpu_uptime = {self.cpu_uptime}, cpu_usage, memory_usage = {self.memory_usage}>')

base.metadata.create_all(engine)