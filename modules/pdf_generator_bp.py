from flask import Blueprint, request, jsonify
import requests
from config import DJANGO_BASE_URL
from decorator.auth_decorator import jwt_required

document_bp = Blueprint("document_bp", __name__)
@document_bp.route("/api/document/", methods=["POST"])
@jwt_required
def documents():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")  

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token  
    }

    if request.method == "POST":
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
