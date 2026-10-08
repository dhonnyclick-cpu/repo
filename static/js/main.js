// main.js - shared interactions
(function() {
    // Current date in topbar
    const el = document.getElementById('current-date');
    if (el) {
        const now = new Date();
        el.textContent = now.toLocaleDateString('id-ID', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    }

    // Image preview on file input
    document.querySelectorAll('input[type="file"][name="image"]').forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (!file) return;
            let preview = document.getElementById('img-preview');
            if (!preview) {
                preview = document.createElement('img');
                preview.id = 'img-preview';
                preview.style.cssText = 'max-width:200px;max-height:200px;border-radius:8px;margin-top:8px;display:block;object-fit:cover;';
                this.parentElement.appendChild(preview);
            }
            preview.src = URL.createObjectURL(file);
        });
    });

    // Auto-hide alerts after 4s
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(a => a.style.display = 'none');
    }, 4000);

    // Client-side table filter (if search input exists)
    const searchInput = document.getElementById('table-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const q = this.value.toLowerCase();
            document.querySelectorAll('.data-table tbody tr').forEach(tr => {
                tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
            });
        });
    }
})();
