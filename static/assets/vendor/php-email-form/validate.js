document.addEventListener("DOMContentLoaded", function() {
  const form = document.querySelector('.php-email-form');

  form.addEventListener('submit', function(event) {
      event.preventDefault();
      if (!validateForm()) {
          return;
      }

      const formData = new FormData(form);

      fetch(form.action, {
          method: 'POST',
          body: formData
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          form.reset();
          // Handle success message here if needed
      })
      .catch(error => {
          console.error('There was a problem with your fetch operation:', error);
          // Handle error message here if needed
      });
  });

  function validateForm() {
      let valid = true;

      const inputs = form.querySelectorAll('input, select');
      inputs.forEach(input => {
          if (!input.checkValidity()) {
              valid = false;
              input.classList.add('is-invalid');
          } else {
              input.classList.remove('is-invalid');
          }
      });

      return valid;
  }
});
