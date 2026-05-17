// CJB Web Development - Site Interactions

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initHeaderScroll();
    initSmoothScroll();
    initAnimations();
    initCookieBanner();
});

// Mobile menu toggle
function initMobileMenu() {
    const toggle = document.getElementById('mobileToggle');
    const menu = document.getElementById('mobileMenu');

    if (!toggle || !menu) return;

    toggle.addEventListener('click', () => {
        const isOpen = menu.classList.contains('mobile-menu-open');
        if (isOpen) {
            menu.classList.remove('mobile-menu-open');
            toggle.classList.remove('open');
        } else {
            menu.classList.add('mobile-menu-open');
            toggle.classList.add('open');
        }
    });

    // Close on nav link click
    menu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.remove('mobile-menu-open');
            toggle.classList.remove('open');
        });
    });
}

// Header scroll effect
function initHeaderScroll() {
    const header = document.getElementById('siteHeader');
    if (!header) return;

    const updateHeader = () => {
        if (window.scrollY > 20) {
            header.classList.add('header-scrolled');
        } else {
            header.classList.remove('header-scrolled');
        }
    };

    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();
}

// Smooth scrolling for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// Scroll-triggered reveal animations
function initAnimations() {
    const animated = document.querySelectorAll('[data-animate]');
    if (!animated.length) return;

    // Step 1: Immediately hide all animated elements.
    // This runs synchronously so there's no visible flash.
    animated.forEach(el => el.classList.add('anim-hidden'));

    // Step 2: Check which elements are already in the viewport
    // and reveal them immediately (no need to wait for scroll).
    const inView = [];
    animated.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            inView.push(el);
        }
    });

    // Reveal in-view elements with staggered delay
    inView.forEach((el, i) => {
        setTimeout(() => {
            el.classList.remove('anim-hidden');
            el.classList.add('revealed');
        }, i * 100);
    });

    // Step 3: Set up observer for elements below the fold
    if (!('IntersectionObserver' in window)) {
        // Fallback: show everything
        animated.forEach(el => {
            el.classList.remove('anim-hidden');
            el.classList.add('revealed');
        });
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Stagger based on position among remaining hidden siblings
                const hiddenSiblings = Array.from(
                    entry.target.parentElement
                        ? entry.target.parentElement.querySelectorAll('[data-animate].anim-hidden:not(.revealed)')
                        : []
                );
                const idx = hiddenSiblings.indexOf(entry.target);
                const delay = idx >= 0 ? idx * 100 : 0;

                setTimeout(() => {
                    entry.target.classList.remove('anim-hidden');
                    entry.target.classList.add('revealed');
                }, delay);

                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.05,
        rootMargin: '0px 0px -20px 0px'
    });

    // Only observe elements not already revealed
    animated.forEach(el => {
        if (!el.classList.contains('revealed')) {
            observer.observe(el);
        }
    });
}

// Cookie banner
function initCookieBanner() {
    if (localStorage.getItem('cookiesAccepted')) {
        const banner = document.getElementById('cookieBanner');
        if (banner) banner.style.display = 'none';
    }
}

function acceptCookies() {
    localStorage.setItem('cookiesAccepted', 'true');
    const banner = document.getElementById('cookieBanner');
    if (banner) {
        banner.style.transform = 'translateY(100%)';
        setTimeout(() => { banner.style.display = 'none'; }, 500);
    }
}

function dismissCookies() {
    localStorage.setItem('cookiesDismissed', 'true');
    const banner = document.getElementById('cookieBanner');
    if (banner) {
        banner.style.transform = 'translateY(100%)';
        setTimeout(() => { banner.style.display = 'none'; }, 500);
    }
}
