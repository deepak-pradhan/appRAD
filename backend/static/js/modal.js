document.addEventListener('htmx:afterSwap', function(event) {
  if (event.detail.target.id === 'edit-modal') {
    document.querySelector('#edit-modal').classList.add('is-active');
  }
});

document.querySelector('.modal-close').addEventListener('click', function() {
  document.querySelector('#edit-modal').classList.remove('is-active');
});

document.addEventListener('htmx:afterSwap', function(event) {
    if (event.detail.target.id === 'tenant-details') {
        document.querySelector('#tenant-details').classList.add('is-active');
    }
});

document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.detail.target.id === 'tenant-form') {
        document.querySelector('#tenant-details').classList.remove('is-active');
    }
});

document.addEventListener('click', function(event) {
  if (event.target.closest('.close-details')) {
    document.querySelector('#tenant-details').innerHTML = '';
  }
});
