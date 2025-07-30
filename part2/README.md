# HolbertonBnB - Part 2

This project is the continuation of **HolbertonBnB**, an application inspired by platforms like AirBnB. Developed as part of the **Holberton School** curriculum, the goal of this second part is to build a **RESTful API** using **Flask** and **Flask-RESTx**, applying design principles such as:

- Layered architecture
- Object-oriented programming
- SOLID principles
- Patterns like **Repository** and **Facade**

The API allows management of the following resources: **users**, **places**, **amenities**, and **reviews**. The system is designed to be modular, testable, and scalable.

---

## Project Structure

```
parte2/
├── app/
│   ├── api/v1/              # REST endpoints organized by resource
│   ├── models/              # Entities and validations
│   ├── persistence/         # In-memory storage (repositories)
│   ├── services/            # Business logic (facades)
├── config.py                # Global configuration
├── run.py                   # Application entry point
├── requirements.txt         # Project dependencies
```

---

## Requirements and Installation

### Prerequisites

- Python 3.x  
- `pip`  
- `virtualenv` (optional but recommended)

### Installation

```bash
git clone <repo-url>
cd parte2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the app

```bash
python3 run.py
```

The API will be available at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## System Architecture

The system follows a layered architecture:

- **Presentation (API)**: Handles HTTP requests/responses and errors.
- **Business Logic (Facade)**: Applies rules and coordinates entities.
- **Persistence (Repository)**: Manages storage (in-memory).

> The **Facade** pattern is used to decouple the API from internal logic, exposing a clear interface.

---

## Main Entities

- **User**: A registered user of the platform.
- **Place**: A property listed by a user.
- **Amenity**: Optional services for a place (WiFi, pool, etc.).
- **Review**: Comment and rating for a place.
- **BaseModel**: Abstract class with common attributes (`id`, `created_at`, `updated_at`).

---

## Validations

- Email must contain `@` and `.`.
- First and last names: max 50 characters.
- Price must be a positive number.
- Valid geographical coordinates.
- Review score: between 1 and 5 stars.

---

## Available Endpoints

| Method | Route                                      | Description                            |
|--------|--------------------------------------------|----------------------------------------|
| POST   | `/api/v1/users/`                           | Create a new user                      |
| GET    | `/api/v1/users/<user_id>`                  | Retrieve user info                     |
| PUT    | `/api/v1/users/<user_id>`                  | Update user info                       |
| POST   | `/api/v1/places/`                          | Create a new place                     |
| GET    | `/api/v1/places/`                          | List all places                        |
| GET    | `/api/v1/places/<place_id>`                | Retrieve place info                    |
| PUT    | `/api/v1/places/<place_id>`                | Update a place                         |
| POST   | `/api/v1/amenities/`                       | Create a new amenity                   |
| GET    | `/api/v1/amenities/`                       | List all amenities                     |
| GET    | `/api/v1/amenities/<amenity_id>`           | Retrieve amenity info                  |
| PUT    | `/api/v1/amenities/<amenity_id>`           | Update an amenity                      |
| POST   | `/api/v1/reviews/`                         | Create a review                        |
| GET    | `/api/v1/reviews/`                         | List all reviews                       |
| GET    | `/api/v1/reviews/<review_id>`              | Retrieve a review                      |
| PUT    | `/api/v1/reviews/<review_id>`              | Update a review                        |
| DELETE | `/api/v1/reviews/<review_id>`              | Delete a review                        |
| GET    | `/api/v1/places/<place_id>/reviews`        | List reviews for a specific place      |

---

## Data Flow - Examples

### Register a User

1. Client sends `POST /api/v1/users/` with JSON data.
2. Data is validated.
3. `facade.create_user()` is called.
4. A `User` object is instantiated and saved.
5. A JSON response is returned.

### Create a Review

1. Client sends `POST /api/v1/reviews/`.
2. `user_id` and `place_id` are validated.
3. The review is stored and linked to the place.
4. A response with the review data is returned.

---

## Testing

To run automated tests:

```bash
python3 -m unittest discover tests/
```

Each test file covers both valid and invalid scenarios for the API endpoints.

---

## Authors

- Geronimo Negreira
- Agustin Lahalo 
- Bruno Dos Santos
