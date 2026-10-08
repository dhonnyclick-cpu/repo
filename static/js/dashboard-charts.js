// dashboard-charts.js - Chart.js visuals following dataviz method
// Palette: validated categorical slots (fixed order, never cycled) + blue sequential ramp.
// Surfaces: light #fcfcfb. Ink stays in text tokens, never series color.
(function () {
    const CATEGORICAL = [
        '#2a78d6', // 1 blue
        '#eb6834', // 2 orange
        '#1baf7a', // 3 aqua
        '#eda100', // 4 yellow
        '#e87ba4', // 5 magenta
        '#008300', // 6 green
        '#4a3aa7', // 7 violet
        '#e34948', // 8 red
    ];
    // Sequential blue ramp light->dark (single-hue magnitude)
    const SEQUENTIAL_BLUE = ['#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#2a78d6', '#256abf', '#1c5cab', '#184f95', '#104281', '#0d366b'];

    const GRID = '#e1e0d9';
    const MUTED = '#898781';
    const INK = '#0b0b0b';

    Chart.defaults.font.family = 'system-ui, -apple-system, "Segoe UI", sans-serif';
    Chart.defaults.color = MUTED;

    function baseScales() {
        return {
            x: { grid: { display: false }, ticks: { color: MUTED, maxRotation: 30 } },
            y: { beginAtZero: true, grid: { color: GRID }, ticks: { color: MUTED, precision: 0 } }
        };
    }

    // --- 1. Top 10 stock: single series -> one sequential hue, no legend box (title names it)
    fetch('/api/stock-chart')
        .then(r => r.json())
        .then(({ labels, data }) => {
            const el = document.getElementById('stockChart');
            if (!el) return;
            // Map magnitude to ramp steps (largest = darkest)
            const max = Math.max(...data, 1);
            const bg = data.map(v => {
                const t = v / max;
                const idx = Math.min(SEQUENTIAL_BLUE.length - 1, Math.floor(t * (SEQUENTIAL_BLUE.length - 1)));
                return SEQUENTIAL_BLUE[Math.max(3, idx)]; // start at step readable on surface
            });
            new Chart(el, {
                type: 'bar',
                data: { labels, datasets: [{ label: 'Stok (satuan)', data, backgroundColor: bg, borderRadius: 4, borderSkipped: 'start' }] },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y} satuan` } }
                    },
                    scales: baseScales()
                }
            });
        })
        .catch(() => {});

    // --- 2. Stock per category: identity -> categorical slots in fixed order, legend present
    fetch('/api/category-chart')
        .then(r => r.json())
        .then(({ labels, data }) => {
            const el = document.getElementById('categoryChart');
            if (!el) return;
            new Chart(el, {
                type: 'doughnut',
                data: {
                    labels,
                    datasets: [{
                        data,
                        backgroundColor: labels.map((_, i) => CATEGORICAL[i % CATEGORICAL.length]),
                        borderColor: '#fcfcfb',
                        borderWidth: 2 // 2px surface gap between segments
                    }]
                },
                options: {
                    responsive: true,
                    cutout: '55%',
                    plugins: {
                        legend: { position: 'bottom', labels: { color: INK, boxWidth: 12, padding: 12 } },
                        tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.parsed} satuan` } }
                    }
                }
            });
        })
        .catch(() => {});

    // --- 3. Stock per warehouse: single measure -> one sequential hue, no legend
    fetch('/api/warehouse-chart')
        .then(r => r.json())
        .then(({ labels, data }) => {
            const el = document.getElementById('warehouseChart');
            if (!el) return;
            new Chart(el, {
                type: 'bar',
                data: { labels, datasets: [{ label: 'Total stok', data, backgroundColor: '#2a78d6', borderRadius: 4, borderSkipped: 'start' }] },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y} satuan` } }
                    },
                    scales: baseScales()
                }
            });
        })
        .catch(() => {});
})();
