(function() {
  'use strict';

  const form = document.getElementById('stop-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);
    const csrfToken = formData.get('csrfmiddlewaretoken');
    
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken
        }
      });
      
      const contentType = res.headers.get("content-type");
      
      if (contentType && contentType.indexOf("application/json") !== -1) {
        const data = await res.json();
        if (data.ok) {
          alert('✅ Uložené úspešne!');
          window.location.href = data.redirect || '/stops/';
        } else {
          // data.errors je teraz pole zo servera
          const msg = Array.isArray(data.errors) ? data.errors.join('\n') : data.errors;
          alert('❌ Validačná chyba:\n' + msg);
        }
      } else {
        // Ak to nie je JSON, server poslal HTML (napr. chybu 500)
        const htmlErr = await res.text();
        console.error("Server vrátil HTML namiesto JSON:", htmlErr);
        alert('❌ Server vrátil chybu (HTML). Pozri konzolu F12.');
      }
    } catch (err) {
      alert('❌ Kritická chyba komunikácie: ' + err.message);
    }
  });
})();