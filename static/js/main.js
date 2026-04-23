// Potvrzení před vrácením knihy
document.querySelectorAll('.form-vratit').forEach(form => {
  form.addEventListener('submit', e => {
    if (!confirm('Opravdu vrátit tuto knihu?')) e.preventDefault();
  });
});
