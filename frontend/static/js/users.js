(function () {
  'use strict';

  function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split('; ') : [];
    for (const c of cookies) {
      const [k, v] = c.split('=');
      if (k === name) return decodeURIComponent(v);
    }
    return null;
  }

  function findBadgeCell(checkbox) {
    const row = checkbox.closest('tr');
    return row ? row.querySelector('.badge-admin, .badge-role') : null;
  }

  async function toggleStaff(checkbox) {
    const userId = checkbox.dataset.userId;
    const desired = checkbox.checked;
    const url = `/users/api/users/${userId}/toggle-staff/`;
    const csrftoken = getCookie('csrftoken');
    checkbox.disabled = true;

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        body: JSON.stringify({ is_staff: desired })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || !data.ok) throw new Error(data.detail || 'Operácia zlyhala');

      const badge = findBadgeCell(checkbox);
      if (badge) {
        if (data.is_staff) { badge.className = 'badge badge-admin'; badge.textContent = 'Admin'; }
        else { badge.className = 'badge badge-role'; badge.textContent = 'Registrovaný používateľ'; }
      }
    } catch (err) {
      checkbox.checked = !desired;
      alert(err.message || 'Chyba pri ukladaní.');
    } finally {
      checkbox.disabled = false;
    }
  }

  function bindToggles(context=document) {
    context.querySelectorAll('.js-toggle-staff').forEach(cb => {
      cb.addEventListener('change', () => toggleStaff(cb));
    });
  }

  const elSearch = document.getElementById('user-search');
  const elRole = document.getElementById('role-filter');
  const elOrdering = document.getElementById('ordering');
  const elPageSize = document.getElementById('page-size');
  const elPrev = document.getElementById('users-prev');
  const elNext = document.getElementById('users-next');
  const elPageInfo = document.getElementById('users-page-info');
  const elTbody = document.getElementById('users-tbody');
  const elTable = document.getElementById('users-table');

  let state = { page: 1, pages: 1 };

  function debounce(fn, ms) {
    let t;
    return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
  }

  function buildQuery() {
    const params = new URLSearchParams();
    if (elSearch && elSearch.value.trim()) params.set('search', elSearch.value.trim());
    if (elRole && elRole.value) params.set('role', elRole.value);
    if (elOrdering && elOrdering.value) params.set('ordering', elOrdering.value);
    if (elPageSize && elPageSize.value) params.set('page_size', elPageSize.value);
    params.set('page', state.page);
    return params.toString();
  }

  async function loadUsers() {
    const url = `/users/api/users/?${buildQuery()}`;
    const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
    const data = await res.json();

    state.page = data.page;
    state.pages = data.pages;

    const currentId = String(data.current_user_id);
    const rows = data.items.map(item => {
      const isCurrent = String(item.id) === currentId;
      const highlight = isCurrent ? ' style="background-color:#e8f4f8;"' : '';
      const you = isCurrent ? '<span style="color:#0066cc;font-weight:bold;margin-left:8px;">(Vy)</span>' : '';
      const roleBadge = item.is_staff
        ? '<span class="badge badge-admin">Admin</span>'
        : '<span class="badge badge-role">Registrovaný používateľ</span>';

      const actions = isCurrent
        ? '<span style="color:#999;font-size:0.9rem;">-</span>'
        : `
          <div style="display:flex;gap:.5rem;justify-content:center;align-items:center;">
            <label style="display:flex;align-items:center;gap:6px;cursor:pointer;">
              <input type="checkbox" class="js-toggle-staff" data-user-id="${item.id}" ${item.is_staff ? 'checked' : ''}>
              <span style="font-size:.9rem;">Admin práva</span>
            </label>
            <a href="${item.edit_url}" class="btn btn-sm btn-primary">Upraviť</a>
            <a href="${item.reset_url}" class="btn btn-sm btn-outline">Reset hesla</a>
          </div>
        `;

      return `
        <tr${highlight}>
          <td><strong>${item.username}</strong>${you}</td>
          <td>${item.email || '-'}</td>
          <td>${item.first_name || '-'}</td>
          <td>${item.last_name || '-'}</td>
          <td>${roleBadge}</td>
          <td style="white-space:nowrap;">${item.date_joined}</td>
          <td style="text-align:center;">${actions}</td>
        </tr>
      `;
    }).join('');

    elTbody.innerHTML = rows;
    bindToggles(elTbody);
    elPageInfo.textContent = `Strana ${data.page} z ${data.pages}`;
    elPrev.disabled = data.page <= 1;
    elNext.disabled = data.page >= data.pages;
  }

  const debouncedLoad = debounce(loadUsers, 300);

  function bindFilters() {
    if (elSearch) elSearch.addEventListener('input', () => { state.page = 1; debouncedLoad(); });
    if (elRole) elRole.addEventListener('change', () => { state.page = 1; loadUsers(); });
    if (elOrdering) elOrdering.addEventListener('change', () => { state.page = 1; loadUsers(); });
    if (elPageSize) elPageSize.addEventListener('change', () => { state.page = 1; loadUsers(); });
    if (elPrev) elPrev.addEventListener('click', () => { if (state.page > 1) { state.page--; loadUsers(); } });
    if (elNext) elNext.addEventListener('click', () => { if (state.page < state.pages) { state.page++; loadUsers(); } });
  }

  document.addEventListener('DOMContentLoaded', function () {
    bindToggles();
    bindFilters();
  });
})();