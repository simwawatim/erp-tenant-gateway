from flask import Blueprint, request, jsonify
import requests
from config import DJANGO_BASE_URL  # Your Django API base URL
from decorator.auth_decorator import jwt_required

dashboard_bp = Blueprint("dashboard_bp", __name__)

def safe_json(response):
    """Safely parse response as JSON, fallback to text or error."""
    try:
        return response.json()
    except ValueError:
        if response.text:
            return {"error": response.text}
        return {"error": "Empty response from server."}


@dashboard_bp.route("/api/dashboard/stats/", methods=["POST"])
@jwt_required
def dashboard_stats():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")
    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }

    try:
        django_response = requests.post(
            f"{DJANGO_BASE_URL}/dashboard/stats/",
            headers=headers
        )

        return jsonify(safe_json(django_response)), django_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
