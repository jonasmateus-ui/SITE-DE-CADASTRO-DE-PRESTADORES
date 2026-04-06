// ── TOBIAS CHAT ──────────────────────────────────────────────────────────────

function toggleChat() {
  const chat = document.getElementById('tobias-chat');
  chat.classList.toggle('open');
  if (chat.classList.contains('open')) {
    document.getElementById('msg').focus();
  }
}

document.getElementById('tobias-toggle')?.addEventListener('click', toggleChat);

document.getElementById('msg')?.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') enviar();
});

function addMsg(text, tipo) {
  const msgs = document.getElementById('msgs');
  const div = document.createElement('div');
  div.className = `msg-bubble msg-${tipo}`;
  div.textContent = text;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

async function enviar() {
  const input = document.getElementById('msg');
  const msg = input.value.trim();
  if (!msg) return;

  addMsg(msg, 'user');
  input.value = '';

  const typing = document.getElementById('typing');
  typing.style.display = 'block';

  try {
    const res = await fetch('/tobias', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensagem: msg })
    });
    const data = await res.json();
    typing.style.display = 'none';
    addMsg(data.resposta, 'bot');
  } catch (err) {
    typing.style.display = 'none';
    addMsg('Ops! Tive um probleminha técnico. Tente novamente.', 'bot');
  }
}

// ── TOAST ─────────────────────────────────────────────────────────────────────

function showToast(msg) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3500);
}