/* Vatican Glamorous – banner consenso cookie (Google Consent Mode v2) + eventi GA4
   Il consenso predefinito (tutto "denied") e il caricamento di gtag.js sono nell'<head> di ogni pagina. */
(function () {
  'use strict';
  var KEY = 'vg_consent_v1';
  var IT = (document.documentElement.lang || 'it').slice(0, 2) === 'it';
  var script = document.currentScript;
  var base = script && script.src ? script.src.replace(/assets\/consent\.js.*$/, '') : '/';
  var DIRECT = 'https://direct-book.com/properties/passeggiatadelgelsomino';
  window.dataLayer = window.dataLayer || [];
  function gt() { window.dataLayer.push(arguments); }
  var gtag = window.gtag || gt;

  /* ---------- consenso ---------- */
  function read() { try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; } }
  function save(granted) { try { localStorage.setItem(KEY, JSON.stringify({ granted: granted, ts: Date.now() })); } catch (e) {} }
  function apply(granted) {
    var v = granted ? 'granted' : 'denied';
    gtag('consent', 'update', { ad_storage: v, ad_user_data: v, ad_personalization: v, analytics_storage: v });
  }

  var banner = null;
  function closeBanner() { if (banner) { banner.remove(); banner = null; } }
  function openBanner() {
    if (banner) return;
    banner = document.createElement('div');
    banner.className = 'vg-consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', IT ? 'Preferenze cookie' : 'Cookie preferences');
    var p = document.createElement('p');
    p.appendChild(document.createTextNode(IT ? 'Cookie? ' : 'Cookies? '));
    var a = document.createElement('a');
    a.href = base + (IT ? 'it/privacy/' : 'en/privacy/');
    a.textContent = 'Info';
    p.appendChild(a);
    var btns = document.createElement('div');
    btns.className = 'vg-consent-btns';
    [['reject', 'No', false], ['accept', 'Ok', true]].forEach(function (b) {
      var el = document.createElement('button');
      el.type = 'button'; el.setAttribute('data-consent', b[0]); el.textContent = b[1];
      el.setAttribute('aria-label', b[2] ? (IT ? 'Accetta i cookie' : 'Accept cookies') : (IT ? 'Rifiuta i cookie' : 'Decline cookies'));
      el.addEventListener('click', function () { save(b[2]); apply(b[2]); closeBanner(); });
      btns.appendChild(el);
    });
    banner.appendChild(p); banner.appendChild(btns);
    document.body.appendChild(banner);
  }
  if (!read()) openBanner();
  document.addEventListener('click', function (e) {
    var s = e.target.closest && e.target.closest('[data-cookie-settings]');
    if (s) { e.preventDefault(); openBanner(); }
  });

  /* ---------- eventi GA4 ---------- */
  function clean(t) { return (t || '').replace(/\s+/g, ' ').trim().slice(0, 100); }
  function send(name, text, dest) {
    gtag('event', name, {
      page_location: location.href,
      button_text: clean(text),
      language: document.documentElement.lang || '',
      destination_url: dest || '',
      transport_type: 'beacon'
    });
    /* Google Ads: conversione "Click Prenota" */
    if (name === 'booking_click') {
      gtag('event', 'conversion', { send_to: 'AW-16744634075/GPY5CLva6YwdENutu7A-', transport_type: 'beacon' });
    }
  }
  function classify(a) {
    var raw = a.getAttribute('href') || '';
    if (/^tel:/i.test(raw)) return 'phone_click';
    if (/^mailto:/i.test(raw)) return 'email_click';
    var u; try { u = new URL(a.href, location.href); } catch (e) { return null; }
    if (/(^|\.)wa\.me$|(^|\.)whatsapp\.com$/i.test(u.hostname)) return 'whatsapp_click';
    var text = clean(a.getAttribute('aria-label') || a.textContent);
    if (/(^|\.)direct-book\.com$|(^|\.)airbnb\.[a-z.]+$|(^|\.)booking\.com$/i.test(u.hostname)) return 'booking_click';
    if (/\/(prenota|book)\/?$/i.test(u.pathname)) return 'booking_click';
    if (/\b(prenota|book)\b/i.test(text) && u.hostname !== 'www.getyourguide.com') return 'booking_click';
    return null;
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var name = classify(a);
    if (!name) return;
    var dest; try { dest = /^(tel|mailto):/i.test(a.getAttribute('href')) ? a.getAttribute('href') : new URL(a.href, location.href).href; } catch (x) { dest = a.href; }
    send(name, a.getAttribute('aria-label') || a.textContent, dest);
  }, true);
  /* ricerca date dal riquadro di prenotazione e dalla pagina Prenota */
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f.matches || !f.matches('[data-booking-form], [data-direct-book]')) return;
    var btn = e.submitter || f.querySelector('[type="submit"]');
    var dest = f.dataset.bookingUrl ? new URL(f.dataset.bookingUrl, location.href).href : DIRECT;
    send('booking_click', btn ? btn.textContent : '', dest);
  }, true);
})();
