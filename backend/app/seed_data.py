"""
Run this once after the tables are created (i.e. after starting the app at least once,
or after `python -c "from app.database import engine, Base; import app.models; Base.metadata.create_all(engine)"`)
to fill the foods table with sample data matching the app's mockup.

Usage (from the backend folder, NOT backend/app — this must run as a module
so the relative imports inside the app package work):
    python -m app.seed_data
"""

from .database import SessionLocal
from . import models

SAMPLE_FOODS = [
    # name, category, description, tags, image_url
    ("Pizza", "Fast Food", "Classic cheesy pizza with a crisp crust.", "cheese fast food italian", None),
    ("Biryani", "Non-Vegetarian", "Fragrant spiced rice layered with meat.", "spicy rice indian non-vegetarian", None),
    ("Burger", "Fast Food", "Grilled patty burger with fresh toppings.", "fast food grilled bun", None),
    ("Pasta", "Vegetarian", "Italian pasta tossed in a light sauce.", "italian carbs vegetarian", None),
    ("Salad", "Healthy", "Fresh mixed greens and vegetables.", "healthy low carb vegan raw", None),
    ("Paneer Tikka", "Vegetarian", "Marinated grilled cottage cheese cubes.", "vegetarian high protein indian grilled", None),
    ("Chicken", "High Protein", "Grilled chicken breast.", "high protein non-vegetarian grilled", None),
    ("Sushi", "Healthy", "Fresh raw fish and vinegared rice rolls.", "healthy japanese seafood low carb", None),
    ("Ice Cream", "Dessert", "Creamy sweet frozen dessert.", "dessert sweet cold", None),
    ("Dosa", "Vegetarian", "Crispy South Indian rice crepe.", "vegetarian indian breakfast", None),
    ("Sandwich", "Fast Food", "Layered bread with veggies and spreads.", "fast food quick vegetarian", None),
    ("Smoothie", "Healthy", "Blended fruit and yogurt drink.", "healthy vegan sweet drink", None),
    ("Veggie Buckwheat Bowl", "Healthy", "Buckwheat grains with roasted vegetables.", "healthy vegan gluten-free grain bowl", None),
    ("Spaghetti Aglio e Olio", "Vegetarian", "Garlic and olive oil spaghetti.", "vegetarian italian pasta light", None),
    ("Grilled Chicken Salad", "High Protein", "Salad topped with grilled chicken.", "high protein healthy low carb", None),
    ("Mango Smoothie Bowl", "Healthy", "Mango smoothie topped with fruit and granola.", "healthy vegan sweet breakfast", None),
    ("Quinoa Salad", "Healthy", "Quinoa with fresh vegetables and lemon dressing.", "healthy vegan high protein gluten-free", None),
    ("Thai Green Curry", "Vegan", "Spicy coconut curry with vegetables.", "vegan spicy thai curry", None),
    ("High Protein Bowl", "High Protein", "Grains, legumes, and grilled protein bowl.", "high protein healthy balanced", None),
    ("Avocado Toast", "Healthy", "Toasted bread topped with mashed avocado.", "healthy vegetarian breakfast quick", None),
    ("Grilled Vegetables", "Low Carb", "Assorted vegetables grilled to perfection.", "low carb vegan healthy", None),
    ("Chickpea Salad", "Vegan", "Chickpeas tossed with herbs and lemon.", "vegan high protein healthy", None),
    ("Pasta Primavera", "Vegetarian", "Pasta with fresh seasonal vegetables.", "vegetarian italian light", None),
    ("Grilled Chicken", "High Protein", "Simple herb-marinated grilled chicken.", "high protein non-vegetarian low carb", None),
    ("Veggie Wrap", "Healthy", "Whole wheat wrap stuffed with vegetables.", "healthy vegetarian quick lunch", None),

    # extra items so "more like this" has richer matches within each dish type
    ("Margherita Pizza", "Fast Food", "Classic pizza with tomato, basil and mozzarella.", "cheese fast food italian pizza", None),
    ("Pepperoni Pizza", "Fast Food", "Pizza topped with spicy pepperoni.", "cheese fast food italian pizza spicy", None),
    ("Chicken Biryani", "Non-Vegetarian", "Layered rice with spiced chicken.", "spicy rice indian non-vegetarian biryani", None),
    ("Veg Biryani", "Vegetarian", "Layered rice with mixed vegetables and spices.", "spicy rice indian vegetarian biryani", None),
    ("Penne Arrabbiata", "Vegetarian", "Penne pasta in a spicy tomato sauce.", "italian pasta vegetarian spicy", None),
    ("Palak Paneer", "Vegetarian", "Cottage cheese cubes in a spiced spinach gravy.", "vegetarian indian high protein paneer", None),
    ("Paneer Butter Masala", "Vegetarian", "Cottage cheese in a rich tomato-butter gravy.", "vegetarian indian paneer creamy", None),
    ("Butter Chicken", "Non-Vegetarian", "Chicken simmered in a creamy tomato gravy.", "non-vegetarian indian chicken creamy", None),
    ("Chicken Tikka", "High Protein", "Marinated chicken pieces grilled to char.", "high protein non-vegetarian grilled indian chicken", None),
    ("California Roll", "Healthy", "Sushi roll with crab, avocado and cucumber.", "healthy japanese seafood sushi low carb", None),
    ("Salmon Nigiri", "Healthy", "Fresh salmon over pressed vinegared rice.", "healthy japanese seafood sushi low carb", None),
    ("Club Sandwich", "Fast Food", "Triple-decker sandwich with chicken and veggies.", "fast food quick sandwich", None),
    ("Grilled Veggie Sandwich", "Healthy", "Grilled vegetables between toasted bread.", "healthy vegetarian quick sandwich", None),
    ("Berry Smoothie", "Healthy", "Blended mixed berries with yogurt.", "healthy vegan sweet drink smoothie fruit", None),
    ("Greek Salad", "Healthy", "Cucumber, tomato, olives and feta.", "healthy vegetarian low carb salad", None),
    ("Caesar Salad", "Vegetarian", "Romaine lettuce with parmesan and croutons.", "vegetarian salad healthy", None),
]


def run():
    db = SessionLocal()
    try:
        added = 0
        for name, category, description, tags, image_url in SAMPLE_FOODS:
            exists = db.query(models.Food).filter(models.Food.name == name).first()
            if exists:
                continue
            db.add(models.Food(
                name=name,
                category=category,
                description=description,
                tags=tags,
                image_url=image_url,
            ))
            added += 1
        db.commit()
        print(f"Seed complete. Added {added} new foods (skipped {len(SAMPLE_FOODS) - added} already present).")
    finally:
        db.close()


def make_admin(email: str):
    """Promote an existing registered user to admin, so they can access admin.html."""
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            print(f"No user found with email {email}. Register that account first, then re-run this.")
            return
        user.is_admin = 1
        db.commit()
        print(f"{email} is now an admin.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
    # Uncomment and set your own email after registering, to unlock admin.html:
    # make_admin("you@example.com")
