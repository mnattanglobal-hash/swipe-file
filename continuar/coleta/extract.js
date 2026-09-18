(() => {
  const marker = 'Identificação da biblioteca';
  const count = (el) => (el.innerText || '').split(marker).length - 1;
  const leaves = [...document.querySelectorAll('div')].filter(d => count(d) === 1 && !d.querySelector('div'));
  const roots = new Set();
  for (const leaf of leaves) {
    let el = leaf, best = leaf;
    while (el.parentElement && count(el.parentElement) === 1) { el = el.parentElement; best = el; }
    roots.add(best);
  }
  const clean = (h) => {
    try { const u = new URL(h); if (u.hostname.includes('l.facebook.com')) return decodeURIComponent(u.searchParams.get('u')||h); return h; } catch(e){ return h; }
  };
  const out = [];
  for (const r of roots) {
    const t = r.innerText || '';
    const id = (t.match(/Identificação da biblioteca:\s*(\d+)/) || [])[1];
    if (!id) continue;
    const start = (t.match(/Veiculação iniciada em ([^\n]+)/) || [])[1] || '';
    const variants = (t.match(/(\d+)\s+an[úu]ncios? usa[m]? esse criativo/) || [])[1] || '';
    const imgs = [...r.querySelectorAll('img')].map(i => i.src).filter(s => s && s.includes('fbcdn') && !/s60x60|p60x60/.test(s));
    const vnodes = [...r.querySelectorAll('video')];
    const vids = vnodes.map(v => v.poster || '').filter(Boolean);
    const vsrc = vnodes.map(v => v.src || (v.querySelector('source')||{}).src || '').filter(Boolean);
    const all = [...new Set([...r.querySelectorAll('a')].map(a => clean(a.href)))];
    const page = all.filter(h => /facebook\.com\/(?!ads\/library)/.test(h));
    const dest = all.filter(h => !/facebook\.com/.test(h));
    out.push({id, start, variants, media: vids.length? 'video':'image', thumbs: vids.length? vids : imgs.slice(0,2), video: vsrc[0]||'', page: page[0]||'', dest: dest[0]||'', text: t});
  }
  return JSON.stringify(out);
})()
