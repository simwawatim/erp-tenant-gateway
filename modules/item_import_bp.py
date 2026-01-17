from flask import Blueprint, request, jsonify
import requests
from config import BASE_API, DJANGO_BASE_URL
from decorator.auth_decorator import jwt_required

items_imports_bp = Blueprint("items_imports_bp", __name__)

def safe_json(response):
    try:
        return response.json()
    except ValueError:
        if response.text:
            return {"error": response.text}
        return {"error": "Empty response from server."}


@items_imports_bp.route("/api/imports/", methods=["GET"])
@jwt_required
def items_imports():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")
    headers = {"X-Tenant-ID": tenant_id, "Authorization": jwt_token}

    try:
        if request.method == "GET":
            django_response = requests.get(f"{DJANGO_BASE_URL}/imports/", params=dict(request.args), headers=headers)
            return jsonify(safe_json(django_response)), django_response.status_code
        else:
            return jsonify({"error": "Method not allowed"}), 405

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


