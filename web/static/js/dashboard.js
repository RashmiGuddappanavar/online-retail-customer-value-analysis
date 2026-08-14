document.addEventListener("DOMContentLoaded", function() {
    const formatCurrency = (val) => new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' }).format(val);
    const formatNumber = (val) => new Intl.NumberFormat('en-GB').format(val);

    function updateClock() {
        const now = new Date();
        const clockElem = document.getElementById('live-clock');
        if (clockElem) {
            clockElem.textContent = now.toISOString().replace('T', ' ').substring(0, 19);
        }
    }

    // Live KPI Auto-Refresh Poll (Every 3 seconds)
    function pollLiveKPIs() {
        fetch('/api/live-kpis')
            .then(res => res.json())
            .then(kpis => {
                updateClock();
                const revElem = document.getElementById('kpi-total-revenue');
                const ordElem = document.getElementById('kpi-total-orders');
                const custElem = document.getElementById('kpi-unique-customers');
                const aovElem = document.getElementById('kpi-aov');
                const repRateElem = document.getElementById('kpi-repeat-rate');
                const repCustElem = document.getElementById('kpi-repeat-customers');
                const simCountElem = document.getElementById('kpi-sim-count');
                const simRevElem = document.getElementById('kpi-sim-rev');
                const cancElem = document.getElementById('kpi-cancellation-rate');
                const cancLinesElem = document.getElementById('kpi-cancelled-lines');

                const purchasingCust = kpis.purchasing_customers !== undefined ? kpis.purchasing_customers : (kpis.unique_customers !== undefined ? kpis.unique_customers : 0);
                const repeatRate = kpis.repeat_customer_rate !== undefined ? kpis.repeat_customer_rate : (kpis.repeat_rate !== undefined ? kpis.repeat_rate : 0.0);
                const repeatCust = kpis.repeat_customers !== undefined ? kpis.repeat_customers : 0;

                if (revElem) revElem.textContent = formatCurrency(kpis.total_revenue);
                if (ordElem) ordElem.textContent = formatNumber(kpis.total_orders);
                if (custElem) custElem.textContent = formatNumber(purchasingCust);
                if (aovElem) aovElem.textContent = formatCurrency(kpis.aov);
                if (repRateElem) repRateElem.textContent = `${repeatRate.toFixed(2)}%`;
                if (repCustElem) repCustElem.textContent = `${formatNumber(repeatCust)} repeat buyers`;
                if (simCountElem) simCountElem.textContent = `${formatNumber(kpis.simulated_count)} tx ingested`;
                if (simRevElem) simRevElem.textContent = `${formatCurrency(kpis.simulated_revenue)} live volume`;
                if (cancElem) cancElem.textContent = `${kpis.cancellation_rate.toFixed(2)}%`;
                if (cancLinesElem) cancLinesElem.textContent = `${formatNumber(kpis.cancelled_lines)} cancelled lines`;
            })
            .catch(err => console.error("Error polling live KPIs:", err));
    }

    // Live Transactions Stream Feed Poll
    function pollLiveTransactions() {
        const feedElem = document.getElementById('live-transaction-feed');
        if (!feedElem) return;

        fetch('/api/live-transactions')
            .then(res => res.json())
            .then(txs => {
                feedElem.innerHTML = '';
                if (txs.length === 0) {
                    feedElem.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted);">No live transactions yet. Use demo controls to generate data.</td></tr>';
                    return;
                }
                txs.forEach(tx => {
                    const row = document.createElement('tr');
                    const isSim = tx.is_simulated === 1;
                    const lineVal = tx.IsCancelled ? 0.0 : (tx.Quantity * tx.UnitPrice);
                    row.innerHTML = `
                        <td><code>${tx.InvoiceNo}</code></td>
                        <td>${tx.StockCode} - ${tx.Description}</td>
                        <td>${tx.Quantity}</td>
                        <td>${formatCurrency(lineVal)}</td>
                        <td>${tx.Country}</td>
                        <td>
                            <span class="badge ${isSim ? 'badge-high' : 'badge-low'}">
                                ${isSim ? 'SIMULATED LIVE' : 'HISTORICAL BASELINE'}
                            </span>
                        </td>
                    `;
                    feedElem.appendChild(row);
                });
            })
            .catch(err => console.error("Error polling live transactions:", err));
    }

    setInterval(() => {
        pollLiveKPIs();
        pollLiveTransactions();
    }, 3000);
    pollLiveKPIs();
    pollLiveTransactions();

    // Demo control functions
    window.triggerDemoIngest = function(count) {
        fetch(`/api/demo/generate?count=${count}`, { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                pollLiveKPIs();
                pollLiveTransactions();
            })
            .catch(err => console.error("Error triggering demo ingest:", err));
    };

    window.toggleStream = function(start) {
        const endpoint = start ? '/api/demo/stream/start' : '/api/demo/stream/stop';
        fetch(endpoint, { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                const textElem = document.getElementById('live-status-text');
                if (textElem) {
                    textElem.textContent = start ? '● LIVE STREAMING' : '● LIVE';
                }
            })
            .catch(err => console.error("Error toggling stream:", err));
    };

    // Chart Renderings
    const monthlyCtx = document.getElementById('monthlyChart');
    if (monthlyCtx) {
        fetch('/api/monthly-revenue')
            .then(res => res.json())
            .then(data => {
                new Chart(monthlyCtx, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Completed Revenue (£)',
                            data: data.revenue,
                            borderColor: '#38bdf8',
                            backgroundColor: 'rgba(56, 189, 248, 0.1)',
                            fill: true,
                            tension: 0.3
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { labels: { color: '#94a3b8' } } },
                        scales: {
                            x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
                            y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
                        }
                    }
                });
            });
    }

    const countryCtx = document.getElementById('countryChart');
    if (countryCtx) {
        fetch('/api/top-countries')
            .then(res => res.json())
            .then(data => {
                new Chart(countryCtx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Revenue (£)',
                            data: data.revenue,
                            backgroundColor: '#22c55e'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { labels: { color: '#94a3b8' } } },
                        scales: {
                            x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
                            y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
                        }
                    }
                });
            });
    }

    const productCtx = document.getElementById('productChart');
    if (productCtx) {
        fetch('/api/top-products')
            .then(res => res.json())
            .then(data => {
                new Chart(productCtx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Revenue (£)',
                            data: data.revenue,
                            backgroundColor: '#a855f7'
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        plugins: { legend: { labels: { color: '#94a3b8' } } },
                        scales: {
                            x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
                            y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
                        }
                    }
                });
            });
    }

    const segmentCtx = document.getElementById('segmentChart');
    if (segmentCtx) {
        fetch('/api/customer-segments')
            .then(res => res.json())
            .then(data => {
                new Chart(segmentCtx, {
                    type: 'doughnut',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.counts,
                            backgroundColor: [
                                '#22c55e', '#38bdf8', '#a855f7', '#f59e0b', '#f43f5e', '#64748b', '#ec4899'
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }
                    }
                });
            });
    }
});
