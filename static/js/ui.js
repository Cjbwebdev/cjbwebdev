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

// Intersection Observer animations
function initAnimations() {
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-up');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('[data-animate]').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
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
