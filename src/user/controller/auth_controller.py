from dataclasses import asdict

from flask import Blueprint, Response, json, request

from src import db
from src.user.controller.request.loginRequest import LoginRequest
from src.user.repository.user_repository import UserRepository
from src.user.service.auth_service import AuthService

auth_blueprint = Blueprint("auth", __name__)

user_repository = UserRepository(db.session)

auth_service = AuthService(user_repository=user_repository)


@auth_blueprint.route("/auth/login", methods=["POST"])
def login() -> Response:
    req_data = request.get_json()
    login_request = LoginRequest(email=req_data["email"], password=req_data["password"])
    login_response, access_token = auth_service.login(login_request)

    response = json.jsonify(asdict(login_response))
    response.status_code = 200

    response.headers["Authorization"] = f"Bearer {access_token}"
    response.status_code = 200
    return response