class MenuPagination {
    constructor() {
        this.allCards = [...document.querySelectorAll('.menu-card')];
        this.pagination = document.getElementById('pagination');
        this.filterBtns = document.querySelectorAll('.filter-btn');
        this.currentPage = 1;
        this.perPage = 4;
        this.currentFilter = 'all';
        this.filteredCards = this.allCards;

        this.init();
    }

    init() {
        this.setupFilterListeners();
        this.updateView();
    }

    setupFilterListeners() {
        this.filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active filter button
                this.filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Apply filter
                this.currentFilter = btn.dataset.filter;
                this.applyFilter();
                this.currentPage = 1;
                this.updateView();
            });
        });
    }

    applyFilter() {
        if (this.currentFilter === 'all') {
            this.filteredCards = this.allCards;
        } else {
            this.filteredCards = this.allCards.filter(card =>
                card.dataset.category === this.currentFilter
            );
        }
    }

    showPage(page) {
        this.currentPage = page;

        // Hide all cards first
        this.allCards.forEach(card => {
            card.style.display = 'none';
            card.classList.remove('show');
        });

        // Show filtered cards for current page
        const startIndex = (page - 1) * this.perPage;
        const endIndex = startIndex + this.perPage;
        const cardsToShow = this.filteredCards.slice(startIndex, endIndex);

        cardsToShow.forEach((card, index) => {
            card.style.display = 'block';
            setTimeout(() => {
                card.classList.add('show');
            }, index * 100);
        });
    }

    generatePagination() {
        const totalPages = Math.ceil(this.filteredCards.length / this.perPage);
        let paginationHTML = '';

        // Previous button
        if (this.currentPage > 1) {
            paginationHTML += `
                        <li>
                            <button data-page="prev" class="px-3 py-2 border rounded hover:bg-orange-500 hover:text-white transition-colors">
                                ←
                            </button>
                        </li>
                    `;
        }

        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            const activeClass = i === this.currentPage ? 'active' : '';
            paginationHTML += `
                        <li>
                            <button data-page="${i}" class="page-btn px-3 py-2 border rounded transition-all duration-200 ${activeClass}">
                                ${i.toString().padStart(2, '0')}
                            </button>
                        </li>
                    `;
        }

        // Next button
        if (this.currentPage < totalPages) {
            paginationHTML += `
                        <li>
                            <button data-page="next" class="px-3 py-2 border rounded hover:bg-orange-500 hover:text-white transition-colors">
                                →
                            </button>
                        </li>
                    `;
        }

        this.pagination.innerHTML = paginationHTML;

        // Add click listeners to new pagination buttons
        this.pagination.addEventListener('click', (e) => {
            const btn = e.target.closest('button');
            if (!btn) return;

            const page = btn.dataset.page;
            const totalPages = Math.ceil(this.filteredCards.length / this.perPage);

            if (page === 'prev' && this.currentPage > 1) {
                this.updateView(this.currentPage - 1);
            } else if (page === 'next' && this.currentPage < totalPages) {
                this.updateView(this.currentPage + 1);
            } else if (!isNaN(page)) {
                this.updateView(Number(page));
            }
        });
    }

    updateView(page = this.currentPage) {
        this.currentPage = page;
        this.generatePagination();
        this.showPage(this.currentPage);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MenuPagination();
});