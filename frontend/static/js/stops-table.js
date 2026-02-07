(function() {
  'use strict';

  const tbody = document.getElementById('stops-tbody');
  const searchInput = document.getElementById('stops-search');
  const prevBtn = document.getElementById('stops-prev');
  const nextBtn = document.getElementById('stops-next');
  const pageInfo = document.getElementById('stops-page-info');
  const pageSizeSelect = document.getElementById('stops-page-size');
  const totalCountSpan = document.getElementById('stops-total-count');
  const tableEl = document.getElementById('stops-main-table');

  const isStaff = tableEl.dataset.isStaff === 'true';

  let state = { page: 1, pages: 1, search: '', page_size: 10 };

  async function loadStops() {
    const url = `/api/stops/?page=${state.page}&search=${encodeURIComponent(state.search)}&page_size=${state.page_size}`;
    try {
      const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
      const data = await res.json();
      
      state.page = data.page;
      state.pages = data.pages;

      if (totalCountSpan) totalCountSpan.textContent = data.count;

      const rows = data.stops.map(s => {
        let rowHtml = `
          <tr>
            <td class="${isStaff ? 'editable-cell' : ''}" data-stop-id="${s.id}" data-field="name">${s.name}</td>
            <td class="${isStaff ? 'editable-cell' : ''}" data-stop-id="${s.id}" data-field="latitude">${s.latitude}</td>
            <td class="${isStaff ? 'editable-cell' : ''}" data-stop-id="${s.id}" data-field="longitude">${s.longitude}</td>
        `;
        
        if (isStaff) {
          rowHtml += `
            <td style="text-align:center;">
              <a href="/stops/${s.id}/update/" class="btn btn-sm btn-primary">Upraviť</a>
              <a href="/stops/${s.id}/delete/" class="btn btn-sm btn-outline btn-delete-ajax" style="color:red; border-color:red;">Zmazať</a>
            </td>
          `;
        }

        rowHtml += `</tr>`;
        return rowHtml;
      }).join('');

      tbody.innerHTML = rows || '<tr><td colspan="4" style="text-align:center;color:#999;">Žiadne zastávky</td></tr>';

      pageInfo.textContent = `Strana ${state.page} z ${state.pages}`;

      if (state.page > 1) {
          prevBtn.style.display = 'inline-block';
      } else {
          prevBtn.style.display = 'none';
      }

      if (state.page < state.pages) {
          nextBtn.style.display = 'inline-block';
      } else {
          nextBtn.style.display = 'none';
      }

    } catch (err) {
      tbody.innerHTML = `<tr><td colspan="4" style="color:red;">Chyba pri načítaní: ${err.message}</td></tr>`;
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', () => { state.page = 1; state.search = searchInput.value.trim(); loadStops(); });
  }
  if (pageSizeSelect) {
    pageSizeSelect.addEventListener('change', () => { state.page_size = parseInt(pageSizeSelect.value, 10); state.page = 1; loadStops(); });
  }
  if (prevBtn) prevBtn.addEventListener('click', () => { if (state.page > 1) { state.page--; loadStops(); } });
  if (nextBtn) nextBtn.addEventListener('click', () => { if (state.page < state.pages) { state.page++; loadStops(); } });

  document.addEventListener('DOMContentLoaded', loadStops);
  window.loadStops = loadStops;
})();