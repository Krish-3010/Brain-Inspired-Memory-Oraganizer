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

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route("/auth/profile_info", methods=["GET"])
def profile_info():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Login required"}), 401
    email = session['user']
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    if email not in users:
        return jsonify({"status": "error", "message": "User profile not found"}), 404
    user_data = users[email]
    return jsonify({
        "status": "success",
        "user": {
            "username": user_data.get("username"),
            "email": email,
            "phone": user_data.get("phone"),
            "profile_pic": user_data.get("profile_pic", "/static/profile/default.png")
        }
    })

@auth.route("/auth/update_profile", methods=["POST"])
def update_profile():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Login required"}), 401
    
    current_email = session['user']
    
    username = request.form.get("username", "").strip()
    new_email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    remove_avatar = request.form.get("remove_avatar", "false") == "true"
    
    if not username or not new_email or not phone:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
        
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
        
    if current_email not in users:
        return jsonify({"status": "error", "message": "User profile not found"}), 404
        
    # Check if changing email
    email_changed = (new_email != current_email)
    if email_changed:
        if new_email in users:
            return jsonify({"status": "error", "message": "New email is already registered"}), 400
            
    # Avatar update
    profile_pic = users[current_email].get("profile_pic", "/static/profile/default.png")
    
    if remove_avatar:
        profile_pic = "/static/profile/default.png"
    elif 'avatar' in request.files:
        file = request.files['avatar']
        if file and file.filename != '':
            if allowed_file(file.filename):
                import re
                clean_email = re.sub(r'[^a-zA-Z0-9]', '_', new_email)
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"avatar_{clean_email}.{ext}"
                upload_folder = "static/profile"
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                profile_pic = f"/static/profile/{filename}"
            else:
                return jsonify({"status": "error", "message": "Invalid file type. Only PNG, JPG, JPEG, GIF allowed."}), 400
                
    user_data = users[current_email]
    user_data["username"] = username
    user_data["phone"] = phone
    user_data["profile_pic"] = profile_pic
    
    if email_changed:
        # Move user key
        users[new_email] = user_data
        del users[current_email]
        
        # Update session
        session['user'] = new_email
        
        # Move notes if present
        notes_file = "data/notes.json"
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as nf:
                notes = json.load(nf)
            if current_email in notes:
                notes[new_email] = notes.pop(current_email)
                with open(notes_file, 'w') as nf:
                    json.dump(notes, nf, indent=4)
    else:
        users[current_email] = user_data
        
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)
        
    return jsonify({
        "status": "success",
        "message": "Profile updated successfully!",
        "user": {
            "username": username,
            "email": new_email,
            "phone": phone,
            "profile_pic": profile_pic
        }
    })
