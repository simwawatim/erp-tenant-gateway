from flask import Blueprint, request, jsonify
import requests
from config import DJANGO_BASE_URL
from decorator.auth_decorator import jwt_required

permissions_bp = Blueprint("permissions_bp", __name__)

@permissions_bp.route("/api/permissions/", methods=["GET", "POST", "PUT"])
@jwt_required
def permissions():

    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization") 

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }


    if request.method == "GET":
        try:
            params = request.args.to_dict()
            django_response = requests.get(
                f"{DJANGO_BASE_URL}/groups/permissions/",
                params=params,
                headers=headers,
                timeout=10
            )
            return jsonify(django_response.json()), django_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"status": "fail", "message": str(e), "data": None}), 500

    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"status": "fail", "message": "Missing JSON body", "data": None}), 400
        try:
            django_response = requests.post(
                f"{DJANGO_BASE_URL}/groups/permissions/",
                json=data,
                headers=headers,
                timeout=10
            )
            return jsonify(django_response.json()), django_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"status": "fail", "message": str(e), "data": None}), 500


    elif request.method == "PUT":
        data = request.get_json()
        if not data or "user_id" not in data or "permissions" not in data:
            return jsonify({
                "status": "fail",
                "message": "Missing 'user_id' or 'permissions' in JSON body",
                "data": None
            }), 400
        user_id = data["user_id"]
        try:
            django_response = requests.put(
                f"{DJANGO_BASE_URL}/user/{user_id}/permissions/",
                json={"permissions": data["permissions"]},
                headers=headers,
                timeout=10
            )
            return jsonify(django_response.json()), django_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"status": "fail", "message": str(e), "data": None}), 500



@permissions_bp.route("/api/user/<int:user_id>/permissions/", methods=["GET", "PUT"])
@jwt_required
def user_permissions(user_id):
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token,
        "Content-Type": "application/json"
    }
    if request.method == "GET":
        try:
            django_response = requests.get(
                f"{DJANGO_BASE_URL}/user/{user_id}/permissions/",
                headers=headers,
            )
            return jsonify(django_response.json()), django_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"status": "fail", "message": str(e), "data": None}), 500

    elif request.method == "PUT":
        payload = request.get_json()
        if not payload or "permissions" not in payload:
            return jsonify({
                "status": "fail",
                "message": "Missing 'permissions' in JSON body",
                "data": None
            }), 400

        try:
            django_response = requests.put(
                f"{DJANGO_BASE_URL}/user/{user_id}/permissions/",
                headers=headers,
                json={"permissions": payload["permissions"]}, 
                timeout=50
            )
            return jsonify(django_response.json()), django_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({
                "status": "fail",
                "message": str(e),
                "data": None
            }), 500