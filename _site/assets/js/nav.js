(() => {
  const btn = document.querySelector('[data-menu-button]');
  const panel = document.querySelector('[data-menu-panel]');
  const closeButtons = document.querySelectorAll('[data-menu-close]');
  const backdrop = document.querySelector('[data-menu-backdrop]');

  if (!btn || !panel) return;

  const open = () => {
    panel.classList.add('is-open');
    backdrop?.classList.add('is-open');
    document.body.classList.add('menu-open');
    btn.setAttribute('aria-expanded', 'true');
  };

  const close = () => {
    panel.classList.remove('is-open');
    backdrop?.classList.remove('is-open');
    document.body.classList.remove('menu-open');
    btn.setAttribute('aria-expanded', 'false');
  };

  btn.addEventListener('click', () => {
    if (panel.classList.contains('is-open')) close();
    else open();
  });

  closeButtons.forEach((button) => button.addEventListener('click', close));
  backdrop?.addEventListener('click', close);
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') close();
  });
})();
