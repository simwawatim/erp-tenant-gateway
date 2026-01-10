from flask import Blueprint, request, jsonify
import requests
from config import DJANGO_BASE_URL
from decorator.auth_decorator import jwt_required
from utils.header import get_headers

proforma_bp = Blueprint("proforma_bp", __name__)


def safe_json(response):
    """Safely parse response as JSON, fallback to text or error."""
    try:
        return response.json()
    except ValueError:
        if response.text:
            return {"error": response.text}
        return {"error": "Empty response from server."}


@proforma_bp.route("/api/proformas/", methods=["GET", "POST"])
@jwt_required
def proformas():
    headers = get_headers()

    if request.method == "GET":
        try:
            django_response = requests.get(
                f"{DJANGO_BASE_URL}/proformas/", params=dict(request.args), headers=headers
            )
            return jsonify(safe_json(django_response)), django_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        try:
            django_response = requests.post(
                f"{DJANGO_BASE_URL}/proformas/", json=data, headers=headers
            )
            return jsonify(safe_json(django_response)), django_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500



@proforma_bp.route("/api/proformas/<int:proforma_id>/", methods=["GET", "DELETE"])
@jwt_required
def proforma_by_id(proforma_id):
    headers = get_headers()

    try:
        if request.method == "GET":
            django_response = requests.get(
                f"{DJANGO_BASE_URL}/proformas/{proforma_id}/", headers=headers
            )
        elif request.method == "DELETE":
            django_response = requests.delete(
                f"{DJANGO_BASE_URL}/proformas/{proforma_id}/delete/", headers=headers
            )
        else:
            return jsonify({"error": "Method not allowed"}), 405

        return jsonify(safe_json(django_response)), django_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
