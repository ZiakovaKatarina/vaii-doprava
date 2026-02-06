(function() {
  'use strict';
  
  const loginForm = document.querySelector('#login-form');
  if (!loginForm) return;
  
  loginForm.addEventListener('submit', async function(e) {
    e.preventDefault();  // zastav klasický submit
    
    const formData = new FormData(loginForm);
    const csrftoken = formData.get('csrfmiddlewaretoken');
    
    try {
      const res = await fetch(loginForm.action, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        body: formData
      });
      
      const data = await res.json();
      
      if (data.success) {
        window.location.href = data.redirect_url;  // presmerovanie po úspechu
      } else {

        const errorDiv = document.querySelector('.login-error') || document.createElement('div');
        errorDiv.className = 'login-error';
        errorDiv.style.color = 'red';
        errorDiv.textContent = data.error || 'Nesprávne prihlasovacie údaje.';
        loginForm.prepend(errorDiv);
      }
    } catch (err) {
      alert('Chyba pri prihlasovaní.');
    }
  });
})();