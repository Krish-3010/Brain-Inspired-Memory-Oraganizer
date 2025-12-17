from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json, os, re
from auth import auth
from flask_cors import CORS
from difflib import SequenceMatcher

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.titles = []  

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word.lower():
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.titles.append(word)
        node.is_end = True

    def search(self, prefix):
        node = self.root
        for ch in prefix.lower():
            if ch not in node.children:
                return []
            node = node.children[ch]
        return list(set(node.titles))  

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.register_blueprint(auth)
CORS(app, supports_credentials=True)

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "notes.json")
os.makedirs(DATA_DIR, exist_ok=True)

def load_notes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_notes(notes):
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=4)

notes_data = load_notes()
trie = Trie()
for user, user_notes in notes_data.items():
    if isinstance(user_notes, dict):  
        for title in user_notes.keys():
            trie.insert(title)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth/')
@app.route('/auth')
def auth_page():
    return render_template('auth.html')

@app.route('/question')
def question_page():
    return render_template('question.html')

@app.route('/view_notes')
@app.route('/notes')
def notes_page():
    return render_template('view_notes.html')

@app.route('/create_note')
def create_note_page():
    return render_template('create_note.html')

@app.route('/save_note', methods=['POST'])
def save_note():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Login first!"}), 401

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user = session['user']

    if not title or not content:
        return jsonify({"status": "error", "message": "Title or content missing!"}), 400

    notes = load_notes()
    if user not in notes:
        notes[user] = {}

    notes[user][title] = content
    save_notes(notes)

    trie.insert(title)

    return jsonify({"status": "success", "message": "Note saved successfully!"})

@app.route('/get_notes', methods=['GET'])
def get_notes():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Login first!"}), 401

    user = session['user']
    notes = load_notes()
    user_notes = notes.get(user, {})
    return jsonify({"status": "success", "notes": user_notes})

@app.route('/search_notes', methods=['GET'])
def search_notes():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Login first!"}), 401

    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"status": "error", "message": "Empty query!"}), 400

    results = trie.search(query)
    user = session['user']
    notes = load_notes().get(user, {})

    matched = {t: notes[t] for t in results if t in notes}
    return jsonify({"status": "success", "results": matched})

@app.route('/delete_note', methods=['POST'])
def delete_note():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Login first!"}), 401

    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({"status": "error", "message": "Title missing!"}), 400

    user = session['user']
    notes = load_notes()

    if user not in notes or title not in notes[user]:
        return jsonify({"status": "error", "message": "Note not found!"}), 404
    
    del notes[user][title]

    save_notes(notes)

    global trie
    trie = Trie()
    for u, user_notes in notes.items():
        if isinstance(user_notes, dict):
            for t in user_notes.keys():
                trie.insert(t)

    return jsonify({"status": "success", "message": f"'{title}' deleted successfully!"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.html'))  

@app.route('/ask_question', methods=['POST'])
def ask_question():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Login first!"}), 401

    data = request.get_json() or {}
    query = (data.get('question') or "").strip()
    if not query:
        return jsonify({"status": "error", "message": "Question is empty!"}), 400

    user = session['user']
    notes = load_notes().get(user, {})

    if not notes:
        return jsonify({"status": "error", "message": "No notes found for this user!"}), 404

    stopwords = {"is","a","the","and","or","of","in","on","at","to","my","i","me","do","did","does","was","were","are"}
    def tokenize(text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = [t for t in text.split() if t and t not in stopwords]
        return tokens

    q_tokens = tokenize(query)
    q_token_set = set(q_tokens)

    candidates = []
    for title, content in notes.items():
        combined = f"{title} {content}"
        combined_tokens = tokenize(combined)
        if not combined_tokens:
            continue

        common = q_token_set.intersection(set(combined_tokens))
        if len(q_token_set) > 0:
            overlap_ratio = len(common) / len(q_token_set)
        else:
            overlap_ratio = 0.0

        seq_ratio = SequenceMatcher(None, query.lower(), combined.lower()).ratio()

        score = 0.7 * overlap_ratio + 0.3 * seq_ratio

        candidates.append((title, content, score, overlap_ratio, seq_ratio))

    candidates.sort(key=lambda x: x[2], reverse=True)

    THRESHOLD = 0.28
    results = []
    for title, content, score, overlap_ratio, seq_ratio in candidates:
        if score >= THRESHOLD:
            results.append({"title": title, "content": content, "score": round(score, 3)})
    results = results[:5]

    if not results:
        return jsonify({"status": "success", "results": [], "message": "No related notes found."})

    return jsonify({"status": "success", "results": results})

if __name__ == '__main__':
    app.run(debug=True)
