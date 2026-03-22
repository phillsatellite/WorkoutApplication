from flask import session, request
from flask_restful import Resource
from models import Workout
from schemas import workout_schema, workouts_schema
from extensions import db


def get_current_user_id():
    return session.get("user_id")


class WorkoutList(Resource):
    def get(self):
        user_id = get_current_user_id()
        if not user_id:
            return {"error": "Unauthorized."}, 401

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        pagination = (
            Workout.query
            .filter_by(user_id=user_id)
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return {
            "workouts": workouts_schema.dump(pagination.items),
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
        }, 200

    def post(self):
        user_id = get_current_user_id()
        if not user_id:
            return {"error": "Unauthorized."}, 401

        data = request.get_json()

        errors = workout_schema.validate(data)
        if errors:
            return {"error": errors}, 422

        try:
            workout = Workout(
                title=data.get("title", "").strip(),
                notes=data.get("notes", ""),
                duration=data.get("duration"),
                user_id=user_id,
            )
            db.session.add(workout)
            db.session.commit()
            return workout_schema.dump(workout), 201

        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 422


class WorkoutDetail(Resource):
    def _get_workout(self, id):
        user_id = get_current_user_id()
        if not user_id:
            return None, ({"error": "Unauthorized."}, 401)

        workout = Workout.query.get(id)
        if not workout:
            return None, ({"error": "Workout not found."}, 404)

        if workout.user_id != user_id:
            return None, ({"error": "Forbidden."}, 403)

        return workout, None

    def patch(self, id):
        workout, err = self._get_workout(id)
        if err:
            return err

        data = request.get_json()

        try:
            if "title" in data:
                workout.title = data["title"].strip()
            if "notes" in data:
                workout.notes = data["notes"]
            if "duration" in data:
                workout.duration = data["duration"]

            db.session.commit()
            return workout_schema.dump(workout), 200

        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 422

    def delete(self, id):
        workout, err = self._get_workout(id)
        if err:
            return err

        db.session.delete(workout)
        db.session.commit()
        return {}, 204