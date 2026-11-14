const menuButton = document.querySelector('[data-menu-button]');
const menu = document.querySelector('[data-menu]');
const header = document.querySelector('[data-header]');

if (menuButton && menu) {
  menuButton.addEventListener('click', () => {
    const open = menu.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('menu-open', open);
  });
  menu.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
    menu.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('menu-open');
  }));
}

window.addEventListener('scroll', () => header?.classList.toggle('is-scrolled', window.scrollY > 32), { passive: true });

const addInfantsField = (form) => {
  if (form.elements.namedItem('infants')) return;
  const isItalian = form.dataset.locale === 'it';
  const grid = form.querySelector('.cv-date-row, .cv-book-grid');
  if (!grid) return;
  const wrapper = document.createElement('div');
  const id = `${form.matches('[data-direct-book]') ? 'book' : 'cv'}-infants-${isItalian ? 'it' : 'en'}`;
  const label = isItalian ? 'Neonati' : 'Infants';
  const age = isItalian ? '(meno di 2 anni)' : '(under 2)';
  wrapper.className = form.matches('[data-direct-book]') ? '' : 'cv-field';
  wrapper.innerHTML = `<label for="${id}">${label}<small>${age}</small></label><select id="${id}" name="infants"><option selected>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select>`;
  grid.appendChild(wrapper);
  const childrenLabel = form.querySelector('label[for*="children"], label[for*="bambini"]');
  if (childrenLabel && !childrenLabel.querySelector('small')) {
    childrenLabel.insertAdjacentHTML('beforeend', `<small>${isItalian ? '(2–12 anni)' : '(ages 2–12)'}</small>`);
  }
};

document.querySelectorAll('[data-booking-form], [data-direct-book]').forEach(addInfantsField);

document.querySelectorAll('[data-booking-form]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const destination = form.dataset.bookingUrl;
    if (!destination) {
      window.location.href = 'https://direct-book.com/properties/passeggiatadelgelsomino';
      return;
    }
    const values = new FormData(form);
    const url = new URL(destination, window.location.origin);
    url.searchParams.set('locale', form.dataset.locale || document.documentElement.lang || 'it');
    url.searchParams.set('checkInDate', values.get('checkin'));
    url.searchParams.set('checkOutDate', values.get('checkout'));
    url.searchParams.set('adults', values.get('adults') || '2');
    url.searchParams.set('children', values.get('children') || '0');
    url.searchParams.set('infants', values.get('infants') || '0');
    window.location.href = `${url.pathname}${url.search}`;
  });
});

document.querySelectorAll('[data-direct-book]').forEach((form) => {
  const isItalian = form.dataset.locale === 'it';
  const bookingSection = form.closest('section');
  const fallback = bookingSection?.querySelector('.cv-book-fallback');
  const fallbackLink = fallback?.querySelector('a');
  fallbackLink?.setAttribute('data-booking-fallback', '');
  const mobileBookingLink = document.querySelector('.cv-mobile-bar a:last-child');
  if (mobileBookingLink) mobileBookingLink.href = isItalian ? '#motore' : '#booking';
  const initialParams = new URLSearchParams(window.location.search);
  const fieldMap = {
    checkin: initialParams.get('checkInDate'),
    checkout: initialParams.get('checkOutDate'),
    adults: initialParams.get('adults'),
    children: initialParams.get('children'),
    infants: initialParams.get('infants')
  };
  Object.entries(fieldMap).forEach(([name, value]) => {
    const field = form.elements.namedItem(name);
    if (field && value !== null) field.value = value;
  });

  const getBookingUrl = () => {
    const values = new FormData(form);
    const url = new URL('https://direct-book.com/properties/passeggiatadelgelsomino');
    url.searchParams.set('locale', form.dataset.locale || 'en');
    url.searchParams.set('checkInDate', values.get('checkin'));
    url.searchParams.set('checkOutDate', values.get('checkout'));
    url.searchParams.set('items[0][adults]', values.get('adults'));
    url.searchParams.set('items[0][children]', values.get('children'));
    url.searchParams.set('items[0][infants]', values.get('infants'));
    url.searchParams.set('currency', 'EUR');
    return url;
  };

  const preserveSelection = () => {
    const values = new FormData(form);
    const bookingUrl = getBookingUrl();
    if (fallbackLink) fallbackLink.href = bookingUrl.toString();
    const localUrl = new URL(window.location.href);
    localUrl.searchParams.set('checkInDate', values.get('checkin'));
    localUrl.searchParams.set('checkOutDate', values.get('checkout'));
    localUrl.searchParams.set('adults', values.get('adults'));
    localUrl.searchParams.set('children', values.get('children'));
    localUrl.searchParams.set('infants', values.get('infants'));
    window.history.replaceState({}, '', localUrl);
    return bookingUrl;
  };

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    window.location.href = preserveSelection().toString();
  });

  preserveSelection();
});

const reveals = document.querySelectorAll('[data-reveal]');
if (typeof window.IntersectionObserver === 'function') {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  reveals.forEach((node) => observer.observe(node));
} else {
  reveals.forEach((node) => node.classList.add('is-visible'));
}

const photoCodes = new Map(); // i codici foto (H1, A2, C3...) sono scritti direttamente nell'HTML

const photoContainerSelector = [
  '.cv-hero-bg',
  '.cv-page-hero',
  '.cv-card-media',
  '.cv-feature-video',
  '.cv-destination-image',
  '.cv-editorial-media',
  '.cv-photo',
  '.cv-room-media'
].join(', ');

const lightboxPhotos = Array.from(document.querySelectorAll('body.elegance main img:not([data-no-lightbox])'));

lightboxPhotos.forEach((photo) => {
  if (photo.dataset.photoCode) return; // i codici attuali sono già nell'HTML: la vecchia tabella non va applicata
  const sourcePath = new URL(photo.getAttribute('src'), window.location.origin).pathname;
  const code = photoCodes.get(sourcePath);
  if (!code) return;
  photo.dataset.photoCode = code;
  const container = photo.closest(photoContainerSelector) || photo.parentElement;
  if (!container || container.querySelector(':scope > .cv-photo-code')) return;
  container.classList.add('cv-coded-photo');
  const badge = document.createElement('span');
  badge.className = 'cv-photo-code';
  badge.textContent = code;
  badge.setAttribute('aria-hidden', 'true');
  container.appendChild(badge);
});

if (lightboxPhotos.length) {
  const isItalian = document.documentElement.lang === 'it';
  const labels = isItalian
    ? { close: 'Chiudi foto', previous: 'Foto precedente', next: 'Foto successiva', enlarge: 'Ingrandisci foto' }
    : { close: 'Close photo', previous: 'Previous photo', next: 'Next photo', enlarge: 'Enlarge photo' };
  const lightbox = document.createElement('div');
  let activeIndex = 0;
  let hideTimer;

  lightbox.className = 'cv-lightbox';
  lightbox.hidden = true;
  lightbox.innerHTML = `
    <div class="cv-lightbox-dialog" role="dialog" aria-modal="true" aria-label="${labels.enlarge}">
      <button class="cv-lightbox-close" type="button" aria-label="${labels.close}">×</button>
      <button class="cv-lightbox-nav cv-lightbox-prev" type="button" aria-label="${labels.previous}">‹</button>
      <figure class="cv-lightbox-figure">
        <img class="cv-lightbox-image" alt="">
        <figcaption class="cv-lightbox-caption"></figcaption>
      </figure>
      <button class="cv-lightbox-nav cv-lightbox-next" type="button" aria-label="${labels.next}">›</button>
    </div>`;
  document.body.appendChild(lightbox);

  const lightboxImage = lightbox.querySelector('.cv-lightbox-image');
  const lightboxCaption = lightbox.querySelector('.cv-lightbox-caption');
  const closeButton = lightbox.querySelector('.cv-lightbox-close');
  let touchStartX = 0;
  let touchStartY = 0;

  const showPhoto = (index) => {
    activeIndex = (index + lightboxPhotos.length) % lightboxPhotos.length;
    const photo = lightboxPhotos[activeIndex];
    lightboxImage.src = photo.currentSrc || photo.src;
    lightboxImage.alt = photo.alt || '';
    const code = photo.dataset.photoCode;
    lightboxCaption.textContent = [code, photo.alt].filter(Boolean).join(' · ');
    lightboxCaption.hidden = !code && !photo.alt;
  };

  // Foto "singole" (data-lightbox-single): si ingrandiscono ma non si scorre verso le altre
  let singleMode = false;
  const isSingle = (i) => lightboxPhotos[(i + lightboxPhotos.length) % lightboxPhotos.length].hasAttribute('data-lightbox-single');
  const step = (dir) => {
    if (singleMode) return;
    let i = activeIndex;
    for (let k = 0; k < lightboxPhotos.length; k += 1) { i += dir; if (!isSingle(i)) break; }
    showPhoto(i);
  };

  const openLightbox = (index) => {
    window.clearTimeout(hideTimer);
    singleMode = isSingle(index);
    lightbox.classList.toggle('is-single', singleMode);
    showPhoto(index);
    lightbox.hidden = false;
    document.body.classList.add('lightbox-open');
    window.requestAnimationFrame(() => lightbox.classList.add('is-open'));
    closeButton.focus();
  };

  const closeLightbox = () => {
    lightbox.classList.remove('is-open');
    document.body.classList.remove('lightbox-open');
    hideTimer = window.setTimeout(() => {
      lightbox.hidden = true;
      lightboxImage.removeAttribute('src');
    }, 180);
    lightboxPhotos[activeIndex]?.focus({ preventScroll: true });
  };

  lightboxPhotos.forEach((photo, index) => {
    photo.classList.add('cv-lightbox-trigger');
    photo.tabIndex = 0;
    photo.setAttribute('role', 'button');
    photo.setAttribute('aria-label', `${labels.enlarge}${photo.alt ? `: ${photo.alt}` : ''}`);
    photo.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      openLightbox(index);
    });
    photo.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openLightbox(index);
      }
    });
  });

  closeButton.addEventListener('click', closeLightbox);
  lightbox.querySelector('.cv-lightbox-prev').addEventListener('click', () => step(-1));
  lightbox.querySelector('.cv-lightbox-next').addEventListener('click', () => step(1));
  lightbox.addEventListener('click', (event) => {
    if (!event.target.closest('.cv-lightbox-image, .cv-lightbox-close, .cv-lightbox-nav')) closeLightbox();
  });
  lightboxImage.addEventListener('touchstart', (event) => {
    const touch = event.changedTouches[0];
    touchStartX = touch.clientX;
    touchStartY = touch.clientY;
  }, { passive: true });
  lightboxImage.addEventListener('touchend', (event) => {
    const touch = event.changedTouches[0];
    const distanceX = touch.clientX - touchStartX;
    const distanceY = touch.clientY - touchStartY;
    if (Math.abs(distanceX) > 48 && Math.abs(distanceX) > Math.abs(distanceY)) {
      step(distanceX < 0 ? 1 : -1);
    }
  }, { passive: true });
  document.addEventListener('keydown', (event) => {
    if (lightbox.hidden) return;
    if (event.key === 'Escape') closeLightbox();
    if (event.key === 'ArrowLeft') step(-1);
    if (event.key === 'ArrowRight') step(1);
  });
}

// Cover Flow 3D: galleria fotografica con effetto prospettico (bagni, camere, sala giochi & bici)
const initializeCoverflow = (coverflowGallery) => {
  const slides = Array.from(coverflowGallery.querySelectorAll(':scope > .cv-photo'));
  if (!slides.length) return;

  const isItalian = document.documentElement.lang === 'it';
  const coverflowKind = coverflowGallery.dataset.coverflow;
  const hasGroups = slides.some((slide) => slide.dataset.coverflowGroup);
  let activeSlide = 0;
  let pointerStartX = 0;
  let pointerStartY = 0;
  let didSwipe = false;

  coverflowGallery.classList.add('cv-coverflow');
  coverflowGallery.tabIndex = 0;
  coverflowGallery.setAttribute('role', 'region');
  coverflowGallery.setAttribute('aria-roledescription', 'carousel');
  const ariaLabels = {
    bathrooms: ['Galleria fotografica del bagno', 'Bathroom photo gallery'],
    rooms: ['Galleria fotografica delle camere', 'Room photo gallery'],
    leisure: ['Galleria fotografica', 'Photo gallery'],
    home: ['Galleria fotografica di Vatican Glamorous', 'Vatican Glamorous photo gallery'],
  };
  const [labelIt, labelEn] = ariaLabels[coverflowKind] || ['Galleria fotografica dell’appartamento', 'Apartment photo gallery'];
  coverflowGallery.setAttribute('aria-label', isItalian ? labelIt : labelEn);

  slides.forEach((slide, index) => {
    slide.dataset.coverflowIndex = String(index);
    slide.querySelector('img')?.setAttribute('data-no-lightbox', '');
  });

  const controls = document.createElement('div');
  controls.className = 'cv-coverflow-controls';
  const groupKeys = [...new Set(slides.map((slide) => slide.dataset.coverflowGroup).filter(Boolean))];
  controls.innerHTML = `
    <div class="cv-coverflow-navigation">
    <button class="cv-coverflow-button cv-coverflow-previous" type="button" aria-label="${isItalian ? 'Foto precedente' : 'Previous photo'}">‹</button>
    <span class="cv-coverflow-status" aria-live="polite"></span>
    <button class="cv-coverflow-button cv-coverflow-next" type="button" aria-label="${isItalian ? 'Foto successiva' : 'Next photo'}">›</button>
    </div>`;
  coverflowGallery.after(controls);

  const status = controls.querySelector('.cv-coverflow-status');
  const groupButtons = Array.from(controls.querySelectorAll('.cv-coverflow-group'));
  const normalize = (index) => (index + slides.length) % slides.length;
  const shortestOffset = (index) => {
    let offset = index - activeSlide;
    if (offset > slides.length / 2) offset -= slides.length;
    if (offset < -slides.length / 2) offset += slides.length;
    return offset;
  };

  const renderCoverflow = () => {
    slides.forEach((slide, index) => {
      const offset = shortestOffset(index);
      const distance = Math.abs(offset);
      const visible = distance <= 2;
      slide.classList.toggle('is-previous-one', offset === -1);
      slide.classList.toggle('is-next-one', offset === 1);
      slide.classList.toggle('is-previous-two', offset === -2);
      slide.classList.toggle('is-next-two', offset === 2);
      slide.style.zIndex = String(20 - distance);
      slide.classList.toggle('is-active', offset === 0);
      slide.setAttribute('aria-hidden', visible ? 'false' : 'true');
      slide.tabIndex = visible ? 0 : -1;
      slide.style.pointerEvents = visible ? 'auto' : 'none';
    });
    const active = slides[activeSlide];
    if (hasGroups) {
      status.textContent = active.dataset.groupName || active.dataset.groupLabel || '';
    } else {
      status.textContent = `${isItalian ? 'Foto' : 'Photo'} ${activeSlide + 1}/${slides.length}`;
    }
  };

  const goTo = (index) => {
    activeSlide = normalize(index);
    renderCoverflow();
  };

  slides.forEach((slide, index) => {
    slide.addEventListener('click', (event) => {
      if (didSwipe) {
        event.preventDefault();
        didSwipe = false;
        return;
      }
      goTo(index);
    });
    slide.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        goTo(index);
      }
    });
  });
  controls.querySelector('.cv-coverflow-previous').addEventListener('click', () => goTo(activeSlide - 1));
  controls.querySelector('.cv-coverflow-next').addEventListener('click', () => goTo(activeSlide + 1));
  groupButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const targetIndex = slides.findIndex((slide) => slide.dataset.coverflowGroup === button.dataset.coverflowTarget);
      if (targetIndex >= 0) goTo(targetIndex);
    });
  });
  coverflowGallery.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') goTo(activeSlide - 1);
    if (event.key === 'ArrowRight') goTo(activeSlide + 1);
  });
  // Mouse / penna: eventi pointer
  coverflowGallery.addEventListener('pointerdown', (event) => {
    if (event.pointerType === 'touch') return;
    pointerStartX = event.clientX;
    pointerStartY = event.clientY;
  });
  coverflowGallery.addEventListener('pointerup', (event) => {
    if (event.pointerType === 'touch') return;
    const distanceX = event.clientX - pointerStartX;
    const distanceY = event.clientY - pointerStartY;
    if (Math.abs(distanceX) > 45 && Math.abs(distanceX) > Math.abs(distanceY)) {
      didSwipe = true;
      goTo(activeSlide + (distanceX < 0 ? 1 : -1));
    }
  });
  // Dito: eventi touch. A differenza dei pointer non vengono annullati quando il
  // browser inizia a scorrere la pagina (succede spesso col telefono in orizzontale).
  let touchX = 0, touchY = 0, touchLock = null;
  coverflowGallery.addEventListener('touchstart', (event) => {
    const t = event.touches[0];
    touchX = t.clientX; touchY = t.clientY; touchLock = null;
  }, { passive: true });
  coverflowGallery.addEventListener('touchmove', (event) => {
    const t = event.touches[0];
    const dx = t.clientX - touchX, dy = t.clientY - touchY;
    if (touchLock === null && (Math.abs(dx) > 8 || Math.abs(dy) > 8)) {
      touchLock = Math.abs(dx) > Math.abs(dy) * 0.7 ? 'x' : 'y';
    }
    if (touchLock === 'x' && event.cancelable) event.preventDefault();
  }, { passive: false });
  coverflowGallery.addEventListener('touchend', (event) => {
    const t = event.changedTouches[0];
    const dx = t.clientX - touchX, dy = t.clientY - touchY;
    if (touchLock === 'x' && Math.abs(dx) > 30) {
      didSwipe = true;
      goTo(activeSlide + (dx < 0 ? 1 : -1));
    }
    touchLock = null;
  });

  renderCoverflow();
};

document.querySelectorAll('.cv-villa-gallery, [data-coverflow="bathrooms"], [data-coverflow="rooms"], [data-coverflow="leisure"], [data-coverflow="features"], [data-coverflow="home"]').forEach(initializeCoverflow);

// Collegamento tra la mini-gallery sotto il Cover Flow e i pulsanti di gruppo del Cover Flow stesso
document.querySelectorAll('[data-jump-to-group]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.jumpToGroup;
    const groupBtn = document.querySelector(`.cv-coverflow-group[data-coverflow-target="${target}"]`);
    if (groupBtn) {
      groupBtn.click();
      document.querySelector('.cv-coverflow[data-coverflow="rooms"]')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });
});

// Overlay dei codici foto (H1, A2, C3...) — TEMPORANEO: visibile sempre durante la revisione.
// Per nasconderli di nuovo (visibili solo con ?codici=1) impostare SHOW_PHOTO_CODES = false.
const SHOW_PHOTO_CODES = false;
if (SHOW_PHOTO_CODES || new URLSearchParams(location.search).has('codici')) {
  document.querySelectorAll('[data-photo-code]').forEach((el) => {
    const host = el.tagName === 'IMG' ? el.parentElement : el;
    if (!host || host.querySelector(':scope > .cv-photocode-badge')) return;
    if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
    const badge = document.createElement('span');
    badge.className = 'cv-photocode-badge';
    badge.textContent = el.dataset.photoCode;
    host.appendChild(badge);
  });
}

// Indicatore di scorrimento (principio generale): su qualsiasi fascia che scorre di lato
// compare a destra una freccia che invita a scorrere; sparisce quando si arriva in fondo.
(() => {
  const isScroller = (el) => {
    if (el.closest('[data-coverflow], .cv-coverflow')) return false;
    const ox = getComputedStyle(el).overflowX;
    return (ox === 'auto' || ox === 'scroll') && el.scrollWidth > el.clientWidth + 8;
  };
  const setup = () => {
    document.querySelectorAll('main *, .cv-benefits *').forEach((el) => {
      if (el.dataset.scrollHint === 'done' || el.classList.contains('vg-scroll-wrap')) return;
      if (!isScroller(el)) return;
      el.dataset.scrollHint = 'done';
      const wrap = document.createElement('div');
      wrap.className = 'vg-scroll-wrap';
      el.parentNode.insertBefore(wrap, el);
      wrap.appendChild(el);
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'vg-scroll-hint';
      btn.setAttribute('aria-label', document.documentElement.lang === 'it' ? 'Scorri a destra' : 'Scroll right');
      btn.innerHTML = '<span aria-hidden="true">›</span>';
      wrap.appendChild(btn);
      let bgEl = wrap, bg = 'rgb(255, 255, 255)';
      while (bgEl && bgEl !== document.documentElement) {
        const c = getComputedStyle(bgEl).backgroundColor;
        if (c && c !== 'transparent' && !/rgba\(.*,\s*0\)$/.test(c)) { bg = c; break; }
        bgEl = bgEl.parentElement;
      }
      wrap.style.setProperty('--vg-hint-bg', bg);
      const update = () => {
        const more = el.scrollLeft + el.clientWidth < el.scrollWidth - 8 && el.scrollWidth > el.clientWidth + 8;
        wrap.classList.toggle('has-more', more);
      };
      btn.addEventListener('click', () => el.scrollBy({ left: el.clientWidth * 0.8, behavior: 'smooth' }));
      el.addEventListener('scroll', update, { passive: true });
      window.addEventListener('resize', update);
      update();
    });
  };
  const run = () => requestAnimationFrame(setup);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
  let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(setup, 200); });
})();

// Hero Home: "Passeggiata del Gelsomino" bianca, allargata esattamente quanto la parola GLAMOROUS
(() => {
  const fit = () => {
    const glam = document.querySelector('.cv-title .vg-glam');
    const sub = document.querySelector('.vg-hero-sub');
    if (!glam || !sub) return;
    sub.style.letterSpacing = '0px';
    sub.style.marginRight = '0px';
    sub.style.display = 'inline-block';
    const target = glam.getBoundingClientRect().width;
    const natural = sub.getBoundingClientRect().width;
    const n = [...sub.textContent].length;
    if (n < 2 || target <= natural) return;
    const ls = (target - natural) / (n - 1);
    sub.style.letterSpacing = ls + 'px';
    sub.style.marginRight = -ls + 'px';
    const off = glam.getBoundingClientRect().left - sub.parentElement.getBoundingClientRect().left;
    sub.style.marginLeft = Math.max(0, off) + 'px';
  };
  const run = () => requestAnimationFrame(fit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(run);
  window.addEventListener('load', run);
  window.addEventListener('resize', run);
  run();
})();

// Calendario date del riquadro di prenotazione (Home e pagina Prenota, IT/EN).
// Sostituisce il selettore nativo del browser: i campi checkin/checkout restano nascosti
// con valore ISO YYYY-MM-DD; si usano solo date locali (nessuna conversione UTC).
(() => {
  const forms = [...document.querySelectorAll('[data-booking-form], [data-direct-book]')]
    .filter((form) => form.querySelector('[data-vg-date-btn]'));
  if (!forms.length) return;

  const TXT = {
    it: {
      months: ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'],
      days: ['Lu', 'Ma', 'Me', 'Gi', 'Ve', 'Sa', 'Do'],
      placeholder: 'gg/mm/aaaa', pickIn: 'Scegli la data di arrivo', pickOut: 'Scegli la data di partenza',
      night: 'notte', nights: 'notti', min: (n) => `Soggiorno minimo: ${n} notti`,
      clear: 'Cancella date', close: 'Chiudi', prev: 'Mese precedente', next: 'Mese successivo', dialog: 'Calendario date'
    },
    en: {
      months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      days: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
      placeholder: 'dd/mm/yyyy', pickIn: 'Select check-in date', pickOut: 'Select check-out date',
      night: 'night', nights: 'nights', min: (n) => `Minimum stay: ${n} nights`,
      clear: 'Clear dates', close: 'Close', prev: 'Previous month', next: 'Next month', dialog: 'Date picker'
    }
  };

  const pad = (n) => String(n).padStart(2, '0');
  const toIso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const fromIso = (s) => {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || '');
    if (!m) return null;
    const d = new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
    return d.getMonth() === Number(m[2]) - 1 ? d : null;
  };
  const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
  const nightsBetween = (a, b) => Math.round((Date.UTC(b.getFullYear(), b.getMonth(), b.getDate()) - Date.UTC(a.getFullYear(), a.getMonth(), a.getDate())) / 86400000);
  const today = () => { const n = new Date(); return new Date(n.getFullYear(), n.getMonth(), n.getDate()); };
  const show = (d) => `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()}`;
  const isWide = () => window.matchMedia('(min-width: 720px)').matches;

  let active = null; // { form, t, minNights, inField, outField, inBtn, outBtn, mode, view, hover }
  let pop = null;
  let lastWheel = 0;

  const get = (state, which) => fromIso((which === 'in' ? state.inField : state.outField).value);

  const setField = (field, date) => {
    const value = date ? toIso(date) : '';
    if (field.value === value) return;
    field.value = value;
    field.dispatchEvent(new Event('input', { bubbles: true }));
    field.dispatchEvent(new Event('change', { bubbles: true }));
  };

  const paintButtons = (state) => {
    [['in', state.inBtn], ['out', state.outBtn]].forEach(([which, btn]) => {
      const d = get(state, which);
      const span = btn.querySelector('span') || btn;
      span.textContent = d ? show(d) : state.t.placeholder;
      btn.classList.toggle('has-value', Boolean(d));
      btn.classList.toggle('is-active', Boolean(pop) && active === state && state.mode === which);
    });
  };

  const close = () => {
    if (!pop) return;
    const state = active;
    pop.remove(); pop = null;
    active = null;
    if (state) paintButtons(state);
  };

  const position = () => {
    if (!pop || !active) return;
    const r = active.inBtn.getBoundingClientRect();
    const w = pop.offsetWidth, h = pop.offsetHeight;
    const vw = document.documentElement.clientWidth, vh = window.innerHeight;
    let left = isWide() ? Math.min(Math.max(12, r.left), vw - w - 12) : Math.max(8, (vw - w) / 2);
    let top = r.bottom + 8;
    if (top + h > vh - 12) top = Math.max(12, r.top - h - 8);
    if (top + h > vh - 12) top = Math.max(12, vh - h - 12);
    top = Math.max(8, top);
    pop.style.left = `${Math.round(left)}px`;
    pop.style.top = `${Math.round(top)}px`;
  };

  const monthHtml = (state, y, m) => {
    const t = state.t;
    const first = new Date(y, m, 1);
    const lead = (first.getDay() + 6) % 7;
    const count = new Date(y, m + 1, 0).getDate();
    const min = today();
    const cin = get(state, 'in');
    let cells = '';
    for (let i = 0; i < lead; i += 1) cells += '<span class="vg-cal-empty"></span>';
    for (let day = 1; day <= count; day += 1) {
      const d = new Date(y, m, day);
      let disabled = d < min;
      if (!disabled && state.mode === 'out' && cin && d > cin && nightsBetween(cin, d) < state.minNights) disabled = true;
      const cls = ['vg-cal-day'];
      if (+d === +min) cls.push('is-today');
      cells += `<button type="button" class="${cls.join(' ')}" data-date="${toIso(d)}"${disabled ? ' disabled' : ''}>${day}</button>`;
    }
    return `<div class="vg-cal-month"><p class="vg-cal-title">${t.months[m]} ${y}</p><div class="vg-cal-week">${t.days.map((d) => `<span>${d}</span>`).join('')}</div><div class="vg-cal-grid">${cells}</div></div>`;
  };

  const render = () => {
    if (!pop || !active) return;
    const state = active;
    const t = state.t;
    const months = isWide() ? 2 : 1;
    const v = state.view;
    let html = '';
    for (let i = 0; i < months; i += 1) {
      const d = new Date(v.getFullYear(), v.getMonth() + i, 1);
      html += monthHtml(state, d.getFullYear(), d.getMonth());
    }
    const now = today();
    const atStart = v.getFullYear() === now.getFullYear() && v.getMonth() === now.getMonth();
    pop.innerHTML = `<div class="vg-cal-head"><button type="button" class="vg-cal-nav" data-cal-prev aria-label="${t.prev}"${atStart ? ' disabled' : ''}>‹</button><button type="button" class="vg-cal-nav" data-cal-next aria-label="${t.next}">›</button></div><div class="vg-cal-months">${html}</div><div class="vg-cal-foot"><p class="vg-cal-status"></p><div class="vg-cal-actions"><button type="button" class="vg-cal-link" data-cal-clear>${t.clear}</button><button type="button" class="vg-cal-close" data-cal-close>${t.close}</button></div></div>`;
    paint();
    position();
  };

  // evidenzia arrivo, partenza e intervallo (anche al passaggio del mouse) senza ridisegnare
  const paint = () => {
    if (!pop || !active) return;
    const state = active;
    const t = state.t;
    const cin = get(state, 'in');
    const hover = state.mode === 'out' && cin && state.hover && state.hover > cin ? state.hover : null;
    const end = state.mode === 'out' && hover ? hover : get(state, 'out');
    pop.querySelectorAll('.vg-cal-day').forEach((btn) => {
      const d = fromIso(btn.dataset.date);
      btn.classList.toggle('is-single', Boolean(cin && !end && +d === +cin));
      btn.classList.toggle('is-start', Boolean(cin && end && +d === +cin));
      btn.classList.toggle('is-end', Boolean(cin && end && +d === +end));
      btn.classList.toggle('is-range', Boolean(cin && end && d > cin && d < end));
    });
    const n = cin && end ? nightsBetween(cin, end) : 0;
    const status = n ? `${n} ${n === 1 ? t.night : t.nights}` : (state.mode === 'out' && cin ? `${t.pickOut} · ${t.min(state.minNights)}` : t.pickIn);
    const el = pop.querySelector('.vg-cal-status');
    if (el) el.textContent = status;
  };

  const shiftMonth = (delta) => {
    if (!active) return;
    const v = active.view;
    const next = new Date(v.getFullYear(), v.getMonth() + delta, 1);
    const now = today();
    if (next < new Date(now.getFullYear(), now.getMonth(), 1)) return;
    active.view = next;
    render();
  };

  const open = (state, mode) => {
    if (pop && active === state) { state.mode = mode; render(); paintButtons(state); return; }
    close();
    active = state;
    state.mode = mode === 'out' && !get(state, 'in') ? 'in' : mode;
    state.hover = null;
    const base = get(state, 'in') || today();
    state.view = new Date(base.getFullYear(), base.getMonth(), 1);
    if (!isWide()) {
      // su telefono porta i campi data in alto, così la scheda si apre subito sotto senza coprire tutto
      const top = state.inBtn.getBoundingClientRect().top;
      const header = document.querySelector('[data-header]');
      const offset = Math.max(0, header ? header.getBoundingClientRect().bottom : 0) + 36;
      if (Math.abs(top - offset) > 4) window.scrollBy({ top: top - offset, left: 0, behavior: 'instant' });
    }
    pop = document.createElement('div');
    pop.className = 'vg-cal';
    pop.setAttribute('role', 'dialog');
    pop.setAttribute('aria-label', state.t.dialog);
    document.body.appendChild(pop);
    pop.addEventListener('click', onPopClick);
    pop.addEventListener('pointerover', onPopHover);
    pop.addEventListener('mouseleave', () => { if (active && active.hover) { active.hover = null; paint(); } });
    pop.addEventListener('wheel', onWheel, { passive: false });
    render();
    paintButtons(state);
  };

  function onWheel(e) {
    if (!active) return;
    e.preventDefault();
    const delta = Math.abs(e.deltaY) >= Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
    if (!delta) return;
    const now = Date.now();
    if (now - lastWheel < 280) return;
    lastWheel = now;
    shiftMonth(delta > 0 ? 1 : -1);
  }

  function onPopHover(e) {
    if (e.pointerType && e.pointerType !== 'mouse') return;
    const btn = e.target.closest('.vg-cal-day');
    if (!active || active.mode !== 'out' || !btn || btn.disabled) return;
    const d = fromIso(btn.dataset.date);
    if (active.hover && +active.hover === +d) return;
    active.hover = d;
    paint();
  }

  function onPopClick(e) {
    e.stopPropagation();
    if (!active) return;
    const state = active;
    if (e.target.closest('[data-cal-prev]')) return shiftMonth(-1);
    if (e.target.closest('[data-cal-next]')) return shiftMonth(1);
    if (e.target.closest('[data-cal-close]')) return close();
    if (e.target.closest('[data-cal-clear]')) {
      setField(state.inField, null); setField(state.outField, null);
      state.mode = 'in'; state.hover = null; render(); paintButtons(state); return;
    }
    const btn = e.target.closest('.vg-cal-day');
    if (!btn || btn.disabled) return;
    const d = fromIso(btn.dataset.date);
    const cin = get(state, 'in');
    if (state.mode === 'in' || !cin || d <= cin) {
      setField(state.inField, d);
      const cout = get(state, 'out');
      if (cout && nightsBetween(d, cout) < state.minNights) setField(state.outField, null);
      state.mode = 'out'; state.hover = null;
      render(); paintButtons(state);
      return;
    }
    setField(state.outField, d);
    state.hover = null;
    paintButtons(state);
    render();
    close();
  }

  forms.forEach((form) => {
    const lang = (form.dataset.locale || document.documentElement.lang || 'it').slice(0, 2) === 'it' ? 'it' : 'en';
    const state = {
      form,
      t: TXT[lang],
      minNights: Number(form.dataset.minNights) || 2,
      inField: form.querySelector('[data-vg-date="in"]'),
      outField: form.querySelector('[data-vg-date="out"]'),
      inBtn: form.querySelector('[data-vg-date-btn="in"]'),
      outBtn: form.querySelector('[data-vg-date-btn="out"]'),
    };
    if (!state.inField || !state.outField || !state.inBtn || !state.outBtn) return;
    // date ricevute dall'URL (pagina Prenota): valide solo se future e nell'ordine giusto
    const cin = get(state, 'in');
    const cout = get(state, 'out');
    if (!cin || cin < today()) { state.inField.value = ''; state.outField.value = ''; }
    else if (!cout || nightsBetween(cin, cout) < state.minNights) state.outField.value = '';
    state.inBtn.addEventListener('click', (e) => { e.stopPropagation(); open(state, 'in'); });
    state.outBtn.addEventListener('click', (e) => { e.stopPropagation(); open(state, 'out'); });
    form.vgCalendar = state;
    paintButtons(state);
  });

  // "Cerca" senza date: apre il calendario invece di inviare (prima degli altri gestori di invio)
  window.addEventListener('submit', (e) => {
    const state = e.target && e.target.vgCalendar;
    if (!state) return;
    const cin = get(state, 'in');
    const cout = get(state, 'out');
    if (cin && cout) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    open(state, cin ? 'out' : 'in');
  }, true);

  document.addEventListener('click', (e) => {
    if (!pop) return;
    if (pop.contains(e.target) || e.target.closest('[data-vg-date-btn]')) return;
    close();
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && pop) { const s = active; close(); s?.inBtn.focus(); } });
  window.addEventListener('resize', () => { if (pop) render(); });
  window.addEventListener('scroll', () => { if (pop) position(); }, { passive: true });
})();
