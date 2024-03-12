from models import Donor, Entity, User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()

u1 = session.query(User).where(User.id == 1).one()
print(f'{u1.name} , {u1.email}')

u2 = session.query(User).where(User.id ==7).one()
print(f'{u2.name} , {u2.email}')

u3 = session.query(User).where(User.id == 5).one()
print(f'{u3.name} , {u3.email}')

e1 = session.query(Entity).where(Entity.id == 3).one()
print(f'{e1.name} , {e1.primary_email}')

e2 = session.query(Entity).where(Entity.id == 5).one()
print(f'{e2.name} , {e2.primary_email}')

# d1 = Donor()
# d1.available_vol = "4"
# d1.user_info = u1
# d1.entity_info = e1

# session.add(d1)
# session.commit()

# print(f'''
# {d1.user_info.name} {d1.user_info.email}  ... d
# {d1.entity_info.name} {d1.entity_info.primary_email} ... e
#  ''')

# print(f'{e1.donors}')

r1 = u2
r2 = u3

# e2.waitlist.append(r1)
# e1.waitlist.append(r2)

# session.commit()

print(f'1 : waitlist: {e1.waitlist}  ... donors: {e1.donors}')

print(f'1 : waitlist: {e2.waitlist}  ... donors: {e2.donors}')