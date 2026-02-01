from flask import Blueprint, request, jsonify
import requests
from config import BASE_API, DJANGO_BASE_URL
from decorator.auth_decorator import jwt_required
from utils.header import get_headers

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



@items_imports_bp.route("/api/import/check/<int:item_id>/", methods=["GET"])
@jwt_required
def check_item(item_id):
    headers = get_headers()

    try:
        django_response = requests.get(
            f"{DJANGO_BASE_URL}/check/import/{item_id}/",
            headers=headers,
            timeout=10,
        )

        return jsonify(safe_json(django_response)), django_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": "Failed to communicate with import service.",
            "details": str(e)
        }), 500



@items_imports_bp.route("/api/import/update/exists/", methods=["GET", "POST"])
@jwt_required
def update_imported_item():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token  
    }


    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        try:
            django_response = requests.post(f"{DJANGO_BASE_URL}/imported-item/update/exists/", json=data, headers=headers)
            return django_response.json(), django_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500
        
        
        

@items_imports_bp.route("/api/save/imported/item/new/<int:item_id>", methods=["PUT"])
@jwt_required
def update_imported_item_to_new(item_id):
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")
    
    if not item_id:
        return jsonify({"error": "Missing item ID in URL"}), 400

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token  
    }


    if request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        try:
            django_response = requests.put(f"{DJANGO_BASE_URL}/save/imported/item/new/{item_id}/", json=data, headers=headers)
            return django_response.json(), django_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500