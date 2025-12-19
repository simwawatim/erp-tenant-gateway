from flask import Flask, request, make_response
from flask_cors import CORS

from modules.sales_bp import sales_bp
from modules.items_bp import items_bp
from modules.customers import customers_bp
from modules.users import users_bp
from modules.tenants import tenants_bp
from modules.stock_bp import stock_bp
from modules.stock_master import stock_master_bp
from modules.supplier import suppliers_bp
from modules.purchase_bp import purchase_bp
from modules.quotation_bp import quotation_bp

app = Flask(__name__)

# Configure CORS explicitly for your frontends
CORS(
    app,
    resources={r"/api/*": {"origins": [
        "http://localhost:3000",
        "https://bongo-erp-frontend-nextjs.vercel.app"
    ]}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

# Prevent redirect issues (trailing slashes)
app.url_map.strict_slashes = False

# Register all blueprints WITHOUT prefixes
app.register_blueprint(customers_bp)
app.register_blueprint(users_bp)
app.register_blueprint(tenants_bp)
app.register_blueprint(items_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(stock_master_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(quotation_bp)
app.register_blueprint(suppliers_bp)

# Health check route
@app.route("/")
def health():
    return {"status": "API running"}, 200

# Handle preflight OPTIONS requests globally
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin"))
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
