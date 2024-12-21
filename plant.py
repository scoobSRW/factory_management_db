from wsgi import app
from app.models.models import db, Employee, Product

with app.app_context():
    # sample employees
    employee1 = Employee(name="John Doe", position="Manager")
    employee2 = Employee(name="Jane Smith", position="Engineer")

    # sample products
    product1 = Product(name="Widget A", price=15.99)
    product2 = Product(name="Widget B", price=25.50)

    db.session.add_all([employee1, employee2, product1, product2])
    db.session.commit()
    print("Planted data successfully!")
