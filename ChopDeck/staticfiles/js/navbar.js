
class OffcanvasMenu {
    constructor() {
        this.offcanvas = document.getElementById('top-navbar');
        this.backdrop = document.getElementById('backdrop');
        this.toggleButton = document.getElementById('navbar-toggler');
        this.closeButton = document.getElementById('close-offcanvas');
        this.isOpen = false;

        this.init();
    }

    init() {
        // Toggle button event
        this.toggleButton.addEventListener('click', () => {
            this.toggle();
        });

        // Close button event
        this.closeButton.addEventListener('click', () => {
            this.hide();
        });

        // Backdrop click event
        this.backdrop.addEventListener('click', () => {
            this.hide();
        });

        // Escape key event
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.hide();
            }
        });

        // Close on resize to desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 1024 && this.isOpen) {
                this.hide();
            }
        });
    }

    show() {
        if (this.isOpen) return;

        this.isOpen = true;
        document.body.style.overflow = 'hidden';

        // Show elements
        this.offcanvas.style.display = 'block';
        this.backdrop.style.display = 'block';

        // Trigger animations
        requestAnimationFrame(() => {
            this.offcanvas.classList.add('show');
            this.backdrop.classList.add('show');
        });

        // Update aria attributes
        this.toggleButton.setAttribute('aria-expanded', 'true');
    }

    hide() {
        if (!this.isOpen) return;

        this.isOpen = false;
        document.body.style.overflow = '';

        // Remove show classes
        this.offcanvas.classList.remove('show');
        this.backdrop.classList.remove('show');

        // Hide elements after animation
        setTimeout(() => {
            if (!this.isOpen) {
                this.offcanvas.style.display = 'none';
                this.backdrop.style.display = 'none';
            }
        }, 300);

        // Update aria attributes
        this.toggleButton.setAttribute('aria-expanded', 'false');
    }

    toggle() {
        if (this.isOpen) {
            this.hide();
        } else {
            this.show();
        }
    }
}

// Initialize the offcanvas menu
const offcanvasMenu = new OffcanvasMenu();

// Global function for closing navbar (same as your Bootstrap version)
function closeNavbar() {
    offcanvasMenu.hide();
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
