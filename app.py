from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from extensions import db, bcrypt, migrate


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout_tracker.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "super-secret-key-change-in-production"

    CORS(app, supports_credentials=True)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    from resources.auth import Signup, Login, Logout, Me
    from resources.workouts import WorkoutList, WorkoutDetail

    api.add_resource(Signup, "/signup")
    api.add_resource(Login, "/login")
    api.add_resource(Logout, "/logout")
    api.add_resource(Me, "/me")
    api.add_resource(WorkoutList, "/workouts")
    api.add_resource(WorkoutDetail, "/workouts/<int:id>")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5555)