from flask import session, request
from flask_restful import Resource
from models import User
from schemas import user_schema
from extensions import db


class Signup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not username or not email or not password:
            return {"error": "Username, email, and password are required."}, 422

        if User.query.filter_by(username=username).first():
            return {"error": "Username already taken."}, 422

        if User.query.filter_by(email=email).first():
            return {"error": "Email already in use."}, 422

        try:
            user = User(username=username, email=email)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.id
            return user_schema.dump(user), 201

        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 422


class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")

        user = User.query.filter_by(username=username).first()

        if not user or not user.authenticate(password):
            return {"error": "Invalid username or password."}, 401

        session["user_id"] = user.id
        return user_schema.dump(user), 200


class Logout(Resource):
    def delete(self):
        if not session.get("user_id"):
            return {"error": "Not logged in."}, 401

        session.pop("user_id", None)
        return {}, 204


class Me(Resource):
    def get(self):
        user_id = session.get("user_id")

        if not user_id:
            return {"error": "Unauthorized."}, 401

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found."}, 404

        return user_schema.dump(user), 200