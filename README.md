# 🍽️ Food Recommendation System

<p align="center">
  <b>Personalized Food Discovery powered by Machine Learning</b>
</p>

<p align="center">
  A full-stack food recommendation platform built with FastAPI, PostgreSQL, SQLAlchemy, JWT Authentication, TF-IDF and Cosine Similarity.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)

![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-009688?style=for-the-badge\&logo=fastapi)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge\&logo=postgresql)

![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge)

![Machine Learning](https://img.shields.io/badge/Machine%20Learning-TF--IDF%20%2B%20Cosine%20Similarity-orange?style=for-the-badge)

![JWT](https://img.shields.io/badge/Auth-JWT-black?style=for-the-badge)

</p>

---

## 📌 Overview

**Food Recommendation System** is a full-stack web application that helps users discover food based on their interests, preferences, favorites and browsing history.

The system uses a **content-based recommendation engine** built with **TF-IDF Vectorization and Cosine Similarity**.

Instead of showing random food items, the recommendation engine builds a user profile from:

* Favorite foods
* Viewed food history
* Selected preference tags
* Food name
* Food category
* Food tags

It then compares the user's profile with the food catalog and ranks the most relevant food items.

---

## ✨ Key Features

### 👤 User Features

* User Registration
* Secure Login
* JWT-based Authentication
* User Profile
* Favorite Foods
* Remove Favorites
* Recommendation History
* Food Preferences
* Personalized Recommendations
* Related Food Recommendations
* Food Search
* Category Filtering

### 🤖 Recommendation Engine

* TF-IDF text vectorization
* Cosine Similarity
* Content-based filtering
* User preference profiling
* Favorite-based recommendations
* History-based recommendations
* Related-food recommendations
* Dietary filtering

### 👑 Admin Features

* Admin Dashboard
* Total Users statistics
* Total Recipes statistics
* Total Favorites statistics
* Today's recommendation/view statistics
* Popular recipes
* User listing
* Recipe listing

### 🎨 Frontend

* Home Page
* Login Page
* Registration Page
* Recommendation Page
* Favorites Page
* History Page
* Profile Page
* Admin Dashboard
* Food images
* Responsive frontend structure

---

# 🧠 How the Recommendation System Works

The recommendation engine is implemented in:

```text
backend/app/recommendation.py
```

It creates a text representation from:

```text
Food Name
   +
Food Category
   +
Food Tags
```

Example:

```text
Pizza
Fast Food
cheese fast food italian pizza
```

This information is converted into numerical vectors using **TF-IDF**.

The system then calculates **Cosine Similarity** between the user's profile and the available foods.

### Recommendation Flow

```text
                 USER
                   │
                   ▼
        ┌────────────────────┐
        │ Favorites          │
        │ History            │
        │ Preferences        │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ User Profile Text  │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ TF-IDF Vectorizer  │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Cosine Similarity  │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Ranked Food Items  │
        └─────────┬──────────┘
                  │
                  ▼
             RECOMMENDATIONS
```

---

# 📐 Recommendation Algorithm

## TF-IDF

The system uses:

```python
TfidfVectorizer(stop_words="english")
```

to convert food-related text into feature vectors.

The text includes:

```text
name + category + tags
```

## Cosine Similarity

Similarity is calculated using:

```python
cosine_similarity()
```

The system ranks food items according to their similarity score.

### Example

If a user interacts with:

```text
Pizza
Pasta
Italian Food
```

the system can identify other foods containing similar terms and recommend related dishes such as:

```text
Margherita Pizza
Pepperoni Pizza
Penne Arrabbiata
Spaghetti Aglio e Olio
```

---

# 🏗️ System Architecture

```text
┌───────────────────────────────────────┐
│              FRONTEND                 │
│                                       │
│ HTML + CSS + JavaScript               │
│                                       │
│ Home | Login | Register | Recommend   │
│ Favorites | History | Profile | Admin │
└──────────────────┬────────────────────┘
                   │
                   │ HTTP / REST API
                   ▼
┌───────────────────────────────────────┐
│              FASTAPI                  │
│                                       │
│ Authentication                        │
│ User Management                       │
│ Food APIs                             │
│ Recommendation APIs                   │
│ Admin APIs                            │
└──────────────────┬────────────────────┘
                   │
          ┌────────┴─────────┐
          │                  │
          ▼                  ▼
┌──────────────────┐  ┌─────────────────┐
│ Recommendation   │  │ PostgreSQL      │
│ Engine           │  │ Database        │
│                  │  │                 │
│ TF-IDF           │  │ Users           │
│ Cosine Similarity│  │ Foods           │
│ User Profile     │  │ Favorites       │
│ Preferences      │  │ History         │
└──────────────────┘  │ Preferences     │
                      └─────────────────┘
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* PostgreSQL
* Pydantic
* Pydantic Settings
* Python-Jose
* Passlib
* Bcrypt
* Python Dotenv

## Machine Learning

* Scikit-learn
* TF-IDF Vectorization
* Cosine Similarity

## Data Processing

* Pandas
* NumPy

## Frontend

* HTML5
* CSS3
* JavaScript

## Database

* PostgreSQL

## Authentication

* JWT Access Tokens
* Password Hashing
* Protected API Routes

---

# 📂 Project Structure

```text
Food_Recommendation_System/
│
├── backend/
│   │
│   ├── app/
│   │   ├── dataset/
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── foods.py
│   │   │   └── users.py
│   │   │
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── recommendation.py
│   │   ├── requirements.txt
│   │   ├── schemas.py
│   │   └── seed_data.py
│   │
│   ├── requirements.txt
│   └── runtime.txt
│
├── frontend/
│   ├── images/
│   ├── js/
│   ├── admin.html
│   ├── favorites.html
│   ├── history.html
│   ├── home.html
│   ├── login.html
│   ├── profile.html
│   ├── recommend.html
│   └── register.html
│
├── css/
│
├── .gitignore
├── .gitattributes
├── README.md
└── pyvenv.cfg
```

---

# 🔌 API Endpoints

The backend exposes REST APIs through FastAPI.

## 👤 User APIs

### Register

```http
POST /api/users/register
```

Creates a new user account and returns an access token.

### Login

```http
POST /api/users/login
```

Authenticates the user and returns a JWT access token.

### Current User

```http
GET /api/users/me
```

Returns the authenticated user's profile.

### Save Preferences

```http
POST /api/users/preferences
```

Stores the user's selected food preference tags.

### Favorites

```http
GET /api/users/favorites
```

Returns the authenticated user's favorite foods.

### Add Favorite

```http
POST /api/users/favorites/{food_id}
```

Adds a food item to favorites.

### Remove Favorite

```http
DELETE /api/users/favorites/{food_id}
```

Removes a food item from favorites.

### History

```http
GET /api/users/history
```

Returns the user's food viewing history.

---

# 🍴 Food APIs

### List Foods

```http
GET /api/foods
```

Supports:

```text
search
category
```

Example:

```text
/api/foods?search=pizza
```

or:

```text
/api/foods?category=Healthy
```

### Get Food

```http
GET /api/foods/{food_id}
```

Returns a specific food item.

### Related Foods

```http
GET /api/foods/{food_id}/related
```

Returns similar foods using TF-IDF + Cosine Similarity.

### Personalized Recommendations

```http
GET /api/foods/recommend/for-me
```

Supports dietary filters such as:

```text
all
healthy
vegetarian
vegan
high_protein
low_carb
```

---

# 👑 Admin APIs

Admin endpoints are protected and require admin authentication.

### Dashboard Statistics

```http
GET /api/admin/stats
```

Provides:

* Total users
* Total recipes
* Total favorites
* Today's recommendations
* Popular recipes

### Users

```http
GET /api/admin/users
```

Returns registered users.

### Recipes

```http
GET /api/admin/recipes
```

Returns available recipes/food items.

---

# 🗄️ Database

The project uses **PostgreSQL** with SQLAlchemy ORM.

The database connection is configured using:

```text
DATABASE_URL
```

Default development format:

```text
postgresql://postgres:postgres@localhost:5432/food_recommendation_db
```

### Database Tables

The application includes models for:

```text
users
foods
favorites
history
user_preferences
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/nitaj3876-pixel/Food_Recommendation_System.git
```

## 2. Open the Project

```bash
cd Food_Recommendation_System
```

## 3. Create Virtual Environment

```bash
python -m venv venv
```

## 4. Activate Virtual Environment

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
venv\Scripts\activate
```

---

# 📦 Install Backend Dependencies

From the project root:

```powershell
python -m pip install -r backend\requirements.txt
```

The backend requirements include:

```text
FastAPI
Uvicorn
SQLAlchemy
PostgreSQL driver
Pydantic
JWT authentication
Password hashing
Scikit-learn
Pandas
NumPy
```

---

# 🐘 PostgreSQL Setup

Make sure PostgreSQL is installed and running.

Create a database named:

```text
food_recommendation_db
```

The application can use:

```text
DATABASE_URL
```

inside the backend environment configuration.

Example:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/food_recommendation_db
```

> Never commit real database passwords, JWT secrets or other credentials to GitHub.

---

# 🚀 Start the Backend

From the project root:

```powershell
python -m uvicorn backend.app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 📚 Swagger API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Alternative documentation:

```text
http://127.0.0.1:8000/redoc
```

The root endpoint returns:

```json
{
  "message": "Foodie API is running. Visit /docs for the interactive API docs."
}
```

---

# 🌱 Seed Sample Food Data

The project includes:

```text
backend/app/seed_data.py
```

This file contains sample food records.

From the **backend folder**, run:

```powershell
cd backend
python -m app.seed_data
```

The seed data includes examples such as:

```text
Pizza
Biryani
Burger
Pasta
Salad
Paneer Tikka
Chicken
Sushi
Dosa
Smoothie
Thai Green Curry
Avocado Toast
Chicken Tikka
Margherita Pizza
Pepperoni Pizza
Chicken Biryani
Veg Biryani
Penne Arrabbiata
Palak Paneer
Butter Chicken
```

---

# 🌐 Run the Frontend

The frontend is a static HTML/CSS/JavaScript application.

Main pages include:

```text
frontend/home.html
frontend/login.html
frontend/register.html
frontend/recommend.html
frontend/favorites.html
frontend/history.html
frontend/profile.html
frontend/admin.html
```

For local development, open the frontend using **VS Code Live Server** or another static HTTP server.

Example with Python:

```powershell
python -m http.server 5500 --directory frontend
```

Then open:

```text
http://127.0.0.1:5500/home.html
```

Make sure the FastAPI backend is also running on:

```text
http://127.0.0.1:8000
```

---

# 🔐 Authentication Flow

```text
User
 │
 ▼
Register / Login
 │
 ▼
FastAPI
 │
 ▼
Password Verification
 │
 ▼
JWT Access Token
 │
 ▼
Frontend stores token
 │
 ▼
Authenticated API Requests
 │
 ▼
Protected User/Admin Resources
```

---

# ❤️ Personalization Flow

```text
User Login
     │
     ▼
Favorite Foods ─────┐
                    │
Browsing History ───┤
                    │
Food Preferences ───┤
                    ▼
             User Profile
                    │
                    ▼
              TF-IDF Vector
                    │
                    ▼
          Cosine Similarity
                    │
                    ▼
          Ranked Food Results
```

---

# 🧪 Example Recommendation

Suppose a user selects:

```text
Vegetarian
Indian
High Protein
```

The system creates a user profile using the selected preference tags.

If the user also favorites:

```text
Paneer Tikka
Palak Paneer
```

the recommendation engine can identify similar foods such as:

```text
Paneer Butter Masala
Veg Biryani
Dosa
Pasta
```

depending on their TF-IDF similarity.

---

# 📊 Admin Dashboard

The Admin Dashboard provides application-level statistics.

It tracks:

| Metric                  | Description                    |
| ----------------------- | ------------------------------ |
| Total Users             | Registered users               |
| Total Recipes           | Food items in database         |
| Total Favorites         | Favorite records               |
| Today's Recommendations | Food history/views for the day |
| Popular Recipes         | Most-favorited foods           |

---

# 🖼️ Frontend Pages

| Page             | Purpose                      |
| ---------------- | ---------------------------- |
| `home.html`      | Main food discovery page     |
| `login.html`     | User authentication          |
| `register.html`  | New account registration     |
| `recommend.html` | Personalized recommendations |
| `favorites.html` | Saved favorite foods         |
| `history.html`   | Previously viewed foods      |
| `profile.html`   | User profile                 |
| `admin.html`     | Admin dashboard              |

---

# 🔒 Security

The project includes:

* JWT-based authentication
* Password hashing
* Protected user endpoints
* Protected admin endpoints
* Environment-based configuration
* CORS configuration
* Database credentials through environment variables

### Important

Do not upload:

```text
.env
API keys
Database passwords
JWT secrets
Private credentials
```

to GitHub.

---

# 📁 Important Backend Files

### `main.py`

Application entry point.

It creates the FastAPI application, configures CORS, creates database tables and registers:

```text
Users Router
Foods Router
Admin Router
```

### `recommendation.py`

Contains the Machine Learning recommendation engine.

Uses:

```text
TF-IDF
Cosine Similarity
```

### `database.py`

Configures SQLAlchemy and PostgreSQL.

### `models.py`

Defines database models:

```text
User
Food
Favorite
History
UserPreference
```

### `auth.py`

Handles:

```text
Password hashing
Password verification
JWT creation
Current user authentication
Admin authentication
```

### `schemas.py`

Defines Pydantic request and response schemas.

### `seed_data.py`

Adds sample food data to the database.

---

# 🎯 Project Objectives

* Build a real-world recommendation system.
* Apply Machine Learning to food discovery.
* Implement content-based recommendation.
* Build a REST API using FastAPI.
* Integrate PostgreSQL with SQLAlchemy.
* Implement JWT authentication.
* Build a complete frontend.
* Create personalized user recommendations.
* Provide admin analytics.

---

# 💡 Why This Project?

Traditional food applications often require users to manually search for food.

This system improves discovery by learning from:

```text
User Preferences
       +
Favorites
       +
History
       ↓
Personalized Recommendations
```

This makes the platform more useful for users who want to discover new food based on their interests.

---

# 🚀 Future Enhancements

* [ ] AI-powered food chatbot
* [ ] Food image recognition
* [ ] Nutrition information
* [ ] Calorie-based recommendations
* [ ] Recipe details and ingredients
* [ ] Cooking instructions
* [ ] Rating and review system
* [ ] Advanced recommendation models
* [ ] Collaborative filtering
* [ ] Hybrid recommendation engine
* [ ] Recommendation explanation
* [ ] User recommendation analytics
* [ ] Cloud deployment
* [ ] Docker support
* [ ] CI/CD pipeline
* [ ] Mobile application

---



# 🧑‍💻 Development Workflow

```text
Clone Repository
       ↓
Create Virtual Environment
       ↓
Install Dependencies
       ↓
Configure PostgreSQL
       ↓
Start FastAPI Backend
       ↓
Seed Food Data
       ↓
Start Frontend
       ↓
Register / Login
       ↓
Select Preferences
       ↓
Explore Foods
       ↓
Generate Recommendations
```

---

# 📌 Repository

**GitHub:**

https://github.com/nitaj3876-pixel/Food_Recommendation_System

---

# 👩‍💻 Author

## Nita Jadhav

Diploma in Information Technology

### Interests

* Artificial Intelligence
* Machine Learning
* Python Development
* Data Science
* Backend Development
* Full-Stack Development
* Recommendation Systems

---

# ⭐ Support

If you find this project useful, please consider giving the repository a ⭐ **Star**.

It helps support the project and future development.

---

<p align="center">
  <b>🍽️ Food Recommendation System</b>
</p>

<p align="center">
  Built with Python • FastAPI • PostgreSQL • SQLAlchemy • Machine Learning • HTML • CSS • JavaScript
</p>

<p align="center">
  Made with ❤️ by Nita Jadhav
</p>
