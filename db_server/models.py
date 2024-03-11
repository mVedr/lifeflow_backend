from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        String, create_engine, func)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = "mysql+mysqlconnector://lifeflow:lifeflow@localhost/lifeflow"

engine = create_engine(db_url)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)

#USER

# Entity_Id

class User(Base):
    __tablename__ = 'users'
    name = Column(String)
    dob = Column(Date)
    email = Column(String,unique=True)
    phone_number = Column(String,unique=True)
    blood_group = Column(String)
    sex = Column(String)
    profile_url = Column(String)
    location = Column(String)
    
    transactions_sent = relationship('Transaction',  back_populates='sender',uselist=True)

    transactions_received = relationship('Transaction',  back_populates='receiver',uselist=True)

#HOSPITAL/BB
    
# Phone Numbers []
# Emails []
    
class Entity(Base):
    __tablename__ = 'entities'
    name = Column(String)
    location = Column(String)
    photo_url = Column(String)
    website_url = Column(String,unique=True) 
    reg_number = Column(String,unique=True)
    
    transactions = relationship('Transaction', back_populates='entity',uselist=True)
    
class Transaction(Base):
    __table_name__ = 'transactions'
    date_time = Column(DateTime,default=func.now())
    from_id = Column(Integer,ForeignKey('users.id')) 
    to_id = Column(Integer,ForeignKey('users.id')) 
    entity_id = Column(Integer, ForeignKey('entities.id'))
    volume = Column(String)

    sender = relationship('User',back_populates='transactions_sent')
    receiver = relationship('User',back_populates='transactions_received')
    entity = relationship('Entity', back_populates='transactions')