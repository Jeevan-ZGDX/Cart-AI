"""
Seed data script for Smart Retail Cart database
Run this after creating the database tables
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.product import Product
from app.models.aisle import Aisle

# Create all tables
Base.metadata.create_all(bind=engine)

def seed_data():
    """Seed the database with initial data"""
    db: Session = SessionLocal()
    
    try:
        # Create aisles
        aisles_data = [
            {"name": "Aisle 1 - Fruits & Vegetables", "section": "A", "x_coordinate": 10.0, "y_coordinate": 10.0, "description": "Fresh fruits and vegetables"},
            {"name": "Aisle 2 - Dairy Products", "section": "B", "x_coordinate": 20.0, "y_coordinate": 10.0, "description": "Milk, cheese, yogurt"},
            {"name": "Aisle 3 - Bakery", "section": "C", "x_coordinate": 30.0, "y_coordinate": 10.0, "description": "Bread, pastries, cakes"},
            {"name": "Aisle 4 - Beverages", "section": "D", "x_coordinate": 40.0, "y_coordinate": 10.0, "description": "Soft drinks, juices, water"},
            {"name": "Aisle 5 - Snacks", "section": "E", "x_coordinate": 50.0, "y_coordinate": 10.0, "description": "Chips, cookies, crackers"},
            {"name": "Aisle 6 - Meat & Seafood", "section": "F", "x_coordinate": 10.0, "y_coordinate": 20.0, "description": "Fresh meat and seafood"},
            {"name": "Aisle 7 - Frozen Foods", "section": "G", "x_coordinate": 20.0, "y_coordinate": 20.0, "description": "Frozen meals and ice cream"},
            {"name": "Aisle 8 - Personal Care", "section": "H", "x_coordinate": 30.0, "y_coordinate": 20.0, "description": "Shampoo, soap, toothpaste"},
        ]
        
        aisles = {}
        for aisle_data in aisles_data:
            aisle = Aisle(**aisle_data)
            db.add(aisle)
            db.flush()
            aisles[aisle.section] = aisle
        
        # Create products
        products_data = [
            # Fruits & Vegetables
            {"sku": "PROD001", "barcode": "1234567890123", "name": "Organic Apples", "description": "Fresh organic red apples", "price": 4.99, "tax_rate": 8.0, "category": "Fruits", "aisle_id": aisles["A"].id, "rfid_tag_id": "RFID001", "stock_quantity": 100},
            {"sku": "PROD002", "barcode": "1234567890124", "name": "Bananas", "description": "Fresh yellow bananas", "price": 2.49, "tax_rate": 8.0, "category": "Fruits", "aisle_id": aisles["A"].id, "rfid_tag_id": "RFID002", "stock_quantity": 150},
            {"sku": "PROD003", "barcode": "1234567890125", "name": "Carrots", "description": "Fresh organic carrots", "price": 3.99, "tax_rate": 8.0, "category": "Vegetables", "aisle_id": aisles["A"].id, "rfid_tag_id": "RFID003", "stock_quantity": 80},
            {"sku": "PROD004", "barcode": "1234567890126", "name": "Tomatoes", "description": "Fresh red tomatoes", "price": 3.49, "tax_rate": 8.0, "category": "Vegetables", "aisle_id": aisles["A"].id, "rfid_tag_id": "RFID004", "stock_quantity": 120},
            
            # Dairy Products
            {"sku": "PROD005", "barcode": "1234567890127", "name": "Whole Milk", "description": "Fresh whole milk 1 gallon", "price": 4.29, "tax_rate": 8.0, "category": "Dairy", "aisle_id": aisles["B"].id, "rfid_tag_id": "RFID005", "stock_quantity": 200},
            {"sku": "PROD006", "barcode": "1234567890128", "name": "Cheddar Cheese", "description": "Sharp cheddar cheese 8oz", "price": 5.99, "tax_rate": 8.0, "category": "Dairy", "aisle_id": aisles["B"].id, "rfid_tag_id": "RFID006", "stock_quantity": 90},
            {"sku": "PROD007", "barcode": "1234567890129", "name": "Greek Yogurt", "description": "Plain Greek yogurt 32oz", "price": 6.49, "tax_rate": 8.0, "category": "Dairy", "aisle_id": aisles["B"].id, "rfid_tag_id": "RFID007", "stock_quantity": 75},
            
            # Bakery
            {"sku": "PROD008", "barcode": "1234567890130", "name": "White Bread", "description": "Fresh white bread loaf", "price": 2.99, "tax_rate": 8.0, "category": "Bakery", "aisle_id": aisles["C"].id, "rfid_tag_id": "RFID008", "stock_quantity": 60},
            {"sku": "PROD009", "barcode": "1234567890131", "name": "Chocolate Chip Cookies", "description": "Fresh baked cookies 12 pack", "price": 4.99, "tax_rate": 8.0, "category": "Bakery", "aisle_id": aisles["C"].id, "rfid_tag_id": "RFID009", "stock_quantity": 45},
            
            # Beverages
            {"sku": "PROD010", "barcode": "1234567890132", "name": "Coca Cola", "description": "Coca Cola 12 pack cans", "price": 6.99, "tax_rate": 8.0, "category": "Beverages", "aisle_id": aisles["D"].id, "rfid_tag_id": "RFID010", "stock_quantity": 180},
            {"sku": "PROD011", "barcode": "1234567890133", "name": "Orange Juice", "description": "Fresh orange juice 64oz", "price": 5.49, "tax_rate": 8.0, "category": "Beverages", "aisle_id": aisles["D"].id, "rfid_tag_id": "RFID011", "stock_quantity": 100},
            {"sku": "PROD012", "barcode": "1234567890134", "name": "Bottled Water", "description": "Purified water 24 pack", "price": 4.99, "tax_rate": 8.0, "category": "Beverages", "aisle_id": aisles["D"].id, "rfid_tag_id": "RFID012", "stock_quantity": 250},
            
            # Snacks
            {"sku": "PROD013", "barcode": "1234567890135", "name": "Potato Chips", "description": "Classic potato chips 10oz", "price": 4.49, "tax_rate": 8.0, "category": "Snacks", "aisle_id": aisles["E"].id, "rfid_tag_id": "RFID013", "stock_quantity": 120},
            {"sku": "PROD014", "barcode": "1234567890136", "name": "Chocolate Bar", "description": "Milk chocolate bar 3.5oz", "price": 2.99, "tax_rate": 8.0, "category": "Snacks", "aisle_id": aisles["E"].id, "rfid_tag_id": "RFID014", "stock_quantity": 200},
            
            # Meat & Seafood
            {"sku": "PROD015", "barcode": "1234567890137", "name": "Chicken Breast", "description": "Fresh chicken breast 1lb", "price": 7.99, "tax_rate": 8.0, "category": "Meat", "aisle_id": aisles["F"].id, "rfid_tag_id": "RFID015", "stock_quantity": 50},
            {"sku": "PROD016", "barcode": "1234567890138", "name": "Salmon Fillet", "description": "Fresh salmon fillet 1lb", "price": 12.99, "tax_rate": 8.0, "category": "Seafood", "aisle_id": aisles["F"].id, "rfid_tag_id": "RFID016", "stock_quantity": 30},
            
            # Frozen Foods
            {"sku": "PROD017", "barcode": "1234567890139", "name": "Frozen Pizza", "description": "Pepperoni pizza 12 inch", "price": 6.99, "tax_rate": 8.0, "category": "Frozen", "aisle_id": aisles["G"].id, "rfid_tag_id": "RFID017", "stock_quantity": 80},
            {"sku": "PROD018", "barcode": "1234567890140", "name": "Ice Cream", "description": "Vanilla ice cream 1.5qt", "price": 5.99, "tax_rate": 8.0, "category": "Frozen", "aisle_id": aisles["G"].id, "rfid_tag_id": "RFID018", "stock_quantity": 60},
            
            # Personal Care
            {"sku": "PROD019", "barcode": "1234567890141", "name": "Shampoo", "description": "Moisturizing shampoo 16oz", "price": 7.99, "tax_rate": 8.0, "category": "Personal Care", "aisle_id": aisles["H"].id, "rfid_tag_id": "RFID019", "stock_quantity": 90},
            {"sku": "PROD020", "barcode": "1234567890142", "name": "Toothpaste", "description": "Fluoride toothpaste 6oz", "price": 4.99, "tax_rate": 8.0, "category": "Personal Care", "aisle_id": aisles["H"].id, "rfid_tag_id": "RFID020", "stock_quantity": 150},
        ]
        
        for product_data in products_data:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        print("Seed data created successfully!")
        print(f"   - Created {len(aisles_data)} aisles")
        print(f"   - Created {len(products_data)} products")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding database...")
    seed_data()
