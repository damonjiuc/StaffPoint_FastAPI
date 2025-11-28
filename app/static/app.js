(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const dropdown = document.querySelector('.menu-region.dropdown');
    if (!dropdown) return;

    const toggle = dropdown.querySelector('.dropdown-toggle');
    const menu = dropdown.querySelector('.dropdown-menu');
    if (!toggle || !menu) return;

    // собираем все допустимые slugs регионов из меню (кроме пустой строки)
    const menuItems = Array.from(menu.querySelectorAll('li[data-region]'));
    const knownRegionSlugs = menuItems
      .map(i => (i.dataset.region || '').trim())
      .filter(s => s.length > 0);

    // helper: убрать префикс региона из текущего pathname, если он есть
    function stripRegionPrefix(parts) {
      if (parts.length === 0) return parts;
      if (knownRegionSlugs.includes(parts[0])) {
        parts.shift();
      }
      return parts;
    }

    // открытие/закрытие меню
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      dropdown.classList.toggle('open');
    });

    // делегируем клик на пункты меню
    menu.addEventListener('click', function (e) {
      const li = e.target.closest('li[data-region]');
      if (!li) return;
      e.stopPropagation();

      const selectedRegion = (li.dataset.region || '').trim(); // "" или "spb"

      // берем текущий путь и разбиваем на части
      const rawParts = window.location.pathname.split('/').filter(Boolean); // ['spb', 'merchandajzing'] или ['merchandajzing'] или []
      const parts = stripRegionPrefix(rawParts.slice()); // копия, с префиксом убранным, если был

      // собираем serviceSlug (всё, что осталось)
      const serviceSlug = parts.join('/'); // '' если корень

      // билдим новый путь
      let newPath;
      if (selectedRegion) {
        newPath = '/' + selectedRegion + (serviceSlug ? '/' + serviceSlug : '');
      } else if (serviceSlug) {
        newPath = '/' + serviceSlug;
      } else {
        newPath = '/';
      }

      // переход
      window.location.href = newPath;
    });

    // закрываем при клике вне
    document.addEventListener('click', function () {
      dropdown.classList.remove('open');
    });

    // optional: клавиатурная доступность: Esc закрывает
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') dropdown.classList.remove('open');
    });
  });
})();