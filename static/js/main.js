/**
 * ElectroStore - Main JavaScript
 * Handles: Page loader, navbar, mobile menu, animations, toast notifications
 */

// ──────────────────────────────────────────
// Page Loader
// ──────────────────────────────────────────
window.addEventListener('load', () => {
  const loader = document.getElementById('page-loader');
  if (loader) {
    loader.style.opacity = '0';
    setTimeout(() => loader.style.display = 'none', 300);
  }
});

// ──────────────────────────────────────────
// Navbar scroll effect
// ──────────────────────────────────────────
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.5)';
    } else {
      navbar.style.boxShadow = 'none';
    }
  }, { passive: true });
}

// ──────────────────────────────────────────
// Mobile Menu Toggle
// ──────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobile-menu');

if (hamburger && mobileMenu) {
  hamburger.addEventListener('click', () => {
    const isOpen = mobileMenu.style.display !== 'none';
    mobileMenu.style.display = isOpen ? 'none' : 'block';
    hamburger.classList.toggle('open', !isOpen);
  });

  hamburger.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      hamburger.click();
    }
  });
}

// ──────────────────────────────────────────
// Toast Notification System
// ──────────────────────────────────────────
function showToast(message, type = 'info', duration = 3000) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${icons[type] || '💬'}</span><span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'fadeOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Expose globally
window.showToast = showToast;

// ──────────────────────────────────────────
// Intersection Observer (Fade-in animations)
// ──────────────────────────────────────────
const animateOnScroll = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, idx) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, idx * 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.product-card, .category-card, .error-code-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    observer.observe(el);
  });
};

document.addEventListener('DOMContentLoaded', animateOnScroll);

// ──────────────────────────────────────────
// Add to Cart (visual feedback)
// ──────────────────────────────────────────
document.addEventListener('click', (e) => {
  if (e.target.closest('.btn-add-cart')) {
    const btn = e.target.closest('.btn-add-cart');
    const original = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-check"></i> Added!';
    btn.style.background = 'rgba(16, 185, 129, 0.2)';
    btn.style.borderColor = 'rgba(16, 185, 129, 0.5)';
    btn.style.color = '#34d399';
    setTimeout(() => {
      btn.innerHTML = original;
      btn.style.background = '';
      btn.style.borderColor = '';
      btn.style.color = '';
    }, 2000);
    showToast('Added to cart!', 'success');
  }
});

// ──────────────────────────────────────────
// FAQ Accordion
// ──────────────────────────────────────────
document.addEventListener('click', (e) => {
  if (e.target.closest('.faq-question')) {
    const btn = e.target.closest('.faq-question');
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('open');

    // Close all
    document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));

    // Open if was closed
    if (!isOpen) item.classList.add('open');
  }
});

// ──────────────────────────────────────────
// Product Image Lazy Loading Fallback
// ──────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('img[data-src]').forEach(img => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        img.src = img.dataset.src;
        observer.unobserve(img);
      }
    });
    observer.observe(img);
  });

  // Handle broken images
  document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', function () {
      this.src = '/static/images/no-image.svg';
      this.onerror = null;
    });
  });
});

// ──────────────────────────────────────────
// CSRF Token helper
// ──────────────────────────────────────────
function getCsrfToken() {
  return document.cookie.split(';')
    .find(c => c.trim().startsWith('csrftoken='))
    ?.split('=')[1] || '';
}

window.getCsrfToken = getCsrfToken;
