#!/usr/bin/env python3
"""Flask app
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """handle / route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """handle /users route
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """login a user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    user_session = AUTH.create_session(email)
    res = jsonify({"email": f"{email}", "message": "logged in"})
    res.set_cookie("session_id", user_session)

    return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """logout a user
    """
    user_session_id = request.cookies.get(session_id)
    user = AUTH.get_user_from_session_id(user_session_id)
    if user is None or user_session_id is None:
        abort(403)
    AUTH.destroy_session(user_session_id)
    redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
