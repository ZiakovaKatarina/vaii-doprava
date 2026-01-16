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
          'X-CSRFToken': csrfToken
        }
      });
      
      const data = await res.json();
      
      if (data.ok) {
        alert('✅ Zastávka bola úspešne vytvorená!');
        window.location.href = data.redirect || '/stops/';
      } else {
        alert('❌ Chyba: ' + (data.errors || 'Nepodarilo sa uložiť'));
      }
    } catch (err) {
      alert('❌ Chyba: ' + err.message);
    }
  });
})();