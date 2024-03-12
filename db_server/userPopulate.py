from datetime import date

from models import User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()

users = [
       User(
        name='Rahul Sharma',
        dob=date(1990, 5, 15),
        email='rahul@example.com',
        phone_number='1234567890',
        blood_group='O+',
        sex='Male',
        location='Delhi'
    ),
    User(
        name='Priya Patel',
        dob=date(1988, 7, 23),
        email='priya@example.com',
        phone_number='9876543210',
        blood_group='A-',
        sex='Female',
        location='Mumbai'
    ),
    User(
        name='Amit Kumar',
        dob=date(1995, 8, 12),
        email='amit@example.com',
        phone_number='7890123456',
        blood_group='B+',
        sex='Male',
        location='Kolkata'
    ),
    User(
        name='Neha Singh',
        dob=date(1992, 3, 8),
        email='neha@example.com',
        phone_number='3456789012',
        blood_group='AB-',
        sex='Female',
        location='Bangalore'
    ),
     User(
        name='Sunil Kapoor',
        dob=date(1978, 10, 2),
        email='sunil@gmail.com',
        phone_number='425266463463',
        blood_group='A+',
        sex='Male',
        location='Chennai'
    ),
    User(
        name='Seema Mehta',
        dob=date(1985, 1, 19),
        email='seema@yahoo.com',
        phone_number='5527688813',
        blood_group='B-',
        sex='Female',
        location='Hyderabad'
    ),
    User(
        name='Vikram Rao',
        dob=date(1999, 12, 31),
        email='vikram@intel.com',
        phone_number='19992131141',
        blood_group='O-',
        sex='Male',
        location='Pune'
    ),
    User(
        name='Pooja Desai',
        dob=date(1993, 6, 14),
        email='pooj123@gmail.com',
        phone_number='31142980242',
        blood_group='AB+',
        sex='Female',
        location='Ahmedabad'
    ),
    User(
        name='Suresh Iyer',
        dob=date(1982, 9, 27),
        email='s_anjali@nitw.ac.in',
        phone_number='19829271218',
        blood_group='B+',
        sex='Male',
        location='Jaipur'
    ),
    User(
        name='Anjali Joshi',
        dob=date(2000, 4, 5),
        email='anjali@nitw.ac.in',
        phone_number='20004540002',
        blood_group='A-',
        sex='Female',
        location='Lucknow'
    ),
]

session.add_all(users)
session.commit()

print(f'{users} added')