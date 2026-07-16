/**
 * voice.js — Web Speech API mic integration for voice query page.
 * Works in Chrome/Edge. Falls back gracefully in unsupported browsers.
 */

(function () {
  'use strict';

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const micBtn   = document.getElementById('mic-hero');
  const statusEl = document.getElementById('voice-status');
  const queryIn  = document.getElementById('query-input');
  const submitBtn= document.getElementById('submit-btn');
  const answerBox= document.getElementById('answer-box');
  const answerTxt= document.getElementById('answer-text');
  const intentBadge = document.getElementById('intent-badge');
  const scoreBadge  = document.getElementById('score-badge');
  const suggestBox  = document.getElementById('suggestions-box');
  const suggestList = document.getElementById('suggestion-list');
  const speakToggle = document.getElementById('speak-toggle');
  const rateRange   = document.getElementById('rate-range');

  let recognition = null;
  let isListening = false;

  /* ── Init Speech Recognition ─────────────────────────────── */
  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      isListening = true;
      micBtn.classList.add('listening');
      setStatus('Listening… speak your question', 'active');
    };

    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      queryIn.value = transcript;
      setStatus(`Heard: "${transcript}"`, 'active');
      submitQuery(transcript);
    };

    recognition.onerror = (e) => {
      setStatus('Mic error: ' + e.error + '. Try typing instead.', 'error');
      stopListening();
    };

    recognition.onend = () => stopListening();
  } else {
    if (micBtn) {
      micBtn.style.opacity = '0.5';
      micBtn.title = 'Speech recognition not supported in this browser.';
    }
    setStatus('Voice input not supported. Use text below.', 'error');
  }

  /* ── Mic Button Click ────────────────────────────────────── */
  if (micBtn) {
    micBtn.addEventListener('click', () => {
      if (!recognition) return;
      if (isListening) {
        recognition.stop();
      } else {
        try {
          recognition.start();
        } catch (err) {
          setStatus('Cannot start mic: ' + err.message, 'error');
        }
      }
    });
  }

  /* ── Text Submit ─────────────────────────────────────────── */
  if (submitBtn) {
    submitBtn.addEventListener('click', () => {
      const q = queryIn.value.trim();
      if (q) submitQuery(q);
    });
  }

  if (queryIn) {
    queryIn.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const q = queryIn.value.trim();
        if (q) submitQuery(q);
      }
    });
  }

  /* ── Core Submit Logic ───────────────────────────────────── */
  function submitQuery(question) {
    setStatus('Processing…', 'active');
    showLoading(true);
    hideAnswer();

    const speak = speakToggle ? speakToggle.checked : false;
    const rate  = rateRange   ? parseInt(rateRange.value) : 150;

    fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, speak, rate }),
    })
      .then(r => r.json())
      .then(data => {
        showLoading(false);
        displayAnswer(data);
        setStatus('Answer ready.', 'active');
        queryIn.value = '';
      })
      .catch(() => {
        showLoading(false);
        setStatus('Server error. Please try again.', 'error');
      });
  }

  /* ── Display Answer ──────────────────────────────────────── */
  function displayAnswer(data) {
    if (answerTxt)   answerTxt.textContent = data.answer || 'No answer found.';
    if (answerBox)   answerBox.classList.add('visible');
    if (intentBadge) intentBadge.textContent = data.intent || '';
    if (scoreBadge)  scoreBadge.textContent  = 'Score: ' + (data.score || 0);

    if (data.suggestions && data.suggestions.length > 0 && suggestBox && suggestList) {
      suggestList.innerHTML = '';
      data.suggestions.forEach(s => {
        const chip = document.createElement('span');
        chip.className = 'suggestion-chip';
        chip.textContent = s;
        chip.addEventListener('click', () => {
          queryIn.value = s;
          submitQuery(s);
        });
        suggestList.appendChild(chip);
      });
      suggestBox.classList.add('visible');
    } else if (suggestBox) {
      suggestBox.classList.remove('visible');
    }
  }

  /* ── Helpers ─────────────────────────────────────────────── */
  function stopListening() {
    isListening = false;
    if (micBtn) micBtn.classList.remove('listening');
  }

  function setStatus(msg, type) {
    if (!statusEl) return;
    statusEl.textContent = msg;
    statusEl.className = 'voice-status ' + (type || '');
  }

  function hideAnswer() {
    if (answerBox)  answerBox.classList.remove('visible');
    if (suggestBox) suggestBox.classList.remove('visible');
  }

  function showLoading(on) {
    if (!submitBtn) return;
    if (on) {
      submitBtn.innerHTML = '<span class="spinner"></span>';
      submitBtn.disabled = true;
    } else {
      submitBtn.innerHTML = '<i class="bi bi-send-fill"></i> Ask';
      submitBtn.disabled = false;
    }
  }

  /* ── Rate range label ────────────────────────────────────── */
  if (rateRange) {
    const rateLabel = document.getElementById('rate-label');
    rateRange.addEventListener('input', () => {
      if (rateLabel) rateLabel.textContent = rateRange.value + ' wpm';
    });
  }

})();
