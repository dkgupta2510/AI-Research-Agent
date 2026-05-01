document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('search-form');
    const input = document.getElementById('query-input');
    const header = document.getElementById('header');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const errorMessage = document.getElementById('error-message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = input.value.trim();
        if (!query) return;

        // Transition header state
        header.classList.remove('header-center');
        header.classList.add('header-top');

        // Show loading, hide others
        loading.classList.remove('hidden');
        results.classList.add('hidden');
        errorMessage.classList.add('hidden');

        try {
            const response = await fetch('/api/research', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'An error occurred during research.');
            }

            renderResults(data);
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove('hidden');
        } finally {
            loading.classList.add('hidden');
        }
    });

    function renderResults(data) {
        // Handle Confidence Badge
        const badge = document.getElementById('confidence-badge');
        badge.textContent = `${data.confidence || 'Unknown'} Confidence`;
        badge.className = 'badge';
        if (data.confidence === 'High') badge.classList.add('badge-high');
        else if (data.confidence === 'Medium') badge.classList.add('badge-medium');
        else if (data.confidence === 'Low') badge.classList.add('badge-low');

        // Populate Answer
        document.getElementById('res-answer').textContent = data.short_answer || data.answer || 'No answer provided.';

        // Populate Lists
        populateList('res-findings', data.key_findings || data.points || []);
        populateList('res-plan', data.plan || [], true);
        populateList('res-limitations', data.limitations || []);
        populateList('res-next-steps', data.next_steps || []);

        // Populate Sources as Links
        const sourcesList = document.getElementById('res-sources');
        sourcesList.innerHTML = '';
        const sources = data.sources || [];
        if (sources.length > 0) {
            sources.forEach(src => {
                const li = document.createElement('li');
                if (src.startsWith('http')) {
                    const a = document.createElement('a');
                    a.href = src;
                    a.target = '_blank';
                    a.rel = 'noopener noreferrer';
                    a.textContent = src;
                    li.appendChild(a);
                } else {
                    li.textContent = src;
                }
                sourcesList.appendChild(li);
            });
            document.querySelector('.sources-card').classList.remove('hidden');
        } else {
            document.querySelector('.sources-card').classList.add('hidden');
        }

        // Hide empty cards
        toggleCard('res-findings', data.key_findings || data.points);
        toggleCard('res-plan', data.plan);
        toggleCard('res-limitations', data.limitations);
        toggleCard('res-next-steps', data.next_steps);

        // Show Results
        results.classList.remove('hidden');
    }

    function populateList(elementId, items, isOrdered = false) {
        const el = document.getElementById(elementId);
        el.innerHTML = '';
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            el.appendChild(li);
        });
    }

    function toggleCard(elementId, items) {
        const card = document.getElementById(elementId).closest('.card');
        if (!items || items.length === 0) {
            card.classList.add('hidden');
        } else {
            card.classList.remove('hidden');
        }
    }
});
