(function() {
  'use strict';
  
  const form = document.querySelector('form[method="post"]');
  if (!form) return;

  const emailField = form.querySelector('input[type="email"]');
  const password1 = form.querySelector('input[name="password1"]');
  const password2 = form.querySelector('input[name="password2"]');
  
  function showError(field, msg) {
    let err = field.nextElementSibling;
    if (!err || !err.classList.contains('error-msg')) {
      err = document.createElement('span');
      err.className = 'error-msg';
      err.style.color = '#dc3545';
      err.style.fontSize = '0.875rem';
      err.style.display = 'block';
      err.style.marginTop = '4px';
      field.parentNode.appendChild(err);
    }
    err.textContent = msg;
    field.style.borderColor = '#dc3545';
  }
  
  function clearError(field) {
    const err = field.nextElementSibling;
    if (err && err.classList.contains('error-msg')) err.textContent = '';
    field.style.borderColor = '';
  }

  if (emailField) {
    emailField.addEventListener('blur', function() {
      const val = this.value.trim();
      if (!val) { clearError(this); return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
        showError(this, 'Neplatný formát emailu.');
      } else {
        clearError(this);
      }
    });
  }

  if (password1) {
    password1.addEventListener('input', function() {
      if (this.value.length > 0 && this.value.length < 8) {
        showError(this, 'Heslo musí mať aspoň 8 znakov.');
      } else {
        clearError(this);
      }
    });
  }

  if (password2 && password1) {
    password2.addEventListener('input', function() {
      if (this.value && this.value !== password1.value) {
        showError(this, 'Heslá sa nezhodujú.');
      } else {
        clearError(this);
      }
    });
  }

  form.addEventListener('submit', function(e) {
    let valid = true;
    if (emailField && emailField.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailField.value.trim())) {
      showError(emailField, 'Neplatný email.');
      valid = false;
    }
    if (password1 && password1.value.length < 8) {
      showError(password1, 'Heslo príliš krátke.');
      valid = false;
    }
    if (password2 && password1 && password2.value !== password1.value) {
      showError(password2, 'Heslá sa nezhodujú.');
      valid = false;
    }
    if (!valid) e.preventDefault();
  });
})();