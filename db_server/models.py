from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        String, create_engine, func)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = "mysql+mysqlconnector://lifeflow:lifeflow@127.0.0.1:3307/lifeflow"

engine = create_engine(db_url)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)

#USER
class User(BaseModel):
    __tablename__ = 'users'
    name = Column(String(255))
    dob = Column(Date)
    email = Column(String(255), unique=True)
    phone_number = Column(String(255), unique=True)
    blood_group = Column(String(255))
    sex = Column(String(255))
    profile_url = Column(String(255))
    location = Column(String(255))
    verified = Column(Boolean)
    
    transactions_sent = relationship('Transaction', foreign_keys='Transaction.from_id', back_populates='sender', uselist=True)
    transactions_received = relationship('Transaction', foreign_keys='Transaction.to_id', back_populates='receiver', uselist=True)

#HOSPITAL/BB
class Entity(BaseModel):
    __tablename__ = 'entities'
    name = Column(String(255))
    location = Column(String(255))
    photo_url = Column(String(255))
    website_url = Column(String(255)) 
    reg_number = Column(String(255), unique=True)
    primary_ph_no = Column(String(255), unique=True)
    secondary_ph_no = Column(String(255))
    primary_email = Column(String(255), unique=True)
    secondary_email = Column(String(255))
    transactions = relationship('Transaction', back_populates='entity',uselist=True)
    
#TRANSACTION
class Transaction(BaseModel):
    __tablename__ = 'transactions'
    date_time = Column(DateTime, default=func.now())
    from_id = Column(Integer, ForeignKey('users.id'))
    to_id = Column(Integer, ForeignKey('users.id'))
    entity_id = Column(Integer, ForeignKey('entities.id'))
    volume = Column(String(255))

    sender = relationship('User', foreign_keys=[from_id], back_populates='transactions_sent', uselist=False)
    receiver = relationship('User', foreign_keys=[to_id], back_populates='transactions_received', uselist=False)
    entity = relationship('Entity', back_populates='transactions', uselist=False)

Base.metadata.create_all(engine)