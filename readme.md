# 🧠 Brain-Inspired Memory Organizer

> A full-stack web application that mimics how the human brain stores and retrieves memories — featuring Trie-based autocomplete search, semantic Q&A over your notes, multi-user authentication, and a hand-drawn sketchbook UI.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![CSS3](https://img.shields.io/badge/CSS3-Hand--Drawn_UI-1572B6?style=for-the-badge&logo=css3&logoColor=white)

---

## 🧠 Overview

**Brain-Inspired Memory Organizer** is a web application that reimagines note-taking through the lens of cognitive science. Rather than a flat list of notes, it builds a mental model of your knowledge — letting you search by prefix, ask natural-language questions, and retrieve semantically relevant content from your personal memory bank.

This project demonstrates key Computer Science and Web Development concepts:

- **Data Structures** — Trie for real-time prefix-based autocomplete search
- **NLP / Information Retrieval** — Token overlap + sequence similarity scoring for Q&A
- **Full-Stack Web Development** — Flask backend with REST APIs, vanilla JS frontend
- **Authentication & Sessions** — Blueprint-based multi-user auth with Flask sessions
- **UI/UX Design** — Custom hand-drawn / sketchbook aesthetic with dark mode support

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Trie-Powered Search** | Real-time prefix autocomplete built on a custom Trie data structure |
| 🤔 **Ask Your Notes** | Natural-language Q&A that scores notes by token overlap and sequence similarity |
| 🔐 **Multi-User Auth** | Secure user registration, login, and session management via Flask Blueprints |
| 👤 **Profile Management** | User profile creation and updating within the app |
| 📝 **Full Note CRUD** | Create, view, and delete notes — with character count and live feedback |
| 🌙 **Dark / Light Mode** | Theme toggle with persistence via `localStorage` |
| 🎨 **Hand-Drawn UI** | Wobbly borders, sticky-note cards, tape decorations, and ledger-paper textures |
| 🍞 **Toast Notifications** | Animated, dismissible notifications with randomized wobbly border radii |
| 🧭 **Dynamic Navbar** | Shared script-driven navbar that highlights the active page |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        CLIENT SIDE                           │
│                                                              │
│  Browser (HTML + CSS + Vanilla JS)                           │
│       │                                                      │
│       ├── /static/style.css    → Hand-drawn UI styles        │
│       ├── /static/script.js    → Shared utilities & navbar   │
│       └── /templates/*.html    → Jinja2 page templates       │
│                                                              │
│  User Actions: Create Note / Search / Ask Question / Auth    │
│       │                                                      │
│       ▼                                                      │
│  fetch() / form submit ─────────────────────────────────►   │
│                          REST API (JSON over HTTP)           │
└──────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                        SERVER SIDE                           │
│                                                              │
│  Flask App (app.py)                                          │
│       │                                                      │
│       ├── Blueprint: auth.py   → /auth/* routes              │
│       │                                                      │
│       ├── /save_note    → Persist note + insert into Trie    │
│       ├── /get_notes    → Return all notes for session user  │
│       ├── /search_notes → Trie.search(prefix) → filter notes │
│       ├── /delete_note  → Remove note + rebuild Trie         │
│       └── /ask_question → Tokenize → Score → Return top 5   │
│                                                              │
│  In-Memory: Trie (rebuilt on startup & on delete)           │
│  Persistent: data/notes.json (per-user JSON store)          │
└──────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│                                                              │
│  data/notes.json                                             │
│  { "username": { "Note Title": "Note Content", ... } }      │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Brain-Inspired-Memory-Organizer/
│
├── app.py                  # Main Flask app, routes, Trie, Q&A engine
├── auth.py                 # Auth Blueprint — register, login, logout
│
├── static/
│   ├── script.js           # Shared utilities: navbar, toast, theme, logout
│   └── style.css           # Hand-drawn UI design system & dark mode
│
├── templates/
│   ├── index.html          # Landing / home page
│   ├── auth.html           # Login & register page
│   ├── create_note.html    # Note creation with live char count
│   ├── view_notes.html     # Note listing & deletion
│   ├── question.html       # Ask-your-notes interface
│   └── profile.html        # User profile view & update
│
├── data/
│   └── notes.json          # Persistent per-user note store (auto-created)
│
├── profile/                # User profile assets/data
└── .gitignore
```

---

## 🔄 How It Works

### 📝 Note Storage
1. User logs in and is identified by their session username.
2. Notes are saved as `{ username: { title: content } }` in `data/notes.json`.
3. On every save, the note title is inserted into an in-memory **Trie**.

### 🔍 Trie Search
1. Each note title is inserted character-by-character into the Trie at startup and on save.
2. On search, `Trie.search(prefix)` traverses to the prefix node and collects all titles stored along that path.
3. Results are filtered to only include notes belonging to the logged-in user.

### 🤔 Ask Your Notes (Q&A Engine)
1. The user types a natural-language question.
2. Both the question and each note's `title + content` are **tokenized** (lowercased, punctuation removed, stopwords stripped).
3. Each note is scored: `score = 0.7 × token_overlap_ratio + 0.3 × sequence_similarity_ratio`.
4. Notes scoring above a threshold (`0.28`) are returned, sorted by score, top 5 max.

### 🔐 Authentication
1. `auth.py` is a Flask Blueprint mounted at `/auth`.
2. On login, the username is stored in `session['user']`.
3. Protected routes check `if 'user' not in session` and return `401` or redirect.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **pip**

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Krish-3010/Brain-Inspired-Memory-Oraganizer.git
cd Brain-Inspired-Memory-Oraganizer

# 2. Install dependencies
pip install flask flask-cors

# 3. Run the app
python app.py
```

The app starts in debug mode at `http://127.0.0.1:5000`.

---

## 💻 Usage

### Step 1 — Register / Login

Navigate to `http://127.0.0.1:5000/auth` and create an account or log in.

---

### Step 2 — Create a Note

Go to **Write Note** and enter a title and content. A live character counter tracks your input.

```
Title:   "Photosynthesis"
Content: "The process by which plants convert sunlight into glucose..."
```

Click **Save Note** — a toast notification confirms success.

---

### Step 3 — Search Notes

Use the search bar to find notes by prefix:

```
Search: "Photo"
→ Returns: "Photosynthesis", "Photography basics", ...
```

---

### Step 4 — Ask Your Notes

Navigate to **Ask** and type a natural-language question:

```
Question: "How do plants make food?"
→ Returns: "Photosynthesis" (score: 0.74), ...
```

---

### Step 5 — View & Delete Notes

The **View Notes** page lists all your notes as card tiles. Click delete to remove one — the Trie is automatically rebuilt.

---

## 🎨 UI Design System

The interface uses a **hand-drawn / sketchbook** aesthetic built entirely in CSS:

| Element | Design Detail |
|---|---|
| **Borders** | Wobbly `border-radius` values (e.g. `255px 15px 225px 15px / 15px 225px 15px 255px`) |
| **Note Cards** | Sticky-note style with tape decoration (`::before` pseudo-element) |
| **Shadows** | Hard offset box-shadows (`4px 4px 0px var(--color-border)`) for a stamped look |
| **Typography** | Handwriting-style font via CSS variable `--font-heading` |
| **Toasts** | Animated slide-in notifications with randomized wobbly border radii |
| **Dark Mode** | Full dark theme via `.dark-theme` class toggled on `<body>`, persisted in `localStorage` |
| **Textures** | Ledger-paper background on note creation page |

---

## 🛠️ Technical Details

### `app.py`

| Component | Detail |
|---|---|
| `TrieNode` | Children dict + `is_end` flag + `titles` list for path-level storage |
| `Trie.insert(word)` | Inserts each character; appends title at every node along the path |
| `Trie.search(prefix)` | Traverses to prefix node, returns deduplicated title list |
| `load_notes()` / `save_notes()` | JSON file I/O for persistent storage |
| `ask_question()` | Tokenizes + scores with `SequenceMatcher` and overlap ratio |
| `delete_note()` | Deletes from JSON + fully rebuilds Trie from remaining notes |
| `CORS` | `flask-cors` with `supports_credentials=True` for session-aware cross-origin requests |

### `auth.py`

| Component | Detail |
|---|---|
| Flask Blueprint | Mounted at `/auth` prefix, self-contained auth logic |
| Session management | `session['user']` set on login, cleared on logout |

### `static/script.js`

| Component | Detail |
|---|---|
| `buildNavbar(activePage)` | Dynamically generates the navbar and highlights the current page |
| `toast(message, type)` | Creates animated toast notifications with random wobbly borders |
| `toggleTheme()` | Adds/removes `.dark-theme` on `<body>` and persists to `localStorage` |
| `getUser()` | Reads cached user from `localStorage` for client-side display |
| `logout()` | POSTs to `/auth/logout`, clears local state, redirects to `/auth` |

---

## 📸 Screenshots

**Dash Board:**
<img width="1898" height="836" alt="image" src="https://github.com/user-attachments/assets/72542d28-a816-4140-99df-c47db89ace04" />

---

**My Notes:**
<img width="1900" height="833" alt="image" src="https://github.com/user-attachments/assets/20b5be75-014b-4a4e-b031-0992678f4cf3" />

---

**+Write Notes:**
<img width="1900" height="836" alt="image" src="https://github.com/user-attachments/assets/65b1472e-64be-481b-b0d7-b3071dec8a36" />

---

**Consult Brain:**
<img width="1900" height="837" alt="image" src="https://github.com/user-attachments/assets/8bbb8ed4-aee7-4a8d-a707-d739084bbe92" />

---

**Profile:**
<img width="1901" height="837" alt="image" src="https://github.com/user-attachments/assets/e430b752-7057-49b2-8e68-8721eb0fb6e8" />

---

**Dark Mode:**
<img width="1892" height="837" alt="image" src="https://github.com/user-attachments/assets/c89ae790-1192-41eb-9025-4e52eff4d856" />

---

## 🔮 Future Enhancements

- [ ] **Vector Embeddings** — Replace token overlap with semantic similarity using sentence embeddings
- [ ] **Tagging System** — Attach tags to notes and filter by topic
- [ ] **Markdown Support** — Render note content as formatted Markdown
- [ ] **Export Notes** — Download notes as PDF or plain text
- [ ] **Database Backend** — Replace `notes.json` with SQLite or PostgreSQL
- [ ] **Spaced Repetition** — Surface notes for review based on forgetting curves
- [ ] **Rich Text Editor** — Inline formatting, images, and code blocks in notes
- [ ] **Docker Support** — Containerize for easy deployment

---

## 👨‍💻 Author

**Krish Mojidra**
B.Tech Computer Science Engineering | Nirma University
📧 krishmojidra3010@gmail.com

---

> ⭐ If you found this project useful or interesting, please consider giving it a star!
