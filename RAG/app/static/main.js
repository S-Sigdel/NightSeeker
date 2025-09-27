const chatEl = document.getElementById('chat');
const formEl = document.getElementById('form');
const inputEl = document.getElementById('input');
const useWebEl = document.getElementById('use_web');
const reindexEl = document.getElementById('reindex');

function addMessage(role, content, extraClass = '') {
  const wrap = document.createElement('div');
  wrap.className = `msg ${extraClass}`;
  const roleEl = document.createElement('div');
  roleEl.className = 'role';
  roleEl.textContent = role;
  const contentEl = document.createElement('div');
  contentEl.className = 'content';
  contentEl.textContent = content;
  wrap.appendChild(roleEl);
  wrap.appendChild(contentEl);
  chatEl.appendChild(wrap);
  chatEl.scrollTop = chatEl.scrollHeight;
  return contentEl;
}

async function sendMessage(message) {
  const userEl = addMessage('You', message);
  const loadingEl = addMessage('Bot', 'Thinking...', 'loading');
  try {
    const res = await fetch('/api/chat', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, use_web: !!(useWebEl && useWebEl.checked) })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    loadingEl.textContent = data.answer || '';
    loadingEl.classList.remove('loading');
    if (Array.isArray(data.sources) && data.sources.length) {
      const srcEl = document.createElement('div');
      srcEl.className = 'sources';
      srcEl.textContent = 'Sources: ' + data.sources.map(s => s.source).join(', ');
      loadingEl.parentElement.appendChild(srcEl);
    }
    if (Array.isArray(data.web) && data.web.length) {
      const webEl = document.createElement('div');
      webEl.className = 'sources';
      webEl.textContent = 'Web: ' + data.web.map(w => w.title || w.url).join(', ');
      loadingEl.parentElement.appendChild(webEl);
    }
  } catch (e) {
    loadingEl.textContent = 'Error: ' + (e && e.message ? e.message : 'Unknown error');
    loadingEl.classList.add('error');
  }
}

formEl.addEventListener('submit', (e) => {
  e.preventDefault();
  const message = inputEl.value.trim();
  if (!message) return;
  inputEl.value = '';
  sendMessage(message);
});

reindexEl.addEventListener('click', async () => {
  addMessage('System', 'Rebuilding index...');
  try {
    const res = await fetch('/api/ingest', { method: 'POST' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    addMessage('System', 'Index rebuilt.');
  } catch (e) {
    addMessage('System', 'Reindex failed: ' + (e && e.message ? e.message : 'Unknown error'));
  }
});

