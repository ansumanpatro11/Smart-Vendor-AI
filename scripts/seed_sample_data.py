import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from backend import models
from decimal import Decimal

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, future=True)
Session = sessionmaker(bind=engine, future=True)

def seed():
    session = Session()
    # create sample vendor
    user = models.User(name='Demo Vendor', email='vendor@example.com', password_hash='$2b$12$KIX', role='vendor')
    session.add(user)
    session.commit()
    # products
    p1 = models.Product(name='Milk Packet', category='Dairy', price=25.00, cost_price=18.00, stock_quantity=100)
    p2 = models.Product(name='Bread', category='Bakery', price=20.00, cost_price=12.00, stock_quantity=80)
    session.add_all([p1,p2])
    session.commit()
    print('Seeded sample data')

if __name__ == '__main__':
    seed()
