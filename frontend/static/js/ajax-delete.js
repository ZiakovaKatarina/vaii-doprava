(function() {
  'use strict';

  // Predpokladáme, že loadStops je globálne dostupná funkcia
  document.addEventListener('click', async (e) => {
    if (e.target.classList.contains('btn-delete-ajax')) {
      e.preventDefault();
      if (!confirm('Naozaj chcete zmazať túto zastávku?')) return;

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
        if (data.ok) {
          alert('✅ Zastávka bola zmazaná');
          // Namiesto reloadu zavolaj loadStops()
          if (typeof window.loadStops === 'function') {
            window.loadStops();
          }
        } else {
          alert('❌ Chyba: ' + (data.error || 'Nepodarilo sa zmazať'));
        }
      } catch (err) {
        alert('❌ Chyba: ' + err.message);
      }
    }
  });
})();