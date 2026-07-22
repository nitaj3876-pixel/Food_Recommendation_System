from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ---------- User ----------
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_admin: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Food ----------
class FoodOut(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class FoodCreate(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None


# ---------- Preferences (Select Favorites page) ----------
class PreferenceIn(BaseModel):
    tags: List[str]


# ---------- Favorites ----------
class FavoriteOut(BaseModel):
    id: int
    food: FoodOut
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- History ----------
class HistoryOut(BaseModel):
    id: int
    food: FoodOut
    viewed_at: datetime

    class Config:
        from_attributes = True


# ---------- Recommendation filter (Healthy/Diet Filter page) ----------
class RecommendationFilter(BaseModel):
    diet: Optional[str] = "all"   # all | healthy | vegetarian | vegan | high_protein | low_carb
