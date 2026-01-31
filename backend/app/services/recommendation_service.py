"""
Recommendation Engine Service
Handles product recommendations based on market basket analysis
"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.recommendation import ProductRecommendation
from app.models.transaction import Transaction, TransactionItem
from app.schemas.recommendation import RecommendationResponse, RecommendationItem


class RecommendationService:
    """Service for product recommendations"""
    
    def get_recommendations(
        self,
        db: Session,
        cart_id: int,
        limit: int = 5
    ) -> RecommendationResponse:
        """
        Get product recommendations for a cart based on:
        1. Frequently bought together (market basket analysis)
        2. Similar category products
        3. Popular items
        """
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            raise ValueError(f"Cart {cart_id} not found")
        
        cart_product_ids = [item.product_id for item in cart.items]
        
        if not cart_product_ids:
            # If cart is empty, return popular products
            return self._get_popular_products(db, cart_id, limit)
        
        recommendations = []
        
        # 1. Frequently bought together (market basket analysis)
        freq_together = self._get_frequently_bought_together(
            db, cart_product_ids, limit
        )
        recommendations.extend(freq_together)
        
        # 2. Similar category products
        if len(recommendations) < limit:
            similar_category = self._get_similar_category_products(
                db, cart_product_ids, limit - len(recommendations)
            )
            recommendations.extend(similar_category)
        
        # 3. Popular products as fallback
        if len(recommendations) < limit:
            popular = self._get_popular_products(
                db, cart_id, limit - len(recommendations)
            )
            recommendations.extend(popular.recommendations)
        
        # Remove duplicates and products already in cart
        seen_ids = set(cart_product_ids)
        unique_recommendations = []
        for rec in recommendations:
            if rec.product.id not in seen_ids:
                unique_recommendations.append(rec)
                seen_ids.add(rec.product.id)
                if len(unique_recommendations) >= limit:
                    break
        
        return RecommendationResponse(
            cart_id=cart_id,
            recommendations=unique_recommendations[:limit],
            based_on_items=cart_product_ids
        )
    
    def _get_frequently_bought_together(
        self,
        db: Session,
        product_ids: List[int],
        limit: int
    ) -> List[RecommendationItem]:
        """
        Market basket analysis: Find products frequently bought with cart items
        """
        recommendations = []
        
        # Query: Find products that appear in transactions with our cart products
        # This is a simplified version - in production, use proper association rules
        
        for product_id in product_ids[:3]:  # Limit to first 3 products for performance
            # Find transactions containing this product
            transactions_with_product = db.query(TransactionItem.transaction_id).filter(
                TransactionItem.product_id == product_id
            ).subquery()
            
            # Find other products in those transactions
            co_occurring = db.query(
                TransactionItem.product_id,
                func.count(TransactionItem.product_id).label('frequency')
            ).filter(
                and_(
                    TransactionItem.transaction_id.in_(transactions_with_product),
                    TransactionItem.product_id.notin_(product_ids)
                )
            ).group_by(TransactionItem.product_id).order_by(
                func.count(TransactionItem.product_id).desc()
            ).limit(limit).all()
            
            for product_id_result, frequency in co_occurring:
                product = db.query(Product).filter(Product.id == product_id_result).first()
                if product and product.is_active:
                    # Calculate confidence based on frequency
                    confidence = min(frequency / 10.0, 1.0)  # Normalize
                    
                    recommendations.append(RecommendationItem(
                        product=product,
                        confidence_score=confidence,
                        recommendation_type="frequently_bought_together",
                        reason=f"Frequently purchased with {product.name}"
                    ))
        
        # Sort by confidence
        recommendations.sort(key=lambda x: x.confidence_score, reverse=True)
        
        return recommendations[:limit]
    
    def _get_similar_category_products(
        self,
        db: Session,
        product_ids: List[int],
        limit: int
    ) -> List[RecommendationItem]:
        """
        Get products from similar categories
        """
        # Get categories from cart products
        cart_products = db.query(Product).filter(Product.id.in_(product_ids)).all()
        categories = list(set([p.category for p in cart_products]))
        
        if not categories:
            return []
        
        # Find products in same categories
        similar_products = db.query(Product).filter(
            and_(
                Product.category.in_(categories),
                Product.id.notin_(product_ids),
                Product.is_active == True
            )
        ).limit(limit * 2).all()
        
        recommendations = []
        for product in similar_products[:limit]:
            recommendations.append(RecommendationItem(
                product=product,
                confidence_score=0.6,  # Medium confidence for category match
                recommendation_type="similar_category",
                reason=f"Similar to items in your cart ({product.category})"
            ))
        
        return recommendations
    
    def _get_popular_products(
        self,
        db: Session,
        cart_id: int,
        limit: int
    ) -> RecommendationResponse:
        """
        Get most popular products (by transaction frequency)
        """
        # Find most purchased products
        popular = db.query(
            TransactionItem.product_id,
            func.count(TransactionItem.product_id).label('purchase_count')
        ).group_by(TransactionItem.product_id).order_by(
            func.count(TransactionItem.product_id).desc()
        ).limit(limit).all()
        
        recommendations = []
        for product_id, count in popular:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product and product.is_active:
                confidence = min(count / 50.0, 1.0)  # Normalize
                recommendations.append(RecommendationItem(
                    product=product,
                    confidence_score=confidence,
                    recommendation_type="popular",
                    reason="Popular item"
                ))
        
        return RecommendationResponse(
            cart_id=cart_id,
            recommendations=recommendations,
            based_on_items=[]
        )


# Global recommendation service instance
recommendation_service = RecommendationService()
