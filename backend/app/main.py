from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from . import models
from .database import engine
from .routes import users, foods, admin

# Creates tables automatically if they don't exist yet (dev convenience).
# For production, use Alembic migrations instead.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Foodie - Food Recommendation System",
    description="FastAPI backend for the Foodie app (TF-IDF + Cosine Similarity recommendations)",
    version="1.0.0",
)

# In production, set CORS_ORIGINS to a comma-separated list of your deployed
# frontend URL(s), e.g. "https://your-app.netlify.app". Left unset, it allows
# any origin - fine for local dev, too permissive for production.
_cors_env = os.getenv("CORS_ORIGINS")
allow_origins = [o.strip() for o in _cors_env.split(",")] if _cors_env else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(foods.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Foodie API is running. Visit /docs for the interactive API docs."}
