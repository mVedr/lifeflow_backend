from models import Donor, Entity, User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()

u1 = session.query(User).where(User.id == 10).one()
# print(f'{u1.name} , {u1.email}')

u2 = session.query(User).where(User.id ==8).one()
# print(f'{u2.name} , {u2.email}')

u3 = session.query(User).where(User.id == 5).one()
# print(f'{u3.name} , {u3.email}')

u4 = session.query(User).where(User.id == 2).one()

e1 = session.query(Entity).where(Entity.id == 1).one()
# # print(f'{e1.name} , {e1.primary_email}')

# # e2 = session.query(Entity).where(Entity.id == 5).one()
# # # print(f'{e2.name} , {e2.primary_email}')

u1.volumeRequiredWhileReceiving = 9
u1.verified = True

d1 = Donor()
d1.available_vol = 4
d1.user_info = u2
d1.entity_info = e1

d2 = Donor()
d2.available_vol = 2
d2.user_info = u3
d2.entity_info = e1

d3 = Donor()
d3.available_vol = 5
d3.user_info = u4
d3.entity_info = e1

session.add(d1)
session.add(d2)
session.add(d3)

e1.waitlist.append(u1)
e1.donors.append(d1)
e1.donors.append(d2)
e1.donors.append(d3)

session.commit()

print(f'1 : waitlist: {e1.waitlist}  ... donors: {e1.donors}')
