from datetime import date

from faker import Faker
from models import Entity, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()

faker = Faker()

entities = []
for _ in range(10):  
    entity = Entity(
        name=faker.company() + 'Hospital',
        location=faker.city(),
        photo_url=faker.image_url(),
        website_url=faker.url(),
        reg_number=faker.unique.ssn(),
        primary_ph_no=faker.phone_number(),
        secondary_ph_no=faker.phone_number(),
        primary_email=faker.email(),
        secondary_email=faker.email()
        
    )
    entities.append(entity)

session.add_all(entities)
session.commit()

print(f'{entities} were added')