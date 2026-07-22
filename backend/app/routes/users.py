from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if user_in.password != user_in.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=auth.hash_password(user_in.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = auth.create_access_token({"sub": str(new_user.id)})
    return {"access_token": token, "user": new_user}


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "user": user}


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@router.post("/preferences", status_code=status.HTTP_204_NO_CONTENT)
def save_preferences(
    prefs: schemas.PreferenceIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Used by the 'Select Your Favorite Foods' onboarding page."""
    db.query(models.UserPreference).filter(models.UserPreference.user_id == current_user.id).delete()
    for tag in prefs.tags:
        db.add(models.UserPreference(user_id=current_user.id, tag=tag))
    db.commit()


@router.get("/favorites", response_model=List[schemas.FavoriteOut])
def list_favorites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return (
        db.query(models.Favorite)
        .filter(models.Favorite.user_id == current_user.id)
        .order_by(models.Favorite.created_at.desc())
        .all()
    )


@router.post("/favorites/{food_id}", status_code=status.HTTP_201_CREATED)
def add_favorite(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    exists = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id, models.Favorite.food_id == food_id
    ).first()
    if exists:
        return {"detail": "Already in favorites"}

    db.add(models.Favorite(user_id=current_user.id, food_id=food_id))
    db.commit()
    return {"detail": "Added to favorites"}


@router.delete("/favorites/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    fav = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id, models.Favorite.food_id == food_id
    ).first()
    if fav:
        db.delete(fav)
        db.commit()


@router.get("/history", response_model=List[schemas.HistoryOut])
def list_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return (
        db.query(models.History)
        .filter(models.History.user_id == current_user.id)
        .order_by(models.History.viewed_at.desc())
        .all()
    )
