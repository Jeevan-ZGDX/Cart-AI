"""
Smart Billing Engine Service
Handles cart calculations, tax, discounts, and bill generation
"""
from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.billing import BillingResponse, BillCalculation
from app.schemas.cart import CartItemResponse
from typing import List


class BillingService:
    """Service for billing calculations and cart management"""
    
    @staticmethod
    def calculate_cart_total(cart: Cart) -> BillCalculation:
        """
        Calculate total bill for a cart including tax and discounts
        """
        subtotal = 0.0
        tax_amount = 0.0
        item_count = 0
        
        for item in cart.items:
            item_subtotal = item.unit_price * item.quantity
            item_tax = item_subtotal * (item.tax_rate / 100.0)
            
            subtotal += item_subtotal
            tax_amount += item_tax
            item_count += item.quantity
        
        # Apply discount (if any)
        discount_amount = cart.discount_amount or 0.0
        
        # Final amount
        final_amount = subtotal + tax_amount - discount_amount
        
        return BillCalculation(
            subtotal=round(subtotal, 2),
            tax_amount=round(tax_amount, 2),
            discount_amount=round(discount_amount, 2),
            final_amount=round(max(0, final_amount), 2),
            item_count=item_count
        )
    
    @staticmethod
    def update_cart_billing(db: Session, cart: Cart) -> Cart:
        """
        Update cart billing totals
        """
        calculation = BillingService.calculate_cart_total(cart)
        
        cart.total_amount = calculation.subtotal
        cart.tax_amount = calculation.tax_amount
        cart.discount_amount = calculation.discount_amount
        cart.final_amount = calculation.final_amount
        
        db.commit()
        db.refresh(cart)
        
        return cart
    
    @staticmethod
    def add_item_to_cart(
        db: Session,
        cart: Cart,
        product_id: int,
        quantity: int = 1
    ) -> CartItem:
        """
        Add item to cart and update billing
        """
        # Get product
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")
        
        # Check if item already in cart
        existing_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        ).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
            existing_item.subtotal = existing_item.unit_price * existing_item.quantity
        else:
            # Create new cart item
            existing_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.price,
                tax_rate=product.tax_rate,
                subtotal=product.price * quantity
            )
            db.add(existing_item)
        
        db.commit()
        db.refresh(existing_item)
        
        # Update cart totals
        BillingService.update_cart_billing(db, cart)
        
        return existing_item
    
    @staticmethod
    def remove_item_from_cart(
        db: Session,
        cart: Cart,
        cart_item_id: int
    ) -> bool:
        """
        Remove item from cart and update billing
        """
        cart_item = db.query(CartItem).filter(
            CartItem.id == cart_item_id,
            CartItem.cart_id == cart.id
        ).first()
        
        if not cart_item:
            return False
        
        db.delete(cart_item)
        db.commit()
        
        # Update cart totals
        BillingService.update_cart_billing(db, cart)
        
        return True
    
    @staticmethod
    def update_item_quantity(
        db: Session,
        cart: Cart,
        cart_item_id: int,
        quantity: int
    ) -> CartItem:
        """
        Update item quantity in cart
        """
        if quantity <= 0:
            BillingService.remove_item_from_cart(db, cart, cart_item_id)
            return None
        
        cart_item = db.query(CartItem).filter(
            CartItem.id == cart_item_id,
            CartItem.cart_id == cart.id
        ).first()
        
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")
        
        cart_item.quantity = quantity
        cart_item.subtotal = cart_item.unit_price * quantity
        
        db.commit()
        db.refresh(cart_item)
        
        # Update cart totals
        BillingService.update_cart_billing(db, cart)
        
        return cart_item
    
    @staticmethod
    def get_billing_response(cart: Cart) -> BillingResponse:
        """
        Generate billing response with all details
        """
        calculation = BillingService.calculate_cart_total(cart)
        
        items = [
            CartItemResponse(
                id=item.id,
                product_id=item.product_id,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.unit_price,
                tax_rate=item.tax_rate,
                subtotal=item.subtotal,
                verified_by_ai=item.verified_by_ai,
                scan_verified=item.scan_verified,
                added_at=item.added_at
            )
            for item in cart.items
        ]
        
        return BillingResponse(
            cart_id=cart.id,
            session_id=cart.session_id,
            calculation=calculation,
            items=items,
            currency="USD"
        )
