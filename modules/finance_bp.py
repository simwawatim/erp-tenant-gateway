from flask import Blueprint, request, jsonify
import requests
from config import DJANGO_BASE_URL
from decorator.auth_decorator import jwt_required

finance_bp = Blueprint("finance_bp", __name__)

def safe_json(response):
    """Safely parse response as JSON, fallback to text or error."""
    try:
        return response.json()
    except ValueError:
        if response.text:
            return {"error": response.text}
        return {"error": "Empty response from server."}

# -----------------------------
# Trail Balance
# -----------------------------
@finance_bp.route("/api/trail/balance/", methods=["GET"])
@jwt_required
def trail_balance():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    if not tenant_id:
        return jsonify({"error": "Missing tenant_id"}), 400

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }

    try:
        django_response = requests.get(
            f"{DJANGO_BASE_URL}/trail/balance/",
            headers=headers,
            params=request.args.to_dict()
        )

        return safe_json(django_response), django_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@finance_bp.route("/api/receivables/", methods=["GET"])
@jwt_required
def receivables():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    if not tenant_id:
        return jsonify({"error": "Missing tenant_id"}), 400

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }

    try:
        django_response = requests.get(
            f"{DJANGO_BASE_URL}/receivables/",
            headers=headers,
            params=request.args.to_dict()
        )

        return safe_json(django_response), django_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@finance_bp.route("/api/payables/", methods=["GET"])
@jwt_required
def payables():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    if not tenant_id:
        return jsonify({"error": "Missing tenant_id"}), 400

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }

    try:
        django_response = requests.get(
            f"{DJANGO_BASE_URL}/payables/",
            headers=headers,
            params=request.args.to_dict()
        )

        return safe_json(django_response), django_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@finance_bp.route("/api/accounting-dashboard/", methods=["GET"])
@jwt_required
def accounting_dashboard():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    if not tenant_id:
        return jsonify({"error": "Missing tenant_id"}), 400

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }

    try:
        receivables_resp = requests.get(
            f"{DJANGO_BASE_URL}/receivables/",
            headers=headers
        )
        payables_resp = requests.get(
            f"{DJANGO_BASE_URL}/payables/",
            headers=headers
        )

        data = {
            "receivables": safe_json(receivables_resp).get("data", {}),
            "payables": safe_json(payables_resp).get("data", {})
        }

        return jsonify({
            "status": "success",
            "message": "Accounting dashboard fetched successfully",
            "data": data
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@finance_bp.route("/api/chart/of/accounts/", methods=["GET"])
@jwt_required
def chart_of_accounts():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    if not tenant_id:
        return jsonify({"error": "Missing tenant_id"}), 400

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }

    try:

        django_response = requests.get(
            f"{DJANGO_BASE_URL}/chart/of/accounts/",
            headers=headers,
        )
        data = safe_json(django_response)

        return jsonify({
            "status": "success",
            "message": "Chart of Accounts fetched successfully",
            "data": data.get("data", data)  
        }), django_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500



@finance_bp.route("/api/balance/sheet/", methods=["GET"])
@jwt_required
def balance_sheet():
    tenant_id = request.user.get("tenant_id")
    jwt_token = request.headers.get("Authorization")

    if not tenant_id:
        return jsonify({"error": "Missing tenant_id"}), 400

    headers = {
        "X-Tenant-ID": tenant_id,
        "Authorization": jwt_token
    }

    try:
        django_response = requests.get(
            f"{DJANGO_BASE_URL}/balance/sheet/",
            headers=headers,
        )

        data = safe_json(django_response)

        return jsonify({
            "status": "success",
            "message": "Balance Sheet fetched successfully",
            "data": data
        }), django_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
