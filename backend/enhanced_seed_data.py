"""
Enhanced seed data script with more realistic fake data
Run this to populate the database with comprehensive test data
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.product import Product
from app.models.aisle import Aisle
from app.models.cart import Cart, CartItem, CartStatus
from app.models.transaction import Transaction, TransactionItem, TransactionStatus, PaymentMethod
from datetime import datetime, timedelta
import random

# Create all tables
Base.metadata.create_all(bind=engine)

def seed_data():
    """Seed the database with comprehensive test data"""
    db: Session = SessionLocal()
    
    try:
        # Check if aisles already exist
        existing_aisles = db.query(Aisle).all()
        aisles = {aisle.section: aisle for aisle in existing_aisles}
        
        # Create missing aisles
        aisles_data = [
            {"name": "Aisle 1 - Fruits & Vegetables", "section": "A", "x_coordinate": 10.0, "y_coordinate": 10.0, "description": "Fresh fruits and vegetables"},
            {"name": "Aisle 2 - Dairy Products", "section": "B", "x_coordinate": 20.0, "y_coordinate": 10.0, "description": "Milk, cheese, yogurt"},
            {"name": "Aisle 3 - Bakery", "section": "C", "x_coordinate": 30.0, "y_coordinate": 10.0, "description": "Bread, pastries, cakes"},
            {"name": "Aisle 4 - Beverages", "section": "D", "x_coordinate": 40.0, "y_coordinate": 10.0, "description": "Soft drinks, juices, water"},
            {"name": "Aisle 5 - Snacks", "section": "E", "x_coordinate": 50.0, "y_coordinate": 10.0, "description": "Chips, cookies, crackers"},
            {"name": "Aisle 6 - Meat & Seafood", "section": "F", "x_coordinate": 10.0, "y_coordinate": 20.0, "description": "Fresh meat and seafood"},
            {"name": "Aisle 7 - Frozen Foods", "section": "G", "x_coordinate": 20.0, "y_coordinate": 20.0, "description": "Frozen meals and ice cream"},
            {"name": "Aisle 8 - Personal Care", "section": "H", "x_coordinate": 30.0, "y_coordinate": 20.0, "description": "Shampoo, soap, toothpaste"},
            {"name": "Aisle 9 - Cleaning Supplies", "section": "I", "x_coordinate": 40.0, "y_coordinate": 20.0, "description": "Detergents, cleaners"},
            {"name": "Aisle 10 - Electronics", "section": "J", "x_coordinate": 50.0, "y_coordinate": 20.0, "description": "Batteries, cables"},
        ]
        
        for aisle_data in aisles_data:
            if aisle_data["section"] not in aisles:
                aisle = Aisle(**aisle_data)
                db.add(aisle)
                db.flush()
                aisles[aisle.section] = aisle
        
        # Check existing products
        existing_products = db.query(Product).all()
        if len(existing_products) >= 20:
            print(f"Products already exist ({len(existing_products)}), adding more...")
            products = existing_products
        else:
            products = existing_products
        
        # Create comprehensive products list (only new ones)
        products_data = [
            # Fruits & Vegetables (Aisle A)
            {"sku": "PROD001", "barcode": "1234567890123", "name": "Organic Apples", "description": "Fresh organic red apples 3lb bag", "price": 4.99, "tax_rate": 8.0, "category": "Fruits", "aisle_id": aisles["A"].id, "rfid_tag_id": "RFID001", "stock_quantity": 100},
            {"sku": "PROD002", "barcode": "1234567890124", "name": "Bananas", "description": "Fresh yellow bananas per lb", "price": 0.69, "tax_rate": 8.0, "category": "Fruits", "aisle_id": aisles["A"].id, "rfid_tag_id": "RFID002", "stock_quantity": 150},
            {"sku": "PROD003", "barcode": "1234567890125", "name": "Carrots", "description": "Fresh organic carrots 1lb", "price": 1.99, "tax_rate": 8.0, "category": "Vegetables", "aisle_id": aisles["A"].id, "rfid_tag_id": "RFID003", "stock_quantity": 80},
            {"sku": "PROD004", "barcode": "1234567890126", "name": "Tomatoes", "description": "Fresh red tomatoes 1lb", "price": 2.99, "tax_rate": 8.0, "category": "Vegetables", "aisle_id": aisles["A"].id, "rfid_tag_id": "RFID004", "stock_quantity": 120},
            {"sku": "PROD005", "barcode": "1234567890127", "name": "Strawberries", "description": "Fresh strawberries 1lb", "price": 3.99, "tax_rate": 8.0, "category": "Fruits", "aisle_id": aisles["A"].id, "rfid_tag_id": "RFID005", "stock_quantity": 60},
            {"sku": "PROD006", "barcode": "1234567890128", "name": "Spinach", "description": "Fresh baby spinach 10oz", "price": 2.49, "tax_rate": 8.0, "category": "Vegetables", "aisle_id": aisles["A"].id, "rfid_tag_id": "RFID006", "stock_quantity": 90},
            
            # Dairy Products (Aisle B)
            {"sku": "PROD007", "barcode": "1234567890129", "name": "Whole Milk", "description": "Fresh whole milk 1 gallon", "price": 4.29, "tax_rate": 8.0, "category": "Dairy", "aisle_id": aisles["B"].id, "rfid_tag_id": "RFID007", "stock_quantity": 200},
            {"sku": "PROD008", "barcode": "1234567890130", "name": "Cheddar Cheese", "description": "Sharp cheddar cheese 8oz", "price": 5.99, "tax_rate": 8.0, "category": "Dairy", "aisle_id": aisles["B"].id, "rfid_tag_id": "RFID008", "stock_quantity": 90},
            {"sku": "PROD009", "barcode": "1234567890131", "name": "Greek Yogurt", "description": "Plain Greek yogurt 32oz", "price": 6.49, "tax_rate": 8.0, "category": "Dairy", "aisle_id": aisles["B"].id, "rfid_tag_id": "RFID009", "stock_quantity": 75},
            {"sku": "PROD010", "barcode": "1234567890132", "name": "Butter", "description": "Unsalted butter 1lb", "price": 4.99, "tax_rate": 8.0, "category": "Dairy", "aisle_id": aisles["B"].id, "rfid_tag_id": "RFID010", "stock_quantity": 110},
            {"sku": "PROD011", "barcode": "1234567890133", "name": "Eggs", "description": "Large eggs 12 count", "price": 3.49, "tax_rate": 8.0, "category": "Dairy", "aisle_id": aisles["B"].id, "rfid_tag_id": "RFID011", "stock_quantity": 180},
            
            # Bakery (Aisle C)
            {"sku": "PROD012", "barcode": "1234567890134", "name": "White Bread", "description": "Fresh white bread loaf", "price": 2.99, "tax_rate": 8.0, "category": "Bakery", "aisle_id": aisles["C"].id, "rfid_tag_id": "RFID012", "stock_quantity": 60},
            {"sku": "PROD013", "barcode": "1234567890135", "name": "Chocolate Chip Cookies", "description": "Fresh baked cookies 12 pack", "price": 4.99, "tax_rate": 8.0, "category": "Bakery", "aisle_id": aisles["C"].id, "rfid_tag_id": "RFID013", "stock_quantity": 45},
            {"sku": "PROD014", "barcode": "1234567890136", "name": "Bagels", "description": "Fresh bagels 6 pack", "price": 3.99, "tax_rate": 8.0, "category": "Bakery", "aisle_id": aisles["C"].id, "rfid_tag_id": "RFID014", "stock_quantity": 50},
            {"sku": "PROD015", "barcode": "1234567890137", "name": "Croissants", "description": "Butter croissants 4 pack", "price": 5.99, "tax_rate": 8.0, "category": "Bakery", "aisle_id": aisles["C"].id, "rfid_tag_id": "RFID015", "stock_quantity": 40},
            
            # Beverages (Aisle D)
            {"sku": "PROD016", "barcode": "1234567890138", "name": "Coca Cola", "description": "Coca Cola 12 pack cans", "price": 6.99, "tax_rate": 8.0, "category": "Beverages", "aisle_id": aisles["D"].id, "rfid_tag_id": "RFID016", "stock_quantity": 180},
            {"sku": "PROD017", "barcode": "1234567890139", "name": "Orange Juice", "description": "Fresh orange juice 64oz", "price": 5.49, "tax_rate": 8.0, "category": "Beverages", "aisle_id": aisles["D"].id, "rfid_tag_id": "RFID017", "stock_quantity": 100},
            {"sku": "PROD018", "barcode": "1234567890140", "name": "Bottled Water", "description": "Purified water 24 pack", "price": 4.99, "tax_rate": 8.0, "category": "Beverages", "aisle_id": aisles["D"].id, "rfid_tag_id": "RFID018", "stock_quantity": 250},
            {"sku": "PROD019", "barcode": "1234567890141", "name": "Coffee", "description": "Ground coffee 12oz", "price": 8.99, "tax_rate": 8.0, "category": "Beverages", "aisle_id": aisles["D"].id, "rfid_tag_id": "RFID019", "stock_quantity": 70},
            {"sku": "PROD020", "barcode": "1234567890142", "name": "Energy Drink", "description": "Energy drink 4 pack", "price": 7.99, "tax_rate": 8.0, "category": "Beverages", "aisle_id": aisles["D"].id, "rfid_tag_id": "RFID020", "stock_quantity": 120},
            
            # Snacks (Aisle E)
            {"sku": "PROD021", "barcode": "1234567890143", "name": "Potato Chips", "description": "Classic potato chips 10oz", "price": 4.49, "tax_rate": 8.0, "category": "Snacks", "aisle_id": aisles["E"].id, "rfid_tag_id": "RFID021", "stock_quantity": 120},
            {"sku": "PROD022", "barcode": "1234567890144", "name": "Chocolate Bar", "description": "Milk chocolate bar 3.5oz", "price": 2.99, "tax_rate": 8.0, "category": "Snacks", "aisle_id": aisles["E"].id, "rfid_tag_id": "RFID022", "stock_quantity": 200},
            {"sku": "PROD023", "barcode": "1234567890145", "name": "Trail Mix", "description": "Mixed nuts and dried fruit 16oz", "price": 6.99, "tax_rate": 8.0, "category": "Snacks", "aisle_id": aisles["E"].id, "rfid_tag_id": "RFID023", "stock_quantity": 85},
            {"sku": "PROD024", "barcode": "1234567890146", "name": "Granola Bars", "description": "Oats and honey granola bars 12 pack", "price": 5.99, "tax_rate": 8.0, "category": "Snacks", "aisle_id": aisles["E"].id, "rfid_tag_id": "RFID024", "stock_quantity": 95},
            
            # Meat & Seafood (Aisle F)
            {"sku": "PROD025", "barcode": "1234567890147", "name": "Chicken Breast", "description": "Fresh chicken breast 1lb", "price": 7.99, "tax_rate": 8.0, "category": "Meat", "aisle_id": aisles["F"].id, "rfid_tag_id": "RFID025", "stock_quantity": 50},
            {"sku": "PROD026", "barcode": "1234567890148", "name": "Salmon Fillet", "description": "Fresh salmon fillet 1lb", "price": 12.99, "tax_rate": 8.0, "category": "Seafood", "aisle_id": aisles["F"].id, "rfid_tag_id": "RFID026", "stock_quantity": 30},
            {"sku": "PROD027", "barcode": "1234567890149", "name": "Ground Beef", "description": "Lean ground beef 1lb", "price": 6.99, "tax_rate": 8.0, "category": "Meat", "aisle_id": aisles["F"].id, "rfid_tag_id": "RFID027", "stock_quantity": 65},
            {"sku": "PROD028", "barcode": "1234567890150", "name": "Pork Chops", "description": "Fresh pork chops 1lb", "price": 8.99, "tax_rate": 8.0, "category": "Meat", "aisle_id": aisles["F"].id, "rfid_tag_id": "RFID028", "stock_quantity": 45},
            
            # Frozen Foods (Aisle G)
            {"sku": "PROD029", "barcode": "1234567890151", "name": "Frozen Pizza", "description": "Pepperoni pizza 12 inch", "price": 6.99, "tax_rate": 8.0, "category": "Frozen", "aisle_id": aisles["G"].id, "rfid_tag_id": "RFID029", "stock_quantity": 80},
            {"sku": "PROD030", "barcode": "1234567890152", "name": "Ice Cream", "description": "Vanilla ice cream 1.5qt", "price": 5.99, "tax_rate": 8.0, "category": "Frozen", "aisle_id": aisles["G"].id, "rfid_tag_id": "RFID030", "stock_quantity": 60},
            {"sku": "PROD031", "barcode": "1234567890153", "name": "Frozen Vegetables", "description": "Mixed frozen vegetables 16oz", "price": 3.99, "tax_rate": 8.0, "category": "Frozen", "aisle_id": aisles["G"].id, "rfid_tag_id": "RFID031", "stock_quantity": 100},
            
            # Personal Care (Aisle H)
            {"sku": "PROD032", "barcode": "1234567890154", "name": "Shampoo", "description": "Moisturizing shampoo 16oz", "price": 7.99, "tax_rate": 8.0, "category": "Personal Care", "aisle_id": aisles["H"].id, "rfid_tag_id": "RFID032", "stock_quantity": 90},
            {"sku": "PROD033", "barcode": "1234567890155", "name": "Toothpaste", "description": "Fluoride toothpaste 6oz", "price": 4.99, "tax_rate": 8.0, "category": "Personal Care", "aisle_id": aisles["H"].id, "rfid_tag_id": "RFID033", "stock_quantity": 150},
            {"sku": "PROD034", "barcode": "1234567890156", "name": "Soap", "description": "Antibacterial soap 3 pack", "price": 3.99, "tax_rate": 8.0, "category": "Personal Care", "aisle_id": aisles["H"].id, "rfid_tag_id": "RFID034", "stock_quantity": 130},
            
            # Cleaning Supplies (Aisle I)
            {"sku": "PROD035", "barcode": "1234567890157", "name": "Laundry Detergent", "description": "Liquid laundry detergent 100oz", "price": 12.99, "tax_rate": 8.0, "category": "Cleaning", "aisle_id": aisles["I"].id, "rfid_tag_id": "RFID035", "stock_quantity": 70},
            {"sku": "PROD036", "barcode": "1234567890158", "name": "Dish Soap", "description": "Dishwashing liquid 24oz", "price": 3.99, "tax_rate": 8.0, "category": "Cleaning", "aisle_id": aisles["I"].id, "rfid_tag_id": "RFID036", "stock_quantity": 110},
            
            # Electronics (Aisle J)
            {"sku": "PROD037", "barcode": "1234567890159", "name": "AA Batteries", "description": "Alkaline AA batteries 8 pack", "price": 9.99, "tax_rate": 8.0, "category": "Electronics", "aisle_id": aisles["J"].id, "rfid_tag_id": "RFID037", "stock_quantity": 140},
            {"sku": "PROD038", "barcode": "1234567890160", "name": "USB Cable", "description": "USB-C charging cable 6ft", "price": 12.99, "tax_rate": 8.0, "category": "Electronics", "aisle_id": aisles["J"].id, "rfid_tag_id": "RFID038", "stock_quantity": 55},
        ]
        
        # Add only new products that don't exist
        existing_barcodes = {p.barcode for p in existing_products}
        new_products = []
        for product_data in products_data:
            if product_data["barcode"] not in existing_barcodes:
                product = Product(**product_data)
                db.add(product)
                db.flush()
                new_products.append(product)
        
        # Combine existing and new products
        all_products = list(existing_products) + new_products
        products = all_products if all_products else existing_products
        
        # Create some fake completed transactions for analytics
        print("Creating fake transactions...")
        for i in range(15):  # Create 15 fake transactions
            cart = Cart(
                session_id=f"FAKE-CART-{i+1:03d}",
                status=CartStatus.PAID,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 7)),
                paid_at=datetime.utcnow() - timedelta(days=random.randint(1, 7)),
                total_amount=0,
                tax_amount=0,
                final_amount=0
            )
            db.add(cart)
            db.flush()
            
            # Add random items to cart
            num_items = random.randint(3, 8)
            selected_products = random.sample(products, min(num_items, len(products)))
            cart_total = 0
            cart_tax = 0
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                subtotal = product.price * quantity
                tax = subtotal * (product.tax_rate / 100.0)
                cart_total += subtotal
                cart_tax += tax
                
                cart_item = CartItem(
                    cart_id=cart.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price,
                    tax_rate=product.tax_rate,
                    subtotal=subtotal,
                    verified_by_ai=True,
                    scan_verified=True
                )
                db.add(cart_item)
            
            cart.total_amount = cart_total
            cart.tax_amount = cart_tax
            cart.final_amount = cart_total + cart_tax
            
            # Create transaction
            transaction = Transaction(
                cart_id=cart.id,
                transaction_id=f"TXN-{datetime.utcnow().strftime('%Y%m%d')}-{i+1:04d}",
                payment_method=random.choice(list(PaymentMethod)),
                amount=cart.final_amount,
                status=TransactionStatus.COMPLETED,
                payment_reference=f"REF-{random.randint(100000, 999999)}",
                completed_at=cart.paid_at
            )
            db.add(transaction)
            db.flush()
            
            # Create transaction items
            for cart_item in cart.items:
                transaction_item = TransactionItem(
                    transaction_id=transaction.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.unit_price,
                    tax_rate=cart_item.tax_rate,
                    subtotal=cart_item.subtotal
                )
                db.add(transaction_item)
        
        db.commit()
        print("Seed data created successfully!")
        print(f"   - Created {len(aisles_data)} aisles")
        print(f"   - Created {len(products_data)} products")
        print(f"   - Created 15 fake transactions for analytics")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding database with enhanced data...")
    seed_data()
