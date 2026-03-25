// scripts/main.js
// This script adds smooth scrolling for navigation links, a sticky header effect, and a dark/light theme toggle.

document.addEventListener('DOMContentLoaded', () => {
  // ---------- Smooth Scrolling ----------
  const navLinks = document.querySelectorAll('nav a[href^="#"]');
  navLinks.forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      const targetId = link.getAttribute('href');
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // ---------- Sticky Header (optional) ----------
  const header = document.querySelector('header');
  const SCROLL_THRESHOLD = 50; // px
  const onScroll = () => {
    if (window.scrollY > SCROLL_THRESHOLD) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', onScroll);
  // Run once in case page loads already scrolled
  onScroll();

  // ---------- Theme Toggle ----------
  const themeBtn = document.getElementById('theme-toggle');
  const THEME_KEY = 'preferred-theme';

  const applyTheme = theme => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem(THEME_KEY, theme);
    // Update button label and icon
    if (theme === 'dark') {
      themeBtn.setAttribute('aria-label', 'Switch to light theme');
      themeBtn.textContent = '🌞'; // sun icon for light mode
    } else {
      themeBtn.setAttribute('aria-label', 'Switch to dark theme');
      themeBtn.textContent = '🌙'; // moon icon for dark mode
    }
  };

  const toggleTheme = () => {
    const current = document.documentElement.dataset.theme || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    applyTheme(next);
  };

  // Load stored preference or default to light
  const stored = localStorage.getItem(THEME_KEY);
  const initialTheme = stored === 'dark' ? 'dark' : 'light';
  applyTheme(initialTheme);

  // Attach click handler
  if (themeBtn) {
    themeBtn.addEventListener('click', toggleTheme);
  }
});
