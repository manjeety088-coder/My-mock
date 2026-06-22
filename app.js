
function setupSearch(inputId, itemSelector){
  const input = document.getElementById(inputId);
  if(!input) return;
  const items = Array.from(document.querySelectorAll(itemSelector));
  const empty = document.getElementById('noResults');
  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    let shown = 0;
    items.forEach(el => {
      const hay = (el.dataset.search || el.textContent || '').toLowerCase();
      const ok = hay.includes(q);
      el.classList.toggle('hidden', !ok);
      if(ok) shown++;
    });
    if(empty) empty.classList.toggle('hidden', shown !== 0);
  });
}
document.addEventListener('DOMContentLoaded', () => {
  setupSearch('searchInput', '[data-search]');
});
