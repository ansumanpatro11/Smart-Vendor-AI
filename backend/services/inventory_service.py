from backend.models.models import Product
def to_dict(p):
    return {'product_id': p.product_id, 'name': p.name, 'price': float(p.price), 'stock_quantity': p.stock_quantity}
class InventoryService:
    def add(self, p, db):
        prod = Product(name=p.name, category=p.category, price=p.price, cost_price=p.cost_price, stock_quantity=p.stock_quantity)
        db.add(prod); db.commit(); db.refresh(prod)
        return {'product_id': prod.product_id}
    def list(self, db):
        prods = db.query(Product).all()
        return [to_dict(p) for p in prods]
