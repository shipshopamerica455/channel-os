/* Genius Junkie — main.js */
var GJ = (function () {

  /* ── MOBILE NAV ── */
  function initMobileNav() {
    var burger = document.querySelector('.nav-burger');
    var mobileNav = document.getElementById('mobile-nav');
    if (!burger || !mobileNav) return;

    burger.addEventListener('click', function () {
      var isOpen = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!isOpen));
      if (isOpen) {
        mobileNav.setAttribute('hidden', '');
      } else {
        mobileNav.removeAttribute('hidden');
      }
    });
  }

  /* ── SUBSCRIBE POPUP ── */
  function initPopup(delaySeconds) {
    var popup = document.getElementById('subscribe-popup');
    var closeBtn = document.getElementById('popup-close');
    if (!popup) return;

    var delay = parseInt(delaySeconds, 10) || 30;
    if (delay === 0) return; // disabled

    // Don't show if already dismissed this session
    if (sessionStorage.getItem('gj_popup_dismissed')) return;

    var shown = false;

    function showPopup() {
      if (shown) return;
      shown = true;
      popup.removeAttribute('hidden');
      document.body.style.overflow = 'hidden';
    }

    function hidePopup() {
      popup.setAttribute('hidden', '');
      document.body.style.overflow = '';
      sessionStorage.setItem('gj_popup_dismissed', '1');
    }

    // Delay trigger
    var timer = setTimeout(showPopup, delay * 1000);

    // Exit-intent (desktop)
    document.addEventListener('mouseleave', function (e) {
      if (e.clientY < 10) showPopup();
    });

    // Close on button
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        clearTimeout(timer);
        hidePopup();
      });
    }

    // Close on overlay click
    popup.addEventListener('click', function (e) {
      if (e.target === popup) hidePopup();
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !popup.hasAttribute('hidden')) hidePopup();
    });

    // Handle Ghost Members form success
    var form = popup.querySelector('[data-members-form]');
    var successMsg = popup.querySelector('.popup-success');
    if (form && successMsg) {
      form.addEventListener('submit', function () {
        setTimeout(function () {
          // Ghost fires a custom event on success; we also check class
          if (form.classList.contains('success')) {
            form.style.display = 'none';
            successMsg.removeAttribute('hidden');
            setTimeout(hidePopup, 3000);
          }
        }, 1500);
      });
    }
  }

  /* ── CATEGORY PILL ACTIVE STATE ── */
  function initPills() {
    var pills = document.querySelectorAll('.cat-pills .pill');
    var currentPath = window.location.pathname;
    pills.forEach(function (pill) {
      var href = pill.getAttribute('href');
      if (href && currentPath.startsWith(href) && href !== '/') {
        pill.classList.add('active');
      } else if (href === '/' && currentPath === '/') {
        pill.classList.add('active');
      }
    });
  }

  /* ── READING PROGRESS BAR ── */
  function initProgressBar() {
    var postContent = document.querySelector('.gh-content');
    if (!postContent) return;

    var bar = document.createElement('div');
    bar.style.cssText = 'position:fixed;top:0;left:0;height:3px;background:var(--accent);z-index:9999;transition:width .1s linear;width:0%;pointer-events:none;';
    document.body.appendChild(bar);

    window.addEventListener('scroll', function () {
      var scrollTop = window.scrollY;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      var progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      bar.style.width = Math.min(progress, 100) + '%';
    }, { passive: true });
  }

  /* ── PUBLIC INIT ── */
  function init(options) {
    options = options || {};
    initMobileNav();
    initPills();
    initProgressBar();
    initPopup(options.popupDelay !== undefined ? options.popupDelay : 30);
  }

  return { init: init };

})();
