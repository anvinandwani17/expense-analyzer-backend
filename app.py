from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "database.json"

# ---------- Load & Save helpers ----------
def load_data():
    if not os.path.exists(DB_FILE):
        return {"expenses": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- API ROUTES ----------

@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = load_data()
    
    new_expense = request.json
    new_expense["id"] = len(data["expenses"]) + 1
    
    data["expenses"].append(new_expense)
    save_data(data)
    
    return jsonify({"message": "Expense added successfully!"})


@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    data = load_data()
    return jsonify(data["expenses"])


@app.route("/get_summary", methods=["GET"])
def get_summary():
    data = load_data()
    expenses = data["expenses"]

    total = sum(exp["amount"] for exp in expenses)

    category_summary = {}
    for exp in expenses:
        cat = exp["category"]
        category_summary[cat] = category_summary.get(cat, 0) + exp["amount"]

    return jsonify({
        "total_spent": total,
        "category_summary": category_summary
    })

@app.route("/", methods=["GET"])
def home():
    return "Expense Analyzer Backend Working!"

if __name__ == "__main__":
    app.run(debug=True)
