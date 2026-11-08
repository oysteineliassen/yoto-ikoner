// Nett først (så nye ikonsett og oppdateringer alltid kommer med), cache som reserve.
const CACHE = 'yoto-ikoner-v2';
const SKALL = ['./', './index.html', './manifest.webmanifest', './app-ikon/ikon-192.png', './app-ikon/ikon-512.png',
  'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SKALL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(k => Promise.all(k.filter(n => n !== CACHE).map(n => caches.delete(n))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  // Aldri mellomlagre Yoto-innlogging eller API
  if (url.hostname.endsWith('yotoplay.com')) return;
  if (url.origin !== location.origin && !url.hostname.includes('cdnjs')) return;
  e.respondWith(
    fetch(e.request).then(svar => {
      if (svar.ok) { const kopi = svar.clone(); caches.open(CACHE).then(c => c.put(e.request, kopi)); }
      return svar;
    }).catch(() => caches.match(e.request, { ignoreSearch: true }))
  );
});
