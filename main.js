/* Shared behavior for every page: sticky nav, mobile menu, scroll reveal, year. */
(function () {
  // sticky nav frosted state
  var nav = document.getElementById('nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 40); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // mobile menu toggle
  var burger = document.getElementById('burger');
  if (burger) {
    burger.addEventListener('click', function () {
      document.getElementById('navlinks').classList.toggle('open');
    });
  }

  // scroll reveal
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && els.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  // current year in footer
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
