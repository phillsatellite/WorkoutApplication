from app import create_app
from extensions import db
from models import User, Workout
from faker import Faker

fake = Faker()
app = create_app()

WORKOUT_TITLES = [
    "Morning Run",
    "Upper Body Lift",
    "Leg Day",
    "HIIT Session",
    "Yoga Flow",
    "Cycling",
    "Pull Day",
    "Core Workout",
    "Cardio Blast",
    "Full Body Circuit",
]

with app.app_context():
    print("Clearing existing data...")
    Workout.query.delete()
    User.query.delete()
    db.session.commit()

    print("Seeding users...")
    users = []
    for _ in range(3):
        user = User(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
        )
        user.password_hash = "password123"
        db.session.add(user)
        users.append(user)

    db.session.commit()

    print("Seeding workouts...")
    for user in users:
        for _ in range(5):
            workout = Workout(
                title=fake.random_element(WORKOUT_TITLES),
                notes=fake.sentence(nb_words=10),
                duration=fake.random_int(min=15, max=90),
                user_id=user.id,
            )
            db.session.add(workout)

    db.session.commit()

    print(f"Done! Seeded {len(users)} users and {len(users) * 5} workouts.")