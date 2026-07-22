from typing import List, Optional
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from . import models


def _food_corpus_text(food: models.Food) -> str:
    """Combine name, category and tags into one text blob for TF-IDF."""
    parts = [food.name or "", food.category or "", food.tags or ""]
    return " ".join(parts)


def get_recommendations_for_user(db: Session, user_id: int, top_n: int = 8) -> List[models.Food]:
    """
    Builds a TF-IDF matrix over all foods' (name + category + tags),
    then compares it against a 'profile vector' built from:
      - foods the user marked as favorites
      - foods in the user's view history
      - tags picked on the Select Favorites onboarding page
    Returns the top_n most similar foods the user hasn't already favorited.
    """
    all_foods = db.query(models.Food).all()
    if not all_foods:
        return []

    corpus = [_food_corpus_text(f) for f in all_foods]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Build the user's interest profile text
    fav_food_ids = {f.food_id for f in db.query(models.Favorite).filter(models.Favorite.user_id == user_id)}
    history_food_ids = [h.food_id for h in db.query(models.History).filter(models.History.user_id == user_id)]
    pref_tags = [p.tag for p in db.query(models.UserPreference).filter(models.UserPreference.user_id == user_id)]

    profile_terms = []
    id_to_food = {f.id: f for f in all_foods}
    for fid in list(fav_food_ids) + history_food_ids:
        food = id_to_food.get(fid)
        if food:
            profile_terms.append(_food_corpus_text(food))
    profile_terms.extend(pref_tags)

    if not profile_terms:
        # New user with no signal yet -> just return a general spread of foods
        return all_foods[:top_n]

    profile_text = " ".join(profile_terms)
    profile_vector = vectorizer.transform([profile_text])

    similarities = cosine_similarity(profile_vector, tfidf_matrix).flatten()

    scored = [
        (all_foods[i], similarities[i])
        for i in range(len(all_foods))
        if all_foods[i].id not in fav_food_ids
    ]
    scored.sort(key=lambda x: x[1], reverse=True)

    return [food for food, score in scored[:top_n]]


def get_related_foods(db: Session, food_id: int, top_n: int = 8) -> List[models.Food]:
    """
    Used when a person clicks into a specific food (from a card or history row).
    Compares that one food's TF-IDF vector against every other food's vector and
    returns the most similar ones - e.g. clicking "Pasta Primavera" surfaces other
    pasta dishes, clicking "Biryani" surfaces other rice/biryani-style dishes,
    instead of just anything sharing the same broad category label.
    """
    all_foods = db.query(models.Food).all()
    target = next((f for f in all_foods if f.id == food_id), None)
    if not target or len(all_foods) < 2:
        return []

    corpus = [_food_corpus_text(f) for f in all_foods]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    target_idx = all_foods.index(target)
    similarities = cosine_similarity(tfidf_matrix[target_idx], tfidf_matrix).flatten()

    scored = [
        (all_foods[i], similarities[i])
        for i in range(len(all_foods))
        if all_foods[i].id != food_id
    ]
    scored.sort(key=lambda x: x[1], reverse=True)

    return [food for food, score in scored[:top_n]]


def filter_by_diet(foods: List[models.Food], diet: Optional[str]) -> List[models.Food]:
    """Used by the Healthy/Diet Filter page - filters recommended foods by category/tag keyword.

    Uses exact whole-word matching (not substring) so that e.g. filtering for
    "vegetarian" does not also match foods tagged "non-vegetarian".
    """
    if not diet or diet == "all":
        return foods
    diet_key = diet.lower().replace("_", " ")

    def food_words(food: models.Food) -> set:
        blob = f"{food.category or ''} {food.tags or ''}".lower()
        # normalize comma separators into spaces, but KEEP hyphens intact so that
        # "non-vegetarian" stays one token and never matches a "vegetarian" filter
        blob = blob.replace(",", " ")
        return set(blob.split())

    diet_words = set(diet_key.split())
    return [f for f in foods if diet_words.issubset(food_words(f))]
