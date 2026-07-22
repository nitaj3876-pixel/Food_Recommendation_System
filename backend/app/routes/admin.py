from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, auth
from ..database import get_db

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin),
):
    """Powers the Admin Dashboard Page: Total Users, Total Recipes, Total Favorites, Today's Recommendations."""
    total_users = db.query(func.count(models.User.id)).scalar()
    total_recipes = db.query(func.count(models.Food.id)).scalar()
    total_favorites = db.query(func.count(models.Favorite.id)).scalar()

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    todays_recommendations = (
        db.query(func.count(models.History.id))
        .filter(models.History.viewed_at >= today_start)
        .scalar()
    )

    # Popular recipes = foods with the most favorites, most-favorited first
    popular = (
        db.query(models.Food, func.count(models.Favorite.id).label("fav_count"))
        .join(models.Favorite, models.Favorite.food_id == models.Food.id)
        .group_by(models.Food.id)
        .order_by(func.count(models.Favorite.id).desc())
        .limit(4)
        .all()
    )
    popular_recipes = [
        {"id": f.id, "name": f.name, "category": f.category, "image_url": f.image_url}
        for f, _ in popular
    ]

    return {
        "total_users": total_users,
        "total_recipes": total_recipes,
        "total_favorites": total_favorites,
        "todays_recommendations": todays_recommendations,
        "popular_recipes": popular_recipes,
    }


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin),
):
    """Powers the Admin Dashboard 'Users' section."""
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return [
        {"id": u.id, "full_name": u.full_name, "email": u.email, "is_admin": u.is_admin}
        for u in users
    ]


@router.get("/recipes")
def list_recipes(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin),
):
    """Powers the Admin Dashboard 'Recipes' section."""
    return db.query(models.Food).order_by(models.Food.id.desc()).all()
