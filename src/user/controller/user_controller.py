from flask import Blueprint, jsonify, request

from src.user.service.user_service import UserService

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = UserService.add_user(data)
    return (
        jsonify(
            {"id": user.id, "name": user.name, "email": user.email, "title": user.title}
        ),
        201,
    )


@user_blueprint.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserService.get_user(user_id)
    if user:
        return (
            jsonify(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "title": user.title,
                    "admin_flag": user.admin_flag,
                    "created_timestamp": user.created_timestamp,
                    "modified_timestamp": user.modified_timestamp,
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "User not found"}), 404