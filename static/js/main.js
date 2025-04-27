// Infinite scroll for story lists (pagination)
document.addEventListener('DOMContentLoaded', function() {
    const nextBtn = document.getElementById('next-page');
    if (nextBtn) {
        nextBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location = nextBtn.getAttribute('href');
        });
    }
    // Simple client-side search (for enhancement)
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                window.location = '/search?q=' + encodeURIComponent(searchInput.value);
            }
        });
    }
});
