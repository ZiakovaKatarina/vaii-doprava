(function() {
  'use strict';

  document.addEventListener('click', async (e) => {
    if (e.target.classList.contains('btn-delete-ajax')) {
      e.preventDefault();
      
      const stopName = e.target.closest('tr').querySelector('td').textContent;
      if (!confirm(`Naozaj chcete zmazať zastávku "${stopName}"?`)) return;

      const url = e.target.getAttribute('href');
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

      try {
        const res = await fetch(url, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        const data = await res.json();

        if (res.ok && data.ok) {
          alert('✅ Zastávka bola zmazaná');
          if (typeof window.loadStops === 'function') {
            window.loadStops();
          }
        } else {
          alert(' ' + (data.error || 'Zastávku nie je možné zmazať.'));
        }
      } catch (err) {
        alert('Systémová chyba pri komunikácii so serverom.');
      }
    }
  });
})();