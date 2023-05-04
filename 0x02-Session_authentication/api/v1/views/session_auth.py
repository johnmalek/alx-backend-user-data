#!/usr/bin/env python3
"""A python module
"""
import os
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['GET'], strict-slashes=False)
def auth_session():
    """handle user login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email)
    if users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_name, session_id)
            return response
    return jsonify({"error": "wrng password"}), 401
