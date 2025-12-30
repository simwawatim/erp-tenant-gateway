from flask import Blueprint, request
import requests

from config import DJANGO_BASE_URL
from decorator.auth_decorator import jwt_required

profile_picture_bp = Blueprint("profile_picture_bp", __name__)


@profile_picture_bp.route("/api/profile/picture/", methods=["POST"])
@jwt_required
def add_profile_picture():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    if "profilePicture" not in request.files:
        return {
            "status": "fail",
            "message": "profilePicture file is required",
            "data": None
        }, 400

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }

    image_file = request.files["profilePicture"]

    try:
        django_response = requests.post(
            f"{DJANGO_BASE_URL}/profile/picture/add/",
            headers=headers,
            files={"profilePicture": image_file}
        )
        return django_response.json(), django_response.status_code

    except requests.exceptions.RequestException as e:
        return {
            "status": "fail",
            "message": str(e),
            "data": None
        }, 500



@profile_picture_bp.route("/api/profile/picture/", methods=["DELETE"])
@jwt_required
def delete_profile_picture():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }

    try:
        django_response = requests.delete(
            f"{DJANGO_BASE_URL}/profile/picture/delete/",
            headers=headers
        )
        return django_response.json(), django_response.status_code

    except requests.exceptions.RequestException as e:
        return {
            "status": "fail",
            "message": str(e),
            "data": None
        }, 500
