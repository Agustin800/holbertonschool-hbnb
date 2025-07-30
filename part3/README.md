# HolbertonBnB – Part 3

By Geronimo Negreira, Agustín Lahalo & Bruno Dos Santos – Cohort 26

---

## Introduction

In Part 3 we extend our HBnB RESTful API by adding:

- Persistent storage with SQLAlchemy (SQLite by default).
- Password hashing with Flask-Bcrypt.
- JWT authentication with Flask-JWT-Extended.
- Role-based access control (admin vs. regular users).
- Database seeding to create a default admin user and a set of amenities at startup.

---

## Project Structure

```
part3/
├── app/
│   ├── api/v1/                 
│   │   ├── auth.py             
│   │   ├── users.py            
│   │   ├── amenity.py          
│   │   ├── places.py           
│   │   └── reviews.py          
│   ├── models/                 
│   ├── persistence/            
│   ├── services/               
│   ├── __init__.py             
│   └── config.py               
├── tests/                      
├── requirements.txt            
├── run.py                      
└── .gitignore                  
```

---

## Prerequisites

- Python 3.7 or newer  
- pip  
- Optionally, virtualenv  

---

## Installation

1. Clone the repository and go into the `part3` directory:
   ```bash
   git clone  https://github.com/Geronimo304/holbertonschool-hbnb.git
   cd part3
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

- Edit `config.py` or set the environment variables `SECRET_KEY` and `JWT_SECRET_KEY` as needed.  
- By default, the app uses SQLite (`sqlite:///database.db`) in development mode.

---

## Database and Seeding

When the app starts (`run.py`), it will:

1. Create database tables using SQLAlchemy.  
2. Ensure there is an admin user (email `admin@hbnb.io`, password `admin1234`).  
3. Insert default amenities: `WiFi`, `Swimming Pool`, `Air Conditioning`.

You can customize these values in the `create_admin_user()` function in `app/__init__.py`.

---

## Running the Application

```bash
python3 run.py
```

The API will be available at:  
```
http://127.0.0.1:5000/
```

---

## Authentication

1. **Obtain a token**  
   ```http
   POST /api/v1/auth/login
   Content-Type: application/json

   {
     "email": "admin@hbnb.io",
     "password": "admin1234"
   }
   ```
   **Response:**  
   ```json
   {
     "access_token": "<JWT_TOKEN>"
   }
   ```

2. **Use the token** in protected endpoints:
   ```
   Authorization: Bearer <JWT_TOKEN>
   ```

---

## Available Endpoints

| Method | Route                                   | Description                                          | Authentication                      |
|--------|-----------------------------------------|------------------------------------------------------|-------------------------------------|
| POST   | `/api/v1/auth/login`                    | Generate a new JWT token                             | None                                |
| GET    | `/api/v1/users/`                        | List all users                                       | Optional (admin privileges for some)|
| POST   | `/api/v1/users/`                        | Create a new user                                    | Admin only                          |
| GET    | `/api/v1/users/<user_id>`               | Retrieve user details                                | Public                              |
| PUT    | `/api/v1/users/<user_id>`               | Update user information                              | Admin or the user themself          |
| GET    | `/api/v1/amenity/`                      | List all amenities                                   | Public                              |
| POST   | `/api/v1/amenity/`                      | Create a new amenity                                 | Admin only                          |
| GET    | `/api/v1/amenity/<amenity_id>`          | Retrieve amenity details                             | Public                              |
| PUT    | `/api/v1/amenity/<amenity_id>`          | Update an amenity                                    | Admin only                          |
| GET    | `/api/v1/places/`                       | List all places                                      | Public                              |
| POST   | `/api/v1/places/`                       | Create a new place (owner is the JWT user)           | JWT required                        |
| GET    | `/api/v1/places/<place_id>`             | Retrieve place details                               | Public                              |
| PUT    | `/api/v1/places/<place_id>`             | Update a place (only the owner)                      | JWT required                        |
| GET    | `/api/v1/reviews/`                      | List all reviews                                     | Public                              |
| POST   | `/api/v1/reviews/`                      | Create a review (one per user per place)             | JWT required                        |
| GET    | `/api/v1/reviews/<review_id>`           | Retrieve review details                              | Public                              |
| PUT    | `/api/v1/reviews/<review_id>`           | Update a review (only the author)                    | JWT required                        |
| DELETE | `/api/v1/reviews/<review_id>`           | Delete a review (only the author)                    | JWT required                        |
| GET    | `/api/v1/places/<place_id>/reviews`     | List reviews for a specific place                    | Public                              |

---

## Authors

- Geronimo Negreira  
- Agustín Lahalo  
- Bruno Dos Santos  
