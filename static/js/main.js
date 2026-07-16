/**
 * main.js — Global JS: sidebar toggle, flash alert auto-dismiss, mobile overlay.
 */

(function () {
  'use strict';

  /* ── Sidebar toggle ──────────────────────────────────────── */
  const hamburger = document.getElementById('hamburger');
  const sidebar   = document.getElementById('sidebar');
  const overlay   = document.getElementById('overlay');

  if (hamburger && sidebar) {
    hamburger.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('show');
    });
  }
  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar && sidebar.classList.remove('open');
      overlay.classList.remove('show');
    });
  }

  /* ── Auto-dismiss flash alerts after 4 s ────────────────── */
  document.querySelectorAll('.flash-alert').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 4000);
  });

  /* ── Active sidebar link highlight ──────────────────────── */
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(el => {
    const href = el.getAttribute('href');
    if (href && path.startsWith(href) && href !== '/') {
      el.classList.add('active');
    }
  });

  /* ── Star rating UI ──────────────────────────────────────── */
  const stars = document.querySelectorAll('.star');
  const ratingInput = document.getElementById('rating-input');
  stars.forEach((star, idx) => {
    star.addEventListener('mouseover', () => highlightStars(idx));
    star.addEventListener('mouseout',  () => highlightStars(Number(ratingInput ? ratingInput.value : 0) - 1));
    star.addEventListener('click', () => {
      if (ratingInput) ratingInput.value = idx + 1;
      highlightStars(idx);
    });
  });

  function highlightStars(upTo) {
    stars.forEach((s, i) => {
      s.classList.toggle('selected', i <= upTo);
    });
  }

})();
