<script>
/* Route 404, animated. Progressive enhancement: the words and both paragraphs are
   real text in the markup, so with no JS the page is simply static and complete.
   The .js class is what opts in to the hidden-then-revealed states. */
(function () {
  var root = document.documentElement;
  root.className += ' js';
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;

  var words = [].slice.call(document.querySelectorAll('.r404-word, .r404-big'));
  var box   = document.querySelector('.r404-box');
  var cta   = document.querySelector('.r404-cta');
  var more  = document.querySelector('.r404-more');
  var paras = [].slice.call(box.querySelectorAll('p'));
  var lines = paras.map(function (el) { return el.textContent; });

  // split into per-character spans so each pixel glyph can land on its own
  var chars = [];
  words.forEach(function (w) {
    var text = w.textContent;
    w.textContent = '';
    for (var i = 0; i < text.length; i++) {
      var sp = document.createElement('span');
      sp.className = 'r404-ch';
      sp.textContent = text[i];
      w.appendChild(sp);
      chars.push(sp);
    }
  });

  if (still) {                       // no motion: show everything at once
    chars.forEach(function (c) { c.style.opacity = 1; });
    box.style.opacity = 1; cta.style.opacity = 1; more.classList.add('on');
    return;
  }

  paras.forEach(function (el) { el.textContent = ''; });

  var STEP = 70;                     // between characters
  chars.forEach(function (c, i) {
    setTimeout(function () { c.classList.add('in'); }, i * STEP);
  });

  var after = chars.length * STEP + 220;
  setTimeout(function () { box.classList.add('in'); type(0); }, after);
  setTimeout(function () { cta.classList.add('in'); }, after + 260);

  function type(n) {
    if (n >= lines.length) { more.classList.add('on'); return; }
    var el = paras[n], text = lines[n], i = 0;
    var t = setInterval(function () {
      el.textContent = text.slice(0, ++i);
      if (i >= text.length) { clearInterval(t); setTimeout(function () { type(n + 1); }, 240); }
    }, 16);
  }
})();
</script>