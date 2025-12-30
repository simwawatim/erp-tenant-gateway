from flask import Blueprint, request, jsonify
import requests
from config import DJANGO_BASE_URL
from decorator.auth_decorator import jwt_required

profile_bp = Blueprint("profile_bp", __name__)
@profile_bp.route("/api/profile/", methods=["GET", "POST", "PUT"])
@jwt_required
def profile():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")  

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token  
    }

    if request.method == "GET":
        try:
            django_response = requests.get(
                f"{DJANGO_BASE_URL}/my-profile/",
                params=dict(request.args),
                headers=headers
            )
            return django_response.json(), django_response.status_code
        except requests.exceptions.RequestException as e:
            return {"message": str(e), "status": "fail", "data": None}, 500
        
    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            return {"message": "Missing JSON body", "status": "fail", "data": None}, 400
        try:
            django_response = requests.put(
                f"{DJANGO_BASE_URL}/my-profile/update/",
                json=data,
                headers=headers
            )
            return django_response.json(), django_response.status_code
        except requests.exceptions.RequestException as e:
            return {"message": str(e), "status": "fail", "data": None}, 500

    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return {"message": "Missing JSON body", "status": "fail", "data": None}, 400
        try:
            django_response = requests.post(
                f"{DJANGO_BASE_URL}/my-profile/change-password/",
                json=data,
                headers=headers
            )
            return django_response.json(), django_response.status_code
        except requests.exceptions.RequestException as e:
            return {"message": str(e), "status": "fail", "data": None}, 500



@profile_bp.route("/api/profile/image/", methods=["GET", "POST"])
@jwt_required
def profile_image():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }

    # ------------------ GET PROFILE IMAGE ------------------
    if request.method == "GET":
        try:
            django_response = requests.get(
                f"{DJANGO_BASE_URL}/profile/image/",
                headers=headers,
                params=request.args
            )
            return django_response.json(), django_response.status_code

        except requests.exceptions.RequestException as e:
            return {
                "status": "fail",
                "message": str(e),
                "data": None
            }, 500

    # ------------------ UPLOAD / UPDATE PROFILE IMAGE ------------------
    elif request.method == "POST":
        if "image" not in request.files:
            return {
                "status": "fail",
                "message": "No image file provided",
                "data": None
            }, 400

        image_file = request.files["image"]

        try:
            django_response = requests.post(
                f"{DJANGO_BASE_URL}/profile/image/",
                headers=headers,
                files={"image": image_file}
            )
            return django_response.json(), django_response.status_code

        except requests.exceptions.RequestException as e:
            return {
                "status": "fail",
                "message": str(e),
                "data": None
            }, 500
