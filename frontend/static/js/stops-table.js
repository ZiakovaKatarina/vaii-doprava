(function() {
  'use strict';

  const tbody = document.getElementById('stops-tbody');
  const searchInput = document.getElementById('stops-search');
  const prevBtn = document.getElementById('stops-prev');
  const nextBtn = document.getElementById('stops-next');
  const pageInfo = document.getElementById('stops-page-info');
  const pageSizeSelect = document.getElementById('stops-page-size');
  const paginationDiv = document.getElementById('stops-pagination');
  let state = { page: 1, pages: 1, search: '', page_size: 10 };

  async function loadStops() {
    const url = `/api/stops/?page=${state.page}&search=${encodeURIComponent(state.search)}&page_size=${state.page_size}`;
    try {
      const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
      const data = await res.json();
      state.page = data.page;
      state.pages = data.pages;

      const rows = data.stops.map(s => `
        <tr>
          <td>${s.name}</td>
          <td>${s.latitude}</td>
          <td>${s.longitude}</td>
          <td>
            <a href="/stops/${s.id}/update/" class="btn btn-sm btn-primary">Upraviť</a>
            <a href="/stops/${s.id}/delete/" class="btn btn-sm btn-outline btn-delete-ajax">Zmazať</a>
          </td>
        </tr>
      `).join('');
      tbody.innerHTML = rows || '<tr><td colspan="4" style="text-align:center;color:#999;">Žiadne zastávky</td></tr>';

      pageInfo.textContent = `Strana ${data.page} z ${data.pages}`;

      if (data.pages <= 1) {
        paginationDiv.style.display = 'none';
      } else {
        paginationDiv.style.display = 'flex';
        prevBtn.disabled = data.page <= 1;
        nextBtn.disabled = data.page >= data.pages;
      }
    } catch (err) {
      tbody.innerHTML = `<tr><td colspan="4" style="color:red;">Chyba pri načítaní: ${err.message}</td></tr>`;
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      state.page = 1;
      state.search = searchInput.value.trim();
      loadStops();
    });
  }
  if (pageSizeSelect) {
    pageSizeSelect.addEventListener('change', () => {
      state.page_size = parseInt(pageSizeSelect.value, 10);
      state.page = 1;
      loadStops();
    });
  }
  if (prevBtn) prevBtn.addEventListener('click', () => {
    if (state.page > 1) { state.page--; loadStops(); }
  });
  if (nextBtn) nextBtn.addEventListener('click', () => {
    if (state.page < state.pages) { state.page++; loadStops(); }
  });

  document.addEventListener('DOMContentLoaded', loadStops);
  window.loadStops = loadStops;
})();