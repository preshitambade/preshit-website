/* ==================================================================
   metrics.js — loads live Scholar metrics + publications from JSON.
   These JSON files are refreshed weekly by the GitHub Actions
   workflows in .github/workflows/. If the fetch fails, the last
   committed values remain in place — nothing on the page breaks.
   ================================================================== */
(function () {
  const CACHE_BUST = '?t=' + Math.floor(Date.now() / 1000 / 3600); // per-hour cache-bust

  // ---------- Scholar metrics strip (home page) ----------
  if (document.getElementById('scholar-strip')) {
    fetch('data/metrics.json' + CACHE_BUST).then(r => r.json()).then(m => {
      document.querySelectorAll('[data-metric]').forEach(el => {
        const key = el.dataset.metric;
        if (m[key] != null) el.textContent = m[key].toLocaleString();
      });
      if (m.scholar_url) {
        const link = document.getElementById('scholar-link');
        if (link) link.href = m.scholar_url;
      }
      if (m.updated) {
        const upd = document.getElementById('metrics-updated');
        if (upd) upd.textContent = 'updated ' + friendly(m.updated);
      }
    }).catch(() => {
      const upd = document.getElementById('metrics-updated');
      if (upd) upd.textContent = 'metrics unavailable — see Scholar directly';
    });
  }

  // ---------- Conferences (research page) ----------
  const confGrid = document.getElementById('conf-grid');
  if (confGrid) {
    fetch('data/conferences.json' + CACHE_BUST).then(r => r.json()).then(data => {
      const list = data.conferences || [];
      if (!list.length) { confGrid.innerHTML = ''; return; }
      // sort newest first
      list.sort((a, b) => (b.year || 0) - (a.year || 0));
      confGrid.innerHTML = list.map(c =>
        `<div class="conf-card reveal in"><div class="yr">${escape(String(c.year || ''))}</div><h3>${escape(c.name || '')}</h3></div>`
      ).join('');
    }).catch(() => { confGrid.innerHTML = ''; });
  }

  // ---------- Publications list (research page) ----------
  const pubList = document.getElementById('pub-list');
  if (pubList) {
    fetch('data/publications.json' + CACHE_BUST).then(r => r.json()).then(data => {
      const pubs = Array.isArray(data) ? data : (data.publications || []);
      if (!pubs.length) {
        pubList.innerHTML = '<div class="pub"><p style="color:var(--ink-soft)">No publications loaded yet.</p></div>';
        return;
      }
      pubList.innerHTML = pubs.map(renderPub).join('');
      const meta = document.getElementById('pub-updated');
      if (meta && data.updated) meta.textContent = 'Last synced from ORCID · ' + friendly(data.updated);
    }).catch(() => {
      pubList.innerHTML = '<div class="pub"><p style="color:var(--ink-soft)">Could not load publications. Please try again later or view them on <a href="https://scholar.google.com/" target="_blank" rel="noopener" style="color:var(--coral)">Google Scholar</a>.</p></div>';
    });
  }

  function renderPub(p) {
    // Expected shape (ORCID/CrossRef derived):
    // { authors, year, title, venue, doi, url }
    const doi = p.doi ? ` <a href="https://doi.org/${p.doi}" target="_blank" rel="noopener" style="color:var(--coral);text-decoration:none">doi:${p.doi}</a>` : '';
    const url = p.url && !p.doi ? ` <a href="${p.url}" target="_blank" rel="noopener" style="color:var(--coral);text-decoration:none">view →</a>` : '';
    const venue = p.venue ? `<span class="venue">${escape(p.venue)}</span>` : '';
    const authors = highlightAuthor(p.authors || '');
    return `<div class="pub reveal in"><p>${authors} (${p.year || '—'}). ${escape(p.title)}. ${venue}.${doi}${url}</p></div>`;
  }

  function highlightAuthor(a) {
    return escape(a).replace(/(Ambade[^,]*)/g, '<strong>$1</strong>');
  }

  function escape(s) {
    return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  function friendly(iso) {
    try {
      const d = new Date(iso);
      const now = new Date();
      const days = Math.floor((now - d) / 86400000);
      if (days === 0) return 'today';
      if (days === 1) return 'yesterday';
      if (days < 14) return days + ' days ago';
      return d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
    } catch { return iso; }
  }
})();
