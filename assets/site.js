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
  const label = isItalian ? 'Infanti' : 'Infants';
  const age = isItalian ? 'meno di 2 anni' : 'under 2';
  wrapper.className = form.matches('[data-direct-book]') ? '' : 'cv-field';
  wrapper.innerHTML = `<label for="${id}">${label}<small>${age}</small></label><select id="${id}" name="infants"><option selected>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select>`;
  grid.appendChild(wrapper);
  const childrenLabel = form.querySelector('label[for*="children"], label[for*="bambini"]');
  if (childrenLabel && !childrenLabel.querySelector('small')) {
    childrenLabel.insertAdjacentHTML('beforeend', `<small>${isItalian ? '2–12 anni' : 'ages 2–12'}</small>`);
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

  const openLightbox = (index) => {
    window.clearTimeout(hideTimer);
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
  lightbox.querySelector('.cv-lightbox-prev').addEventListener('click', () => showPhoto(activeIndex - 1));
  lightbox.querySelector('.cv-lightbox-next').addEventListener('click', () => showPhoto(activeIndex + 1));
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
      showPhoto(activeIndex + (distanceX < 0 ? 1 : -1));
    }
  }, { passive: true });
  document.addEventListener('keydown', (event) => {
    if (lightbox.hidden) return;
    if (event.key === 'Escape') closeLightbox();
    if (event.key === 'ArrowLeft') showPhoto(activeIndex - 1);
    if (event.key === 'ArrowRight') showPhoto(activeIndex + 1);
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

// Overlay dei codici foto (H1, V2, C9...) — visibile solo con ?codici=1 nell'URL, per riferimento interno
if (new URLSearchParams(location.search).has('codici')) {
  document.querySelectorAll('img[data-photo-code]').forEach((img) => {
    const parent = img.parentElement;
    if (parent && getComputedStyle(parent).position === 'static') {
      parent.style.position = 'relative';
    }
    const badge = document.createElement('span');
    badge.className = 'cv-photocode-badge';
    badge.textContent = img.dataset.photoCode;
    parent.appendChild(badge);
  });
}
