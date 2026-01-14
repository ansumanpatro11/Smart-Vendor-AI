from backend.db.session import engine, Base, SessionLocal
from backend.models.models import Product
Base.metadata.create_all(bind=engine)
db = SessionLocal()
samples = [
    {'name':'Milk Packets','category':'Dairy','price':25.0,'cost_price':18.0,'stock_quantity':100},
    {'name':'Bread','category':'Bakery','price':20.0,'cost_price':12.0,'stock_quantity':50},
    {'name':'Biscuit','category':'Snacks','price':10.0,'cost_price':5.0,'stock_quantity':200},
]
for s in samples:
    p = Product(name=s['name'], category=s['category'], price=s['price'], cost_price=s['cost_price'], stock_quantity=s['stock_quantity'])
    db.add(p)
db.commit()
print('Seeded products')