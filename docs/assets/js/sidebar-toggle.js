document.addEventListener('DOMContentLoaded', function() {
  const toggleButtons = document.querySelectorAll('.sidebar-toggle');

  toggleButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();

      // Find the next sibling that is a ul.sidebar-sublinks
      let sublinks = this.parentElement.querySelector('ul.sidebar-sublinks');

      if (!sublinks) {
        return;
      }

      const isExpanded = this.getAttribute('aria-expanded') === 'true';

      // Toggle the state
      this.setAttribute('aria-expanded', !isExpanded);

      if (isExpanded) {
        // Collapse
        sublinks.classList.add('collapsed');
      } else {
        // Expand
        sublinks.classList.remove('collapsed');
      }
    });
  });
});
