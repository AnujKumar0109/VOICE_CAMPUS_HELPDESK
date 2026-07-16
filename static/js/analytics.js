/**
 * analytics.js — Chart.js charts for the analytics dashboard.
 * chartLabels and chartCounts are injected by Jinja in analytics.html.
 */

(function () {
  'use strict';

  /* ── Bar Chart — Queries per Category ───────────────────── */
  const barCtx = document.getElementById('barChart');
  if (barCtx && typeof chartLabels !== 'undefined' && chartLabels.length > 0) {
    new Chart(barCtx, {
      type: 'bar',
      data: {
        labels: chartLabels,
        datasets: [{
          label: 'Queries',
          data: chartCounts,
          backgroundColor: 'rgba(13, 148, 136, 0.85)',
          borderRadius: 6,
          borderSkipped: false,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.parsed.y} queries`
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1 },
            grid: { color: '#e2e8f0' }
          },
          x: { grid: { display: false } }
        }
      }
    });
  }

  /* ── Doughnut Chart — Status Breakdown ──────────────────── */
  const doughCtx = document.getElementById('doughnutChart');
  if (doughCtx && typeof statsAnswered !== 'undefined') {
    new Chart(doughCtx, {
      type: 'doughnut',
      data: {
        labels: ['Answered', 'Unanswered'],
        datasets: [{
          data: [statsAnswered, statsUnanswered],
          backgroundColor: ['#0d9488', '#ef4444'],
          borderWidth: 0,
        }]
      },
      options: {
        responsive: true,
        cutout: '70%',
        plugins: {
          legend: { position: 'bottom', labels: { font: { size: 12 } } }
        }
      }
    });
  }

  /* ── Sidebar toggle for mobile ───────────────────────────── */
  const hamburger = document.getElementById('hamburger');
  const sidebar   = document.getElementById('sidebar');
  const overlay   = document.getElementById('overlay');

  if (hamburger && sidebar && overlay) {
    hamburger.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      overlay.classList.toggle('show');
    });
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('show');
    });
  }

})();
