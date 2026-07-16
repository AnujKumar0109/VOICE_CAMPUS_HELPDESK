/**
 * chat.js — AJAX chat interface with voice input support.
 */

(function () {
  'use strict';

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const chatMessages = document.getElementById('chat-messages');
  const chatInput    = document.getElementById('chat-input');
  const sendBtn      = document.getElementById('send-btn');
  const chatMicBtn   = document.getElementById('chat-mic-btn');

  let recognition = null;
  let isListening = false;

  /* ── Speech Recognition for chat ────────────────────────── */
  if (SpeechRecognition && chatMicBtn) {
    recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;

    recognition.onstart = () => {
      isListening = true;
      chatMicBtn.classList.add('listening');
      chatMicBtn.title = 'Listening…';
    };

    recognition.onresult = (e) => {
      chatInput.value = e.results[0][0].transcript;
      chatInput.focus();
    };

    recognition.onerror = () => stopListening();
    recognition.onend   = () => stopListening();

    chatMicBtn.addEventListener('click', () => {
      if (isListening) { recognition.stop(); }
      else { try { recognition.start(); } catch(e){} }
    });
  } else if (chatMicBtn) {
    chatMicBtn.style.opacity = '0.4';
    chatMicBtn.title = 'Voice not supported';
  }

  function stopListening() {
    isListening = false;
    if (chatMicBtn) chatMicBtn.classList.remove('listening');
  }

  /* ── Send message ────────────────────────────────────────── */
  function sendMessage() {
    const question = chatInput.value.trim();
    if (!question) return;

    appendMessage(question, 'user');
    chatInput.value = '';
    chatInput.style.height = 'auto';
    showTyping();

    fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, speak: false }),
    })
      .then(r => r.json())
      .then(data => {
        removeTyping();
        appendBotMessage(data);
      })
      .catch(() => {
        removeTyping();
        appendMessage('Sorry, an error occurred. Please try again.', 'bot');
      });
  }

  /* ── Append user message ─────────────────────────────────── */
  function appendMessage(text, sender) {
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const row = document.createElement('div');
    row.className = `msg-row ${sender === 'user' ? 'user-msg' : 'bot-msg'}`;

    const icon = sender === 'user' ? 'person-fill' : 'robot';
    row.innerHTML = `
      <div class="msg-avatar"><i class="bi bi-${icon}"></i></div>
      <div>
        <div class="msg-bubble">${escHtml(text)}</div>
        <div class="msg-meta">${now}</div>
      </div>`;
    chatMessages.appendChild(row);
    scrollBottom();
  }

  /* ── Append bot message with meta ────────────────────────── */
  function appendBotMessage(data) {
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const row = document.createElement('div');
    row.className = 'msg-row bot-msg';

    let suggestHtml = '';
    if (data.suggestions && data.suggestions.length > 0) {
      suggestHtml = `<div class="suggestions-box visible" style="margin-top:8px">
        <div style="font-size:11px;color:var(--text-muted);margin-bottom:4px">Did you mean?</div>
        ${data.suggestions.map(s =>
          `<span class="suggestion-chip" onclick="fillChat(this)">${escHtml(s)}</span>`
        ).join('')}
      </div>`;
    }

    let statusHtml = data.status === 'answered'
      ? `<span class="badge badge-success">Answered</span>`
      : `<span class="badge badge-warning">Unresolved</span>`;

    row.innerHTML = `
      <div class="msg-avatar"><i class="bi bi-robot"></i></div>
      <div>
        <div class="msg-bubble">
          ${escHtml(data.answer)}
          ${data.intent ? `<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap">
            <span class="badge badge-info">${data.intent}</span>
            ${statusHtml}
          </div>` : ''}
          ${suggestHtml}
        </div>
        <div class="msg-meta">${now}</div>
      </div>`;
    chatMessages.appendChild(row);
    scrollBottom();
  }

  /* ── Typing indicator ────────────────────────────────────── */
  function showTyping() {
    const row = document.createElement('div');
    row.className = 'msg-row bot-msg';
    row.id = 'typing-row';
    row.innerHTML = `
      <div class="msg-avatar"><i class="bi bi-robot"></i></div>
      <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>`;
    chatMessages.appendChild(row);
    scrollBottom();
  }

  function removeTyping() {
    const row = document.getElementById('typing-row');
    if (row) row.remove();
  }

  /* ── Event listeners ─────────────────────────────────────── */
  if (sendBtn) sendBtn.addEventListener('click', sendMessage);

  if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
    // Auto-resize textarea
    chatInput.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 80) + 'px';
    });
  }

  /* ── Helpers ─────────────────────────────────────────────── */
  function scrollBottom() {
    if (chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function escHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // Global for suggestion chips inside dynamically added content
  window.fillChat = function(el) {
    chatInput.value = el.textContent;
    chatInput.focus();
  };

  // Initial scroll to bottom (for existing history)
  scrollBottom();

})();
