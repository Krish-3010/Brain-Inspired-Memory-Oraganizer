/* ============================================================
   BRAIN-INSPIRED MEMORY ORGANIZER — HAND-DRAWN UTILITIES
   ============================================================ */

/* ---- Theme Management ---- */
function getTheme() {
  return localStorage.getItem('theme') || 'light';
}

function loadTheme() {
  const theme = getTheme();
  if (theme === 'dark') {
    document.body.classList.add('dark-theme');
  } else {
    document.body.classList.remove('dark-theme');
  }
}

function toggleTheme() {
  const isDark = document.body.classList.toggle('dark-theme');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  
  // Re-render navbar to update toggle icon
  const activeKey = window.currentPageKey || '';
  buildNavbar(activeKey);
}

// Call theme load immediately on script execution
loadTheme();
document.addEventListener('DOMContentLoaded', loadTheme);

/* ---- Toast Notification System ---- */
function toast(message, type = 'info', duration = 3500) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  
  const icons = { 
    success: '✓', 
    error: '✕', 
    info: '●' 
  };
  
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  
  // Randomly select a wobbly border radius for the toast
  const wobbleOptions = [
    '255px 15px 225px 15px / 15px 225px 15px 255px',
    '15px 225px 15px 255px / 255px 15px 225px 15px',
    '20px 255px 15px 225px / 225px 15px 255px 20px'
  ];
  const selectedWobble = wobbleOptions[Math.floor(Math.random() * wobbleOptions.length)];
  el.style.borderRadius = selectedWobble;
  
  el.innerHTML = `
    <span class="toast-icon" style="margin-right:8px; font-weight:700;">${icons[type] || '●'}</span>
    <span style="flex-grow: 1;">${message}</span>
  `;
  
  container.appendChild(el);
  
  const remove = () => {
    el.classList.add('removing');
    el.addEventListener('animationend', () => el.remove(), { once: true });
  };
  
  const timer = setTimeout(remove, duration);
  el.addEventListener('click', () => { 
    clearTimeout(timer); 
    remove(); 
  });
}

/* ---- HTML Sanitizer ---- */
function escapeHtml(s) {
  return (s || '').toString()
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/* ---- Logout Transaction ---- */
function logout() {
  fetch('/auth/logout', { method: 'POST', credentials: 'include' })
    .finally(() => {
      localStorage.removeItem('user');
      location.href = '/auth';
    });
}

/* ---- Session cache getters ---- */
function getUser() {
  try { 
    return JSON.parse(localStorage.getItem('user')); 
  } catch { 
    return null; 
  }
}

/* ---- Sketched Navbar Builder ---- */
function buildNavbar(activePage = '') {
  window.currentPageKey = activePage; // Save key for theme toggle rerenders
  
  const nav = document.getElementById('navLinks');
  if (!nav) return;
  const u = getUser();
  const pages = [
    { href: '/', label: 'Home', key: 'home' },
    { href: '/notes', label: 'My Notes', key: 'notes' },
    { href: '/create_note', label: '+ Write Note', key: 'create' },
    { href: '/question', label: 'Consult Brain', key: 'question' },
  ];
  
  let html = pages.map(p =>
    `<a href="${p.href}" class="nav-link${activePage === p.key ? ' active' : ''}">${p.label}</a>`
  ).join('');

  // Dynamically set sun or moon SVG icon based on current theme state
  const isDark = document.body.classList.contains('dark-theme');
  const themeIcon = isDark 
    ? `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707-.707m12.728-12.728l-.707-.707M6.343 6.343l-.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" /></svg>` // Sun
    : `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>`; // Moon

  html += `
    <button class="theme-toggle-btn" onclick="toggleTheme()" title="Switch Light/Dark Mode" style="margin-left:6px;">
      ${themeIcon}
    </button>
  `;

  if (u) {
    html += `<a href="/profile"><img src="${escapeHtml(u.profile_pic || '/static/profile/default.png')}" class="nav-avatar" alt="profile" title="${escapeHtml(u.username)}"></a>`;
    html += `<button class="nav-btn-logout" onclick="logout()">Logout</button>`;
  } else {
    html += `<a href="/auth" class="btn btn-sm" style="margin-left:8px; border-width:2px; padding: 4px 12px; font-size:1.05rem;">Login</a>`;
  }
  
  nav.innerHTML = html;
}
