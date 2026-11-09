/* Where the wolves were: the map. The Inked World base map with every place and hill name that keeps an animal,
 * an animal picker, language and certainty filters, search and popups.
 * Dr Tristan Hotham, Independent researcher, 2026. MIT licence. */
(function () {
  'use strict';
  const qs = new URLSearchParams(location.search);
  const BASE = window.INKBASE;
  const V = '?v=20261108';
  const ENGINE = ['js/curated.js', 'js/ink-palette.js', 'js/ink-icons.js', 'js/ink-houses.js', 'js/ink-map.js', 'js/ink-extras.js'];
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const norm = s => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const small = matchMedia('(max-width:800px)').matches;
  const START = small ? [[-8.6, 50.0], [1.8, 58.7]] : [[-10.6, 49.9], [2.2, 59.0]];
  const LCOL = { english: '#A3261B', norse: '#C77A2A', welsh: '#2F7F4A', gaelic: '#3D6E9E', irish: '#5C8F3A', modern: '#6E604E' };
  let map = null, D = null, PL = null, cur = qs.get('animal') || 'all';
  const state = { certain: true, probable: true, layers: new Set(Object.keys(LCOL)) };

  document.getElementById('theme').addEventListener('click', () => {
    const r = document.documentElement, dark = r.dataset.theme ? r.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    r.dataset.theme = dark ? 'light' : 'dark';
  });
  const ct = document.getElementById('cartouche');
  const fold = f => ct.classList.toggle('folded', f);
  if (small) fold(true);
  document.getElementById('ctToggle').addEventListener('click', () => fold(!ct.classList.contains('folded')));
  document.getElementById('ctFold').addEventListener('click', () => fold(true));

  function loadScripts(list) {
    return list.reduce((p, src) => p.then(() => new Promise((res, rej) => {
      const el = document.createElement('script'); el.src = BASE + src + V; el.onload = res; el.onerror = () => rej(new Error('script ' + src)); document.head.appendChild(el);
    })), Promise.resolve());
  }

  // ---------------- popups
  let popup = null;
  function showPopup(r, lngLat) {
    const A = D.animals[r[3]], L = D.layers[r[4]];
    const lost = D.lost.filter(x => x.animal === A[0]);
    const kind = D.kinds[r[6]].replace('_', ' ');
    let h = `<b class="t">${esc(r[2])}</b>`;
    if (r[12]) h += `<div class="nt">${esc(r[12])}</div>`;
    h += `<table><tr><td>Animal</td><td><span class="sw" style="background:${A[2]}"></span>${esc(A[1])}</td></tr>`
      + `<tr><td>Meaning</td><td>${esc(r[9])}</td></tr>`
      + (r[8] && r[8] !== r[9] ? `<tr><td>Element</td><td>${esc(r[8])}</td></tr>` : '')
      + `<tr><td>Language</td><td>${esc(L[1])}</td></tr>`
      + `<tr><td>Reading</td><td>${r[5] ? 'certain' : 'probable'}</td></tr>`
      + `<tr><td>What</td><td>${esc(kind)}, ${esc(r[7])}${r[11] != null ? ', ' + r[11] + ' m' : ''}</td></tr></table>`;
    if (lost.length) h += `<p class="nt">Lost in the wild: ${lost.map(x => esc(x.label.replace(/^[^,]*, ?/, '') || x.label) + ' ' + esc(x.when)).join('; ')} (${esc(lost[0].src)}).</p>`;
    h += `<p class="nt">${r[5] ? (L[0] === 'english' || L[0] === 'norse' ? 'Etymology as given by the standard place-name dictionaries (Mills, Watts, Ekwall).' : 'The word is the ordinary ' + esc(L[1]) + ' word for the animal.') : (L[0] === 'modern' ? 'A descriptive English or Scots name: it may recall the animal, or a story, a surname or an inn sign.' : 'Probable: one of several possible readings.')}</p>`;
    h += `<div class="lk"><a href="https://www.openstreetmap.org/${esc(r[10])}" target="_blank" rel="noopener">OpenStreetMap</a></div>`;
    if (popup) popup.remove();
    popup = new maplibregl.Popup({ maxWidth: '320px', offset: 8, anchor: small ? 'top' : undefined }).setLngLat(lngLat).setHTML(h).addTo(map);
    if (small) map.easeTo({ center: lngLat, offset: [0, -220], duration: 600 });
  }

  // ---------------- filters
  function filterExpr() {
    const f = ['all'];
    if (cur !== 'all') f.push(['==', ['get', 'a'], D.animals.findIndex(a => a[0] === cur)]);
    const c = []; if (state.certain) c.push(1); if (state.probable) c.push(0);
    f.push(['in', ['get', 'c'], ['literal', c]]);
    f.push(['in', ['get', 'l'], ['literal', [...state.layers].map(l => D.layers.findIndex(x => x[0] === l))]]);
    return f;
  }
  function colourExpr() {
    if (cur === 'all') return ['match', ['get', 'a'], ...D.animals.flatMap((a, i) => [i, a[2]]), '#2B2119'];
    return ['match', ['get', 'l'], ...D.layers.flatMap((l, i) => [i, LCOL[l[0]]]), '#2B2119'];
  }
  function apply() {
    const f = filterExpr();
    map.setFilter('nm', f); map.setFilter('nmc', ['all', f, ['==', ['get', 'c'], 1]]); map.setFilter('nml', f);
    map.setPaintProperty('nm', 'circle-color', colourExpr()); map.setPaintProperty('nmc', 'circle-color', colourExpr());
    document.querySelectorAll('.chip[data-a]').forEach(b => b.setAttribute('aria-pressed', b.dataset.a === cur));
    // key
    const k = document.getElementById('key');
    if (cur === 'all') {
      k.innerHTML = '<b>Animal</b>' + D.animals.map(a => `<div class="row"><i class="dot" style="background:${a[2]}"></i>${esc(a[1])}</div>`).join('');
    } else {
      const n = D.rows.filter(r => D.animals[r[3]][0] === cur && r[13]).length;
      const A = D.animals.find(a => a[0] === cur);
      const lost = D.lost.filter(x => x.animal === cur);
      k.innerHTML = `<b>${esc(A[1])}: ${n} places</b>` + D.layers.map(l => `<div class="row"><i class="dot" style="background:${LCOL[l[0]]}"></i>${esc(l[1])}</div>`).join('')
        + (lost.length ? `<div class="row nt">Lost: ${lost.map(x => { const l = x.label.includes(',') ? x.label.split(', ')[1] : (/^White/.test(x.label) ? x.label : ''); return esc((l ? l + ' ' : '') + x.when); }).join('; ')}</div>` : '');
    }
    k.innerHTML += '<div class="row nt"><i class="dot big"></i>certain <i class="dot"></i>probable</div>';
    const u = new URL(location.href); if (cur === 'all') u.searchParams.delete('animal'); else u.searchParams.set('animal', cur); history.replaceState(null, '', u);
  }

  // ---------------- search: the animal names first, then towns and villages
  function setupSearch() {
    const q = document.getElementById('q'), sug = document.getElementById('sug');
    let items = [], k = -1;
    const names = D.rows.filter(r => r[13]).map(r => ({ t: 'n', name: r[2], sub: D.animals[r[3]][1] + ' · ' + r[7], lon: r[0], lat: r[1], r }));
    const towns = PL.places.map(p => ({ t: 'p', name: p[0], sub: p[4], lon: p[1], lat: p[2], rank: p[3] }));
    const show = () => {
      const v = norm(q.value.trim()); sug.innerHTML = ''; k = -1;
      if (!v) { sug.style.display = 'none'; return; }
      const m = (arr) => arr.filter(p => norm(p.name).startsWith(v)).concat(arr.filter(p => !norm(p.name).startsWith(v) && norm(p.name).includes(v)));
      items = m(names).slice(0, 7).concat(m(towns).slice(0, 12)).slice(0, 14);
      items.forEach((p, i) => { const li = document.createElement('li'); li.setAttribute('role', 'option');
        li.innerHTML = `${esc(p.name)} <span>${p.t === 'n' ? 'name: ' : ''}${esc(p.sub)}</span>`;
        li.addEventListener('mousedown', e => { e.preventDefault(); pick(i); }); sug.appendChild(li); });
      sug.style.display = items.length ? 'block' : 'none';
    };
    const pick = i => {
      const p = items[i]; if (!p) return; q.value = p.name; sug.style.display = 'none'; fold(true);
      map.flyTo({ center: [p.lon, p.lat], zoom: Math.max(map.getZoom(), p.t === 'n' ? 11.5 : 11), duration: 1300 });
      if (p.t === 'n') { if (cur !== 'all' && D.animals[p.r[3]][0] !== cur) { cur = 'all'; apply(); } map.once('moveend', () => showPopup(p.r, [p.lon, p.lat])); }
    };
    q.addEventListener('input', show);
    q.addEventListener('keydown', e => {
      const lis = [...sug.children];
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); k = Math.max(0, Math.min(lis.length - 1, k + (e.key === 'ArrowDown' ? 1 : -1))); lis.forEach((l, i) => l.setAttribute('aria-selected', i === k)); }
      else if (e.key === 'Enter') { e.preventDefault(); if (!items.length) show(); pick(k < 0 ? 0 : k); }
      else if (e.key === 'Escape') sug.style.display = 'none';
    });
    q.addEventListener('blur', () => setTimeout(() => sug.style.display = 'none', 150));
  }

  // ---------------- layers
  function setupLayers() {
    const feats = D.rows.map((r, i) => ({ type: 'Feature', properties: { i, a: r[3], l: r[4], c: r[5], n: r[2], h: r[13] }, geometry: { type: 'Point', coordinates: [r[0], r[1]] } }));
    map.addSource('nm', { type: 'geojson', data: { type: 'FeatureCollection', features: feats }, attribution: 'Names: OpenStreetMap contributors (ODbL)' });
    map.addLayer({ id: 'nm', type: 'circle', source: 'nm', paint: {
      'circle-radius': ['interpolate', ['linear'], ['zoom'], 5, 2.6, 8, 4.2, 12, 7], 'circle-color': '#2B2119',
      'circle-stroke-color': '#FBF5E4', 'circle-stroke-width': ['interpolate', ['linear'], ['zoom'], 5, 0.5, 10, 1.2], 'circle-opacity': 0.92 } });
    map.addLayer({ id: 'nmc', type: 'circle', source: 'nm', paint: {
      'circle-radius': ['interpolate', ['linear'], ['zoom'], 5, 4.2, 8, 6.5, 12, 10], 'circle-color': '#2B2119',
      'circle-stroke-color': '#2B2119', 'circle-stroke-width': ['interpolate', ['linear'], ['zoom'], 5, 0.8, 10, 1.6] } });
    map.addLayer({ id: 'nml', type: 'symbol', source: 'nm', minzoom: 8.5,
      layout: { 'text-field': ['get', 'n'], 'text-font': ['Ink Italic'], 'text-size': ['interpolate', ['linear'], ['zoom'], 8.5, 11.5, 13, 15], 'text-offset': [0, 0.95],
        'text-anchor': 'top', 'text-optional': true, 'symbol-sort-key': ['-', 1, ['get', 'c']] },
      paint: { 'text-color': '#2B2119', 'text-halo-color': 'rgba(251,245,228,0.95)', 'text-halo-width': 1.6 } });
    for (const id of ['nm', 'nmc']) {
      map.on('click', id, e => { const f = e.features[0]; if (f) showPopup(D.rows[f.properties.i], e.features[0].geometry.coordinates); });
      map.on('mouseenter', id, () => map.getCanvas().style.cursor = 'pointer');
      map.on('mouseleave', id, () => map.getCanvas().style.cursor = '');
    }
    const lp = document.getElementById('lp'), btn = document.getElementById('lyrBtn');
    btn.addEventListener('click', () => { const o = lp.classList.toggle('open'); btn.setAttribute('aria-expanded', o); });
    document.querySelectorAll('.chip[data-a]').forEach(b => b.addEventListener('click', () => { cur = b.dataset.a; apply(); }));
    document.getElementById('ckCert').addEventListener('change', e => { state.certain = e.target.checked; apply(); });
    document.getElementById('ckProb').addEventListener('change', e => { state.probable = e.target.checked; apply(); });
    document.querySelectorAll('input[data-l]').forEach(b => b.addEventListener('change', () => { b.checked ? state.layers.add(b.dataset.l) : state.layers.delete(b.dataset.l); apply(); }));
    const vis = (id, on) => map.setLayoutProperty(id, 'visibility', on ? 'visible' : 'none');
    document.getElementById('ckNames').addEventListener('change', e => { vis('nm', e.target.checked); vis('nmc', e.target.checked); vis('nml', e.target.checked && document.getElementById('ckLab').checked); });
    document.getElementById('ckLab').addEventListener('change', e => vis('nml', e.target.checked && document.getElementById('ckNames').checked));
    const boxes = [...lp.querySelectorAll('input[data-g]')], modern = document.getElementById('modern');
    const base = () => {
      const m = modern.checked;
      boxes.forEach(b => { const g = b.dataset.g; const inkOnly = ['mountains', 'forests', 'sea', 'tint'].includes(g); try { InkMap.setGroup(map, g, b.checked && !(m && inkOnly)); } catch (e) { } });
      try { InkMap.setGroup(map, 'paper', !m); InkMap.setGroup(map, 'modern', m); InkMap.setGroup(map, 'coast', !m); if (m) InkMap.setGroup(map, 'roads', false); } catch (e) { }
    };
    boxes.forEach(b => b.addEventListener('change', base)); modern.addEventListener('change', base); base();
    apply();
  }

  // ---------------- start
  Promise.all([fetch('data/names.json').then(r => r.json()), fetch('data/places.json').then(r => r.json())]).then(([j, p]) => {
    D = j; PL = p;
    if (cur !== 'all' && !D.animals.some(a => a[0] === cur)) cur = 'all';
    const opts = { base: BASE, winter: false };
    if (qs.get('tj')) opts.tilejson = qs.get('tj');
    if (qs.get('dem')) opts.dem = qs.get('dem');
    if (qs.get('demmax')) opts.demMax = +qs.get('demmax');
    const at = (qs.get('at') || '').split(',').map(Number);
    opts.mapOptions = at.length === 3 && at.every(isFinite) ? { center: [at[1], at[0]], zoom: at[2] } : { bounds: START, fitBoundsOptions: { padding: 6 } };
    return loadScripts(ENGINE).then(() => InkMap.create('map', opts));
  }).then(m => {
    map = m; window.__map = m;
    const n = document.getElementById('nojs'); if (n) n.remove();
    m.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right');
    const foldAt = () => document.querySelectorAll('.maplibregl-ctrl-attrib.maplibregl-compact').forEach(at => { at.classList.remove('maplibregl-compact-show'); at.removeAttribute('open'); });
    m.once('idle', foldAt); m.on('resize', () => setTimeout(foldAt, 50)); setTimeout(foldAt, 1500);
    setupLayers(); setupSearch();
    const first = e => { if (e.target.closest && e.target.closest('.cartouche,.ov,.lp,.keys,.mfs-btn,.maplibregl-ctrl,.maplibregl-popup')) return; fold(true); };
    document.getElementById('mapWrap').addEventListener('pointerdown', first, { capture: true, passive: true, once: true });
    document.querySelectorAll('a[data-animal]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); cur = a.dataset.animal; apply(); document.getElementById('mapWrap').scrollIntoView({ behavior: 'smooth' }); }));
    if (qs.get('open')) { const r = D.rows.find(r => r[10] === qs.get('open')); if (r) showPopup(r, [r[0], r[1]]); }
  }).catch(e => { console.error(e); const n = document.getElementById('nojs'); if (n) n.textContent = 'The map could not load: ' + e.message; });
})();
