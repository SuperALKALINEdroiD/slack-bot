from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    channelid = Column(String)
    joining_time = Column(DateTime)
    next_message_time_string = Column(String)
    next_message_time = Column(DateTime)
