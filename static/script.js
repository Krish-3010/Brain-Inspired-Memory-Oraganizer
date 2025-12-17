async function saveNote() {
    const titleInput = document.getElementById('title');
    const contentInput = document.getElementById('content');
    const title = titleInput.value.trim();
    const content = contentInput.value.trim();

    if (!title || !content) {
        alert("Please enter both title and content!");
        return;
    }

    const response = await fetch('/save_note', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content })
    });

    const result = await response.json();

    if (result.existing_content) {
        alert(result.message);
        contentInput.value = result.existing_content;
    } else {
        alert(result.message);
        titleInput.value = '';
        contentInput.value = '';
    }
}

async function fetchNotes() {
    const res = await fetch("/get_notes");
    const notes = await res.json();
    const list = document.getElementById("notesList");
    list.innerHTML = "";
    for (const [title, content] of Object.entries(notes)) {
        const li = document.createElement("li");
        li.textContent = `${title}: ${content}`;
        list.appendChild(li);
    }
}

async function registerUser() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!name || !email || !phone || !password) {
        alert("Please fill all fields!");
        return;
    }

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, phone, password })
    });

    const result = await response.json();
    alert(result.message);

    if (result.message.includes("successful")) {
        window.location.href = "/login";
    }
}

async function loginUser() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value.trim();

    if (!email || !password) {
        alert("Please enter both email and password!");
        return;
    }

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();
    alert(result.message);

    if (result.message.includes("successful")) {
        window.location.href = "/notes";
    }
}
