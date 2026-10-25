/* Global Chef League — small site behaviours. No dependencies. */
(function () {
  // ---- Mobile nav ----
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.classList.toggle('nav-open', open);
    });
  }

  // ---- Directory search + filters (Find a Chef) ----
  var dir = document.getElementById('directory');
  if (dir) {
    var rows = Array.prototype.slice.call(dir.querySelectorAll('.dir-row[data-name]'));
    var q = document.getElementById('f-search');
    var svc = document.getElementById('f-service');
    var role = document.getElementById('f-role');
    var count = document.getElementById('dir-count-n');
    var empty = document.getElementById('dir-empty');
    var tags = Array.prototype.slice.call(document.querySelectorAll('.filter-tags .badge--tag'));

    var params = new URLSearchParams(location.search);
    if (params.get('q')) q.value = params.get('q');
    if (params.get('service')) svc.value = params.get('service');
    if (params.get('designation')) role.value = params.get('designation');

    function apply() {
      var term = (q.value || '').trim().toLowerCase();
      var s = svc.value, r = role.value, n = 0;
      rows.forEach(function (row) {
        var hay = (row.dataset.name + ' ' + row.dataset.city + ' ' + row.dataset.specialty).toLowerCase();
        var ok = (!term || hay.indexOf(term) > -1) &&
                 (!s || row.dataset.services.split('|').indexOf(s) > -1) &&
                 (!r || row.dataset.roles.split('|').indexOf(r) > -1);
        row.style.display = ok ? '' : 'none';
        if (ok) n++;
      });
      count.textContent = n + (n === 1 ? ' profile' : ' profiles');
      empty.style.display = n ? 'none' : 'block';
      tags.forEach(function (t) { t.setAttribute('aria-pressed', t.dataset.service === s ? 'true' : 'false'); });
    }
    document.getElementById('dir-form').addEventListener('submit', function (e) { e.preventDefault(); apply(); });
    q.addEventListener('input', apply);
    svc.addEventListener('change', apply);
    role.addEventListener('change', apply);
    tags.forEach(function (t) {
      t.addEventListener('click', function () {
        svc.value = svc.value === t.dataset.service ? '' : t.dataset.service;
        apply();
      });
    });
    apply();
  }

  // ---- Photo upload preview (Submit Profile) ----
  var up = document.getElementById('photo');
  if (up) {
    up.addEventListener('change', function () {
      var box = up.closest('.upload');
      var old = box.querySelector('img'); if (old) old.remove();
      if (up.files && up.files[0]) {
        var img = document.createElement('img');
        img.alt = 'Selected profile photo';
        img.src = URL.createObjectURL(up.files[0]);
        box.appendChild(img);
      }
    });
  }

  // ---- Forms: post to Formspree (or any endpoint that accepts form posts) ----
  Array.prototype.forEach.call(document.querySelectorAll('form[data-ajax]'), function (form) {
    form.addEventListener('submit', function (e) {
      var msg = form.querySelector('.form-msg');
      // Services: at least one checkbox
      var group = form.querySelector('[data-require-one]');
      if (group && !group.querySelector('input:checked')) {
        e.preventDefault();
        show(msg, 'err', 'Please choose at least one service you offer.');
        group.querySelector('input').focus();
        return;
      }
      // Contact method: at least one of email / phone / booking link
      var contactFields = form.querySelectorAll('[data-contact-method]');
      if (contactFields.length && !Array.prototype.some.call(contactFields, function (f) { return f.value.trim(); })) {
        e.preventDefault();
        show(msg, 'err', 'Add at least one public contact method (email, phone, or booking link) so customers can reach you.');
        contactFields[0].focus();
        return;
      }
      if (form.action.indexOf('REPLACE_') > -1) {
        e.preventDefault();
        show(msg, 'err', 'This form is not connected yet. Site owner: add your Formspree form ID (see README).');
        return;
      }
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (res) {
          if (res.ok) {
            form.reset();
            var img = form.querySelector('.upload img'); if (img) img.remove();
            show(msg, 'ok', form.dataset.success || 'Thanks! Your message has been sent.');
          } else {
            return res.json().then(function (d) {
              throw new Error(d && d.errors ? d.errors.map(function (x) { return x.message; }).join(' ') : 'Something went wrong.');
            });
          }
        })
        .catch(function (err) { show(msg, 'err', (err && err.message) || 'Something went wrong. Please try again.'); })
        .then(function () { btn.disabled = false; });
    });
  });

  function show(el, kind, text) {
    if (!el) return;
    el.className = 'form-msg ' + kind;
    el.textContent = text;
    el.setAttribute('role', kind === 'err' ? 'alert' : 'status');
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  // ---- Footer year ----
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
