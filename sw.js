const CACHE_NAME = "lokalizator-pwa-v1";

self.addEventListener("install", event => {
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", event => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return new Response(
        "<h1>Offline</h1><p>Brak połączenia z internetem</p>",
        { headers: { "Content-Type": "text/html; charset=utf-8" } }
      );
    })
  );
});
