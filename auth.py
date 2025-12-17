from flask import Blueprint, render_template, request, jsonify, session
import json, os

auth = Blueprint('auth', __name__)
USERS_FILE = "data/users.json"

os.makedirs("data", exist_ok=True)
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)

@auth.route("/auth")
def auth_page():
    return render_template("auth.html")

@auth.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    if not all([username, email, phone, password]):
        return jsonify({"status": "error", "message": "All fields required"}), 400

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    if email in users:
        return jsonify({"status": "exists", "message": "User already registered!"})

    users[email] = {
        "username": username,
        "phone": phone,
        "password": password,
        "profile_pic": "/static/profile/default.png"
    }

    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

    return jsonify({"status": "success", "message": "Registration successful!"})

@auth.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    if email not in users:
        return jsonify({"status": "error", "message": "User not found"}), 404

    if users[email]["password"] != password:
        return jsonify({"status": "error", "message": "Incorrect password"}), 401

    user_info = users[email]
    session['user'] = email  

    return jsonify({
        "status": "success",
        "message": "Login successful!",
        "user": {
            "email": email,
            "username": user_info["username"],
            "profile_pic": user_info.get("profile_pic", "/static/profile/default.png")
        }
    })

@auth.route("/auth/logout", methods=["POST"])
def logout():
    session.pop('user', None)
    return jsonify({"status": "success", "message": "Logged out successfully!"})
