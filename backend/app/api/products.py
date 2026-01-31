"""
Product API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductResponse, ProductSearch
from app.schemas.cart import CartItemCreate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
def search_products(
    query: str = Query(..., description="Search query (name, barcode, SKU, or category)"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search products by name, barcode, SKU, or category
    """
    search_term = f"%{query.lower()}%"
    
    products = db.query(Product).filter(
        (Product.name.ilike(search_term)) |
        (Product.barcode.ilike(search_term)) |
        (Product.sku.ilike(search_term)) |
        (Product.category.ilike(search_term)),
        Product.is_active == True
    ).limit(limit).all()
    
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get product by ID
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/barcode/{barcode}", response_model=ProductResponse)
def get_product_by_barcode(barcode: str, db: Session = Depends(get_db)):
    """
    Get product by barcode
    """
    product = db.query(Product).filter(Product.barcode == barcode).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
