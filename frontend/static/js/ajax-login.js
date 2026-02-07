(function() {
  'use strict';
  
  const loginForm = document.querySelector('#login-form');
  const errorContainer = document.querySelector('#login-error-container');
  if (!loginForm) return;
  
  loginForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    errorContainer.innerHTML = '';

    document.querySelectorAll('header + .container .alert').forEach(el => el.style.display = 'none');
    
    const formData = new FormData(loginForm);
    const csrftoken = formData.get('csrfmiddlewaretoken');
    
    try {
      const res = await fetch(loginForm.action, {
        method: 'POST',
        headers: { 
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest' 
        },
        body: formData
      });
      
      const data = await res.json();
      
      if (data.success) {
        window.location.href = data.redirect_url;
      } else {
        errorContainer.innerHTML = `
            <div class="alert alert-error" style="margin-bottom: 15px; text-align: center; font-size: 0.9rem;">
                ${data.error || 'Nesprávne meno alebo heslo.'}
            </div>
        `;
        
        loginForm.style.animation = 'shake 0.3s';
        setTimeout(() => loginForm.style.animation = '', 300);
      }
    } catch (err) {
      errorContainer.innerHTML = '<div class="alert alert-error">Chyba pri komunikácii so serverom.</div>';
    }
  });
})();