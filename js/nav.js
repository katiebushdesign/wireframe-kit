(function () {
  'use strict';

  var backdrop = document.getElementById('mega-backdrop');
  var panels = document.querySelectorAll('.mega-panel');
  var megaButtons = document.querySelectorAll('[data-mega]');
  var toggle = document.querySelector('.nav-toggle');
  var mobile = document.getElementById('nav-mobile');
  var body = document.body;
  var desktopMq = window.matchMedia('(min-width: 1024px)');

  function closeMega() {
    if (backdrop) backdrop.classList.remove('open');
    panels.forEach(function (p) {
      p.classList.remove('open');
    });
    megaButtons.forEach(function (b) {
      b.classList.remove('active');
    });
  }

  function closeMobile() {
    if (!mobile || !toggle) return;
    mobile.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    body.classList.remove('nav-mobile-open');
  }

  function closeAll() {
    closeMega();
    closeMobile();
  }

  megaButtons.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!desktopMq.matches) return;
      e.stopPropagation();
      var id = btn.getAttribute('data-mega');
      var panel = document.getElementById(id);
      var open = panel && panel.classList.contains('open');
      closeAll();
      if (!open && panel) {
        panel.classList.add('open');
        btn.classList.add('active');
        if (backdrop) backdrop.classList.add('open');
      }
    });
  });

  if (backdrop) {
    backdrop.addEventListener('click', closeAll);
  }

  if (toggle && mobile) {
    toggle.addEventListener('click', function () {
      var open = mobile.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      body.classList.toggle('nav-mobile-open', open);
      if (open) closeMega();
    });
    mobile.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMobile);
    });
  }

  desktopMq.addEventListener('change', function (e) {
    if (e.matches) closeMobile();
    else closeMega();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAll();
  });
})();
