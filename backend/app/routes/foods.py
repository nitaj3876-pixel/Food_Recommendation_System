from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, schemas, auth, recommendation
from ..database import get_db

router = APIRouter(prefix="/api/foods", tags=["Foods"])


@router.get("", response_model=List[schemas.FoodOut])
def list_foods(
    search: Optional[str] = Query(None, description="Search foods by name"),
    category: Optional[str] = Query(None, description="Filter by category e.g. Healthy, Vegan"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Food)
    if search:
        query = query.filter(models.Food.name.ilike(f"%{search}%"))
    if category:
        # exact (case-insensitive) match - NOT a substring match, so filtering for
        # "Vegetarian" never also pulls in foods categorized "Non-Vegetarian"
        query = query.filter(func.lower(models.Food.category) == category.lower())
    return query.all()


@router.get("/{food_id}", response_model=schemas.FoodOut)
def get_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    # log this view into history (Recommendation History page)
    db.add(models.History(user_id=current_user.id, food_id=food_id))
    db.commit()
    return food


@router.get("/{food_id}/related", response_model=List[schemas.FoodOut])
def get_related(
    food_id: int,
    db: Session = Depends(get_db),
):
    """Powers click-through from any food card: 'more like this' based on
    TF-IDF + cosine similarity between that food and every other food -
    so Pasta Primavera surfaces other pasta dishes, Biryani surfaces other
    rice/biryani-style dishes, etc."""
    food_exists = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not food_exists:
        raise HTTPException(status_code=404, detail="Food not found")
    return recommendation.get_related_foods(db, food_id, top_n=8)


@router.get("/recommend/for-me", response_model=List[schemas.FoodOut])
def recommend_for_me(
    diet: Optional[str] = Query("all", description="all | healthy | vegetarian | vegan | high_protein | low_carb"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Powers the Home Page 'Recommended For You' and Recommendations Page.

    Ranks the ENTIRE food catalog by relevance to the user (not just a small
    top slice) so that:
      - the "All" chip shows every food, most-relevant first
      - the Healthy / Vegetarian / Vegan / High Protein / Low Carb chips
        search across the whole catalog, not just whatever made a small
        top-N cut before filtering
    """
    total_foods = db.query(models.Food).count()
    recs = recommendation.get_recommendations_for_user(db, current_user.id, top_n=max(total_foods, 1))
    recs = recommendation.filter_by_diet(recs, diet)
    return recs
