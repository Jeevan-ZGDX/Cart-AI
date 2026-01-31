"""
Payment Simulation Service
Handles payment processing, QR code generation, and receipts
"""
import qrcode
import io
import base64
import uuid
import json
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.cart import Cart, CartStatus
from app.models.transaction import Transaction, TransactionItem, TransactionStatus, PaymentMethod
from app.models.product import Product
from app.schemas.payment import QRCodeResponse, PaymentResponse


class PaymentService:
    """Service for payment processing and simulation"""
    
    def generate_payment_qr(
        self,
        db: Session,
        cart_id: int
    ) -> QRCodeResponse:
        """
        Generate payment QR code for cart
        """
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            raise ValueError(f"Cart {cart_id} not found")
        
        if cart.status != CartStatus.ACTIVE:
            raise ValueError(f"Cart {cart_id} is not active")
        
        # Generate payment reference
        payment_reference = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        
        # Create payment data
        payment_data = {
            "cart_id": cart_id,
            "session_id": cart.session_id,
            "amount": cart.final_amount,
            "reference": payment_reference,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(payment_data))
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        # QR code expires in 10 minutes
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        return QRCodeResponse(
            qr_code_data=img_str,
            payment_reference=payment_reference,
            amount=cart.final_amount,
            expires_at=expires_at
        )
    
    def process_payment(
        self,
        db: Session,
        cart_id: int,
        payment_method: str,
        payment_reference: Optional[str] = None
    ) -> PaymentResponse:
        """
        Process payment for cart (simulated)
        """
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            raise ValueError(f"Cart {cart_id} not found")
        
        if cart.status != CartStatus.ACTIVE:
            raise ValueError(f"Cart {cart_id} is not active")
        
        if cart.final_amount <= 0:
            raise ValueError("Cart total is zero")
        
        # Generate transaction ID
        transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        
        # Create transaction
        transaction = Transaction(
            cart_id=cart_id,
            transaction_id=transaction_id,
            payment_method=PaymentMethod(payment_method),
            amount=cart.final_amount,
            status=TransactionStatus.COMPLETED,  # Simulated - always succeeds
            payment_reference=payment_reference or f"REF-{uuid.uuid4().hex[:8].upper()}",
            completed_at=datetime.utcnow()
        )
        
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
            transaction.items.append(transaction_item)
        
        # Generate receipt
        receipt_data = self._generate_receipt(cart, transaction)
        transaction.receipt_data = json.dumps(receipt_data)
        
        db.add(transaction)
        
        # Update cart status
        cart.status = CartStatus.PAID
        cart.paid_at = datetime.utcnow()
        
        db.commit()
        db.refresh(transaction)
        
        return PaymentResponse(
            transaction_id=transaction.transaction_id,
            cart_id=cart_id,
            payment_method=payment_method,
            amount=transaction.amount,
            status=transaction.status.value,
            payment_reference=transaction.payment_reference,
            receipt_data=receipt_data,
            completed_at=transaction.completed_at
        )
    
    def _generate_receipt(self, cart: Cart, transaction: Transaction) -> dict:
        """
        Generate receipt data
        """
        receipt = {
            "transaction_id": transaction.transaction_id,
            "session_id": cart.session_id,
            "date": transaction.completed_at.isoformat() if transaction.completed_at else datetime.utcnow().isoformat(),
            "items": [],
            "subtotal": cart.total_amount,
            "tax": cart.tax_amount,
            "discount": cart.discount_amount,
            "total": cart.final_amount,
            "payment_method": transaction.payment_method.value,
            "payment_reference": transaction.payment_reference
        }
        
        for item in transaction.items:
            receipt["items"].append({
                "product_name": item.product.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "tax_rate": item.tax_rate,
                "subtotal": item.subtotal
            })
        
        return receipt


# Global payment service instance
payment_service = PaymentService()
