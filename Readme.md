# Workout Tracker API

A Flask REST API for tracking personal workouts with session-based authentication.

## Setup

```bash
# Install pipenv if you don't have it
pip install pipenv

# Install dependencies
pipenv install

# Activate the virtual environment
pipenv shell

# Initialize the database
flask db init
flask db migrate -m "initial migration"
flask db upgrade

# Seed the database
python seed.py

# Run the server
python app.py
```

## Project Structure

```
WorkoutApplication/
├── app.py
├── models.py
├── schemas.py
├── extensions.py
├── seed.py
├── Pipfile
└── resources/
    ├── __init__.py
    ├── auth.py
    └── workouts.py
```

## Endpoints

### Auth
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/signup` | Register a new user |
| POST | `/login` | Login and start session |
| DELETE | `/logout` | End session |
| GET | `/me` | Get current logged-in user |

### Workouts (all protected)
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/workouts` | Get paginated workouts for current user |
| POST | `/workouts` | Create a new workout |
| PATCH | `/workouts/<id>` | Update a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

### Pagination
`GET /workouts?page=1&per_page=10`

## Example Requests

### Signup
```json
POST /signup
{
  "username": "phill",
  "email": "phill@example.com",
  "password": "password123"
}
```

### Login
```json
POST /login
{
  "username": "phill",
  "password": "password123"
}
```

### Create Workout
```json
POST /workouts
{
  "title": "Morning Run",
  "notes": "Easy 5k",
  "duration": 30
}
```

### Update Workout
```json
PATCH /workouts/1
{
  "duration": 45
}
```