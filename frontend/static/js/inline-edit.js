(function() {
  'use strict';
  
  function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split('; ') : [];
    for (const c of cookies) {
      const [k, v] = c.split('=');
      if (k === name) return decodeURIComponent(v);
    }
    return null;
  }
  
  function makeEditable(cell, stopId, field) {
    const originalValue = cell.textContent.trim();
    const input = document.createElement('input');
    input.type = 'text';
    input.value = originalValue;
    input.style.width = '100%';
    
    cell.textContent = '';
    cell.appendChild(input);
    input.focus();
    
    async function save() {
      const newValue = input.value.trim();
      if (newValue === originalValue) {
        cell.textContent = originalValue;
        return;
      }
      
      const url = `/api/stops/${stopId}/update/`;
      const csrftoken = getCookie('csrftoken');
      
      try {
        const res = await fetch(url, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
          body: JSON.stringify({ [field]: newValue })
        });
        
        const data = await res.json();
        if (data.ok) {
          cell.textContent = newValue;
        } else {
          alert(data.error || 'Uloženie zlyhalo.');
          cell.textContent = originalValue;
        }
      } catch (err) {
        alert('Chyba pri ukladaní.');
        cell.textContent = originalValue;
      }
    }
    
    input.addEventListener('blur', save);
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') { e.preventDefault(); save(); }
      else if (e.key === 'Escape') { cell.textContent = originalValue; }
    });
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.editable-cell').forEach(cell => {
      cell.addEventListener('dblclick', function() {
        const stopId = this.dataset.stopId;
        const field = this.dataset.field;
        makeEditable(this, stopId, field);
      });
    });
  });
})();