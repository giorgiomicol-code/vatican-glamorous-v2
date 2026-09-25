# -*- coding: utf-8 -*-
"""Genera il sito Vatican Glamorous (IT + EN) con la stessa struttura del tema Elegance di Villa Brando.
Ogni pagina è definita UNA volta con i testi affiancati T('italiano', 'english'):
così le due lingue hanno sempre la stessa struttura e i Cover Flow nella stessa posizione."""
import os, json

OUT = 'site'
DOMAIN = 'https://www.vaticanglamorous.com'
PHONE, PHONE_TXT = '+393519768732', '+39 351 976 8732'
WA = 'https://wa.me/393519768732'
EMAIL = 'vaticanglamorous@gmail.com'
AIRBNB = 'https://www.airbnb.it/rooms/898313654338960679'
BOOKING = 'https://www.booking.com/Share-GWKzqP'
DIRECT = 'https://direct-book.com/properties/passeggiatadelgelsomino'
GUIDE = 'https://guide.vaticanglamorous.com'
MAPS = 'https://maps.google.com/?q=Via+San+Telesforo+Roma'
CIN = 'IT058091C2ZV2HSZ96'
YT = 'azY0RWKun1g'
V = '2'  # versione cache CSS/JS

LANG = 'it'
def T(it, en): return it if LANG == 'it' else en

PAGES = [  # chiave, slug it, slug en, voce di menu it, en
    ('home', '', '', 'Home', 'Home'),
    ('apt', 'appartamento', 'apartment', "L’appartamento", 'The apartment'),
    ('rooms', 'camere', 'rooms', 'Camere', 'Rooms'),
    ('rome', 'roma-vaticano', 'rome-vatican', 'Roma &amp; Vaticano', 'Rome &amp; Vatican'),
    ('gallery', 'gallery', 'gallery', 'Gallery', 'Gallery'),
    ('exp', 'esperienze', 'experiences', 'Esperienze', 'Experiences'),
    ('info', 'info', 'info', 'Info', 'Info'),
    ('book', 'prenota', 'book', 'Prenota', 'Book'),
    ('privacy', 'privacy', 'privacy', 'Privacy', 'Privacy'),
]
P = {p[0]: p for p in PAGES}

def slug(key, lang=None):
    lang = lang or LANG
    s = P[key][1 if lang == 'it' else 2]
    return f'{lang}/' + (s + '/' if s else '')

CUR = 'home'
def root():  # prefisso relativo verso la radice del sito
    return '../' if CUR == 'home' else '../../'
def link(key, lang=None): return root() + slug(key, lang)
def A(path): return root() + 'assets/' + path

def img(code, alt, cls='', lazy=True, extra=''):
    f = f'photos/{code[0]}{int(code[1:]):02d}.webp'
    c = f' class="{cls}"' if cls else ''
    l = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return f'<img{c} src="{A(f)}" alt="{alt}"{l} data-photo-code="{code}"{extra}>'

def ph(text_it='Foto in arrivo', text_en='Photo coming soon'):
    return f'<div class="vg-placeholder">{T(text_it, text_en)}</div>'

def fig(code, alt, cap=None, group=None):
    g = ''
    if group: g = f' data-coverflow-group="{group[0]}" data-group-label="{group[1]}" data-group-name="{group[2]}"'
    cap = alt if cap is None else cap
    fc = f'<figcaption class="cv-photo-caption">{cap}</figcaption>' if cap else ''
    return f'<figure class="cv-photo"{g}>{img(code, alt)}{fc}</figure>'

def coverflow(kind, figs, extra_cls=''):
    c = 'cv-photo-grid' + (' ' + extra_cls if extra_cls else '')
    return f'<div class="{c}" data-coverflow="{kind}">\n' + '\n'.join(figs) + '\n</div>'

def amen(items): return '<ul class="cv-amenities">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

# ---------------------------------------------------------------- HEAD / HEADER / FOOTER
def head(title, desc, image='H01'):
    url_it = DOMAIN + '/' + slug(CUR, 'it'); url_en = DOMAIN + '/' + slug(CUR, 'en')
    url = url_it if LANG == 'it' else url_en
    kw = T('Vatican Glamorous, Passeggiata del Gelsomino, casa vacanze vicino al Vaticano, appartamento vacanze San Pietro, affitto breve Roma Vaticano, loft Roma con parcheggio gratuito, alloggio Giubileo Roma',
           'Vatican Glamorous, Passeggiata del Gelsomino, holiday home near Vatican City, apartment near St. Peter’s Basilica, Rome short stay Vatican, loft in Rome with free parking, Rome accommodation near Vatican')
    ld = ''
    if CUR == 'home':
        ld = json.dumps({
            '@context': 'https://schema.org', '@type': 'VacationRental',
            'name': 'Vatican Glamorous', 'alternateName': 'Passeggiata del Gelsomino',
            'description': desc, 'url': url, 'image': f'{DOMAIN}/assets/photos/H01.webp',
            'telephone': PHONE, 'email': EMAIL,
            'address': {'@type': 'PostalAddress', 'streetAddress': 'Via San Telesforo', 'addressLocality': 'Roma', 'addressRegion': 'RM', 'addressCountry': 'IT'},
            'containsPlace': {'@type': 'Accommodation', 'occupancy': {'@type': 'QuantitativeValue', 'maxValue': 4}},
            'sameAs': [AIRBNB, BOOKING],
        }, ensure_ascii=False)
        ld = f'\n  <script type="application/ld+json">{ld}</script>'
    return f'''<!doctype html>
<html lang="{LANG}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{kw}">
  <meta name="application-name" content="Vatican Glamorous">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Vatican Glamorous · Passeggiata del Gelsomino">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{DOMAIN}/assets/photos/{image[0]}{int(image[1:]):02d}.webp">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="{T('it_IT', 'en_GB')}">
  <meta property="og:locale:alternate" content="{T('en_GB', 'it_IT')}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="it" href="{url_it}">
  <link rel="alternate" hreflang="en" href="{url_en}">
  <link rel="alternate" hreflang="x-default" href="{url_en}">
  <link rel="icon" href="{A('brand/favicon.png')}" type="image/png">
  <link rel="stylesheet" href="{A('canva.css')}?v={V}">
  <link rel="stylesheet" href="{A('elegance.css')}?v={V}">
  <link rel="stylesheet" href="{A('elegance-pages.css')}?v={V}">
  <link rel="stylesheet" href="{A('vg.css')}?v={V}">{ld}
</head>'''

def brand(cls='vg-brand'):
    return (f'<a class="{cls}" href="{link("home")}" aria-label="Vatican Glamorous, homepage">'
            f'<img src="{A("brand/emblem.png")}" alt="" data-no-lightbox>'
            f'<span class="vg-brand-text"><strong>Vatican Glamorous</strong><small>Passeggiata del Gelsomino</small></span></a>')

def header():
    menu = ['home', 'apt', 'rooms', 'rome', 'gallery', 'exp', 'info']
    nav = ''.join(f'<a{" class=\"active\"" if k == CUR else ""} href="{link(k)}">{P[k][3] if LANG == "it" else P[k][4]}</a>' for k in menu)
    other = 'en' if LANG == 'it' else 'it'
    lang = (f'<strong>IT</strong><span>/</span><a href="{link(CUR, "en")}">EN</a>' if LANG == 'it'
            else f'<a href="{link(CUR, "it")}">IT</a><span>/</span><strong>EN</strong>')
    return f'''<body class="elegance">
  <header class="cv-header" data-header>
    <div class="cv-wrap cv-nav">
      {brand()}
      <nav class="cv-links" data-menu aria-label="{T('Navigazione principale', 'Main navigation')}">{nav}</nav>
      <div class="cv-tools"><div class="cv-lang">{lang}</div><a class="cv-button" href="{link('book')}">{T('Prenota', 'Book')}</a><button class="cv-menu" type="button" data-menu-button aria-expanded="false" aria-label="{T('Apri il menu', 'Open menu')}"><span></span></button></div>
    </div>
  </header>
'''

def footer():
    return f'''  <footer class="cv-full-footer{' cv-home-footer' if CUR == 'home' else ''}" id="{T('contatti', 'contact')}"><div class="cv-wrap"><div class="cv-footer-grid">
    <div><div class="vg-footer-brand"><img src="{A('brand/emblem-light.png')}" alt="" data-no-lightbox><div><strong>Vatican Glamorous</strong><small>Passeggiata del Gelsomino</small></div></div><p>Via S. Telesforo, Roma<br>{T('A 200 m da San Pietro', '200 m from St. Peter’s')}</p></div>
    <div><h3>{T('Esplora', 'Explore')}</h3><a href="{link('apt')}">{T('L’appartamento', 'The apartment')}</a><a href="{link('rooms')}">{T('Camere', 'Rooms')}</a><a href="{link('rome')}">{T('Roma &amp; Vaticano', 'Rome &amp; Vatican')}</a><a href="{link('gallery')}">Gallery</a></div>
    <div><h3>{T('Contatti', 'Contact')}</h3><a href="tel:{PHONE}">{PHONE_TXT}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></div>
    <div><h3>{T('Informazioni', 'Information')}</h3><a href="{link('info')}">{T('Info e regole', 'Info &amp; house rules')}</a><a href="{MAPS}" target="_blank" rel="noopener">{T('Indicazioni', 'Directions')}</a><a href="{AIRBNB}" target="_blank" rel="noopener">{T('Prenota su Airbnb', 'Book on Airbnb')}</a><a href="{BOOKING}" target="_blank" rel="noopener">{T('Prenota su Booking.com', 'Book on Booking.com')}</a><a href="{link('privacy')}">Privacy</a></div>
  </div><div class="cv-legal">Vatican Glamorous · Passeggiata del Gelsomino · Via S. Telesforo, Roma · CIN {CIN}</div></div></footer>
  <div class="cv-mobile-bar"><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a><a href="{link('book')}">{T('Prenota il soggiorno', 'Book your stay')}</a></div>
  <script src="{A('site.js')}?v={V}" defer></script>
</body>
</html>
'''

def page_hero(code, alt, kicker, h1, text, style=''):
    st = f' style="{style}"' if style else ''
    return f'''<section class="cv-page-hero"><img src="{A(f'photos/{code[0]}{int(code[1:]):02d}.webp')}" alt="{alt}" data-photo-code="{code}"{st}><div class="cv-wrap"><p class="cv-page-kicker">{kicker}</p><h1>{h1}</h1><p>{text}</p></div></section>'''

def cta(h2, p, btn):
    pp = f'<p>{p}</p>' if p else ''
    return f'<section class="cv-cta-band"><div class="cv-wrap"><h2>{h2}</h2>{pp}<a class="cv-button" href="{link("book")}">{btn}</a></div></section>'

def centered(eyebrow, h2, extra=''):
    return f'<div class="cv-centered"><p class="cv-eyebrow">{eyebrow}</p><h2 class="cv-heading">{h2}</h2>{extra}</div>'

def select(name, id_, n, sel):
    return f'<select id="{id_}" name="{name}">' + ''.join(f'<option{" selected" if i == sel else ""}>{i}</option>' for i in range(0 if name != 'adults' else 1, n + 1)) + '</select>'

# ---------------------------------------------------------------- PAGINE
def home():
    title = T('Vatican Glamorous · Passeggiata del Gelsomino | Casa vacanze a 200 m da San Pietro',
              'Vatican Glamorous · Passeggiata del Gelsomino | Holiday home 200 m from St. Peter’s')
    desc = T('Vatican Glamorous (Passeggiata del Gelsomino): loft per 4 persone al 5° piano con ascensore, a 200 m da San Pietro, con posto auto gratuito e 2 balconi. Prenota direttamente.',
             'Vatican Glamorous (Passeggiata del Gelsomino): loft for 4 guests on the 5th floor with lift, 200 m from St. Peter’s, with free parking and 2 balconies. Book direct.')
    L = LANG
    teaser = [
        ('H10', T('Zona giorno in stile loft', 'Loft-style living area')),
        ('H11', T('Soggiorno con libreria e Smart TV', 'Living room with bookcase and Smart TV')),
        ('H12', T('Cucina attrezzata', 'Fully equipped kitchen')),
        ('H13', T('Camera con letto king-size', 'Bedroom with king-size bed')),
        ('H14', T('Letto pronto all’arrivo', 'Bed made up for your arrival')),
        ('H15', T('Divano letto queen-size', 'Queen-size sofa bed')),
        ('H16', T('Balcone con tavolo per la colazione', 'Balcony with breakfast table')),
        ('H17', T('Bagno completo', 'Full bathroom')),
        ('H18', T('Luce naturale in soggiorno', 'Natural light in the living room')),
        ('H19', T('Ingresso e corridoio', 'Entrance and hallway')),
        ('H20', T('Arte contemporanea alle pareti', 'Contemporary art on the walls')),
        ('H21', T('Cabina armadio', 'Walk-in closet')),
        ('H22', T('Camera con scrivania', 'Bedroom with desk')),
        ('H23', T('Dettagli della camera', 'Bedroom details')),
        ('H24', T('Vatican Glamorous in un colpo d’occhio', 'Vatican Glamorous at a glance')),
    ]
    cards = [
        ('apt', 'H2', T('L’appartamento', 'The apartment'), T('Loft, cucina e balconi', 'Loft, kitchen and balconies'), T('Zona giorno di Vatican Glamorous', 'Vatican Glamorous living area')),
        ('rooms', 'H3', T('Le camere', 'The rooms'), T('Fino a 4 ospiti', 'Up to 4 guests'), T('Camera con letto king-size', 'Bedroom with king-size bed')),
        ('rome', 'H4', T('Roma &amp; Vaticano', 'Rome &amp; Vatican'), T('San Pietro a 200 m', 'St. Peter’s 200 m away'), T('La cupola di San Pietro al tramonto', 'St. Peter’s dome at dusk')),
        ('gallery', 'H5', 'Gallery', T('Foto e video', 'Photos and video'), T('Corridoio e zona giorno', 'Hallway and living area')),
    ]
    benefits = [
        ('<svg viewBox="0 0 32 32"><path d="M4 15 16 5l12 10v12H9V15"/><path d="M13 27v-8h6v8"/></svg>', T('Fino a 4 ospiti', 'Up to 4 guests'), T('1 camera · divano letto · 1 bagno', '1 bedroom · sofa bed · 1 bathroom')),
        ('<svg viewBox="0 0 32 32"><path d="M16 29s9-9 9-17a9 9 0 1 0-18 0c0 8 9 17 9 17Z"/><circle cx="16" cy="12" r="3"/></svg>', T('A 200 m da San Pietro', '200 m from St. Peter’s'), T('Il Vaticano a piedi', 'Walk to the Vatican')),
        ('<svg viewBox="0 0 32 32"><rect x="5" y="5" width="22" height="22" rx="3"/><path d="M13 23V9h5a4 4 0 0 1 0 8h-5"/></svg>', T('Posto auto gratuito', 'Free parking'), T('Proprio sotto il palazzo', 'Right below the building')),
        ('<svg viewBox="0 0 32 32"><path d="M5 27h22M7 27V15h18v12M7 19h18M11 19v8M16 19v8M21 19v8"/><path d="M11 15V7h10v8"/></svg>', T('2 balconi', '2 balconies'), T('Colazione all’aperto', 'Breakfast outdoors')),
        ('<svg viewBox="0 0 32 32"><rect x="8" y="4" width="16" height="24" rx="2"/><path d="m12 12 4-4 4 4M12 20l4 4 4-4"/></svg>', T('5° piano con ascensore', '5th floor with lift'), T('Palazzo d’epoca', 'Period building')),
    ]
    b = ''.join(f'<div class="cv-benefit"><span class="cv-benefit-icon">{s}</span><span><strong>{t}</strong><span>{u}</span></span></div>' for s, t, u in benefits)
    cardhtml = '\n'.join(f'''      <a class="cv-card" href="{link(k)}" data-reveal><div class="cv-card-media">{img(c, alt, extra=' data-no-lightbox')}</div><div class="cv-card-bottom"><div><h3>{h}</h3><small>{s}</small></div><span class="cv-card-arrow">→</span></div></a>''' for k, c, h, s, alt in cards)
    dest = [
        (img('H6', T('San Pietro e il Tevere', 'St. Peter’s and the Tiber')), T('San Pietro', 'St. Peter’s')),
        (img('H7', T('Mappa: dall’appartamento al Vaticano in 2 minuti a piedi', 'Map: from the apartment to the Vatican in 2 minutes on foot')), T('Musei Vaticani', 'Vatican Museums')),
        (ph(), T('Castel Sant’Angelo', 'Castel Sant’Angelo')),
        (ph(), T('Piazza Navona', 'Piazza Navona')),
    ]
    desthtml = '\n'.join(f'      <article class="cv-destination" data-reveal><div class="cv-destination-image">{i}</div><h3>{h}</h3></article>' for i, h in dest)
    adults = select('adults', f'cv-adulti-{L}', 4, 2)
    kids = select('children', f'cv-bambini-{L}', 3, 0)
    return head(title, desc) + header() + f'''
  <main id="{T('inizio', 'top')}">
    <section class="cv-hero">
      <div class="cv-hero-bg">{img('H1', T('Zona giorno luminosa di Vatican Glamorous', 'Bright living area at Vatican Glamorous'), lazy=False)}</div>
      <div class="cv-wrap cv-hero-inner">
        <div class="cv-hero-copy" data-reveal><p class="cv-kicker">{T('Casa vacanze a Roma · zona Vaticano', 'Holiday home in Rome · Vatican area')}</p><h1 class="cv-title">Vatican Glamorous</h1><p class="cv-script">{T('Parcheggia l’auto ed entra in Vaticano a piedi', 'Park your car and walk into the Vatican')}</p><p class="cv-locations">{T('San Pietro · Musei Vaticani · Centro storico', 'St. Peter’s · Vatican Museums · Historic centre')}</p><a class="cv-button" href="{link('book')}">{T('Prenota direttamente', 'Book direct')}</a><p class="cv-unique"><b>★</b> {T('4.96 su Airbnb · 9.6 su Booking.com', '4.96 on Airbnb · 9.6 on Booking.com')}</p></div>
        <form class="cv-booking" data-booking-form data-booking-url="{link('book')}" data-locale="{L}" aria-label="{T('Ricerca disponibilità', 'Availability search')}" data-reveal><h2>{T('Trova la data perfetta', 'Find your perfect dates')}</h2><div class="cv-date-row"><div class="cv-field"><label for="cv-arrivo-{L}">{T('Arrivo', 'Check-in')}</label><input id="cv-arrivo-{L}" name="checkin" type="date" required></div><div class="cv-field"><label for="cv-partenza-{L}">{T('Partenza', 'Check-out')}</label><input id="cv-partenza-{L}" name="checkout" type="date" required></div><div class="cv-field"><label for="cv-adulti-{L}">{T('Adulti', 'Adults')}</label>{adults}</div><div class="cv-field"><label for="cv-bambini-{L}">{T('Bambini', 'Children')}</label>{kids}</div></div><button class="cv-button" type="submit">{T('Cerca', 'Search')}</button><p class="cv-note">{T('Date e numero di ospiti saranno già compilati nel motore ufficiale.', 'Dates and guests will be pre-filled in the official booking engine.')}</p><p class="cv-minimum">{T('Soggiorno minimo: 2 notti', 'Minimum stay: 2 nights')}</p><p class="cv-pet">🐾 {T('animali di piccola taglia ammessi', 'small pets welcome')}</p><div class="cv-hero-platforms"><span>{T('Prenota anche su', 'Also book on')}</span><div class="cv-platform-badges"><a href="{AIRBNB}" target="_blank" rel="noopener" aria-label="{T('Prenota su Airbnb', 'Book on Airbnb')}"><img src="{A('icons/airbnb.svg')}" alt="Airbnb" data-no-lightbox></a><a href="{BOOKING}" target="_blank" rel="noopener" aria-label="{T('Prenota su Booking.com', 'Book on Booking.com')}"><img src="{A('icons/booking.svg')}" alt="Booking.com" data-no-lightbox></a></div></div></form>
      </div>
    </section>

    <section class="cv-benefits" id="{T('informazioni', 'highlights')}"><div class="cv-wrap cv-benefit-grid">{b}</div></section>

    <section class="cv-about" id="{T('presentazione', 'about')}"><div class="cv-wrap"><div class="cv-centered" data-reveal><div class="vg-brand-large"><img src="{A('brand/emblem.png')}" alt="" data-no-lightbox><strong>Vatican Glamorous</strong><small>Passeggiata del Gelsomino</small></div><h2 class="cv-heading">{T('Un loft contemporaneo a due passi da San Pietro', 'A contemporary loft a stone’s throw from St. Peter’s')}</h2><p class="cv-script">{T('Spazi autentici.<br>Soggiorni indimenticabili.', 'Authentic spaces.<br>Unforgettable stays.')}</p></div>{coverflow('home', [fig(c, a) for c, a in teaser], 'cv-home-teaser')}<div class="cv-home-teaser-footer"><p class="cv-tagline-uses"><em>{T('Ideale per famiglie, amici, pellegrini, smart-working, set fotografici e riprese.', 'Ideal for families, friends, pilgrims, smart-working, photo shoots and filming.')}</em></p><p>{T('Vatican Glamorous è una casa vacanze ad uso esclusivo, rinnovata in stile loft contemporaneo, al quinto piano (con ascensore) di un tipico palazzo d’epoca a circa 200 metri dalla Basilica di San Pietro.', 'Vatican Glamorous is an exclusive-use holiday home, renovated in a contemporary loft style, on the fifth floor (with lift) of a typical period building about 200 metres from St. Peter’s Basilica.')}</p><p>{T('Accoglie fino a 4 persone: una camera con letto king-size, un comodo divano letto queen-size nella zona giorno, cucina completa, bagno e due balconi con tavolo per la colazione all’aperto. Il posto auto gratuito si trova proprio sotto il palazzo.', 'It sleeps up to 4: a bedroom with a king-size bed, a comfortable queen-size sofa bed in the living area, a full kitchen, a bathroom and two balconies with a table for breakfast outdoors. Free parking is right below the building.')}</p><a class="cv-button" href="{link('book')}">{T('Scopri la disponibilità', 'Check availability')}</a></div></div></section>

    <section class="cv-discover" id="{T('scopri', 'discover')}"><div class="cv-wrap"><div class="cv-centered" data-reveal><p class="cv-eyebrow">{T('Scopri', 'Discover')}</p><h2 class="cv-heading">{T('Stile, comfort e il Vaticano sotto casa.', 'Style, comfort and the Vatican on your doorstep.')}</h2></div><div class="cv-card-grid">
{cardhtml}
    </div></div></section>

    <section class="cv-ribbon"><div class="cv-wrap cv-ribbon-grid"><div class="cv-award" data-reveal><strong>{T('Le vostre splendide recensioni', 'Your wonderful reviews')}</strong><div class="vg-scores"><span>★ 4.96 Airbnb</span><span>9.6/10 Booking.com</span></div><span>Booking.com · Traveller Review Award 2026</span></div><div class="cv-film" data-reveal><p>{T('Cerchi una location per un servizio fotografico?<br>Contattaci per un’offerta dedicata.', 'Looking for a location for a photo shoot?<br>Contact us for a tailored offer.')}</p><a class="cv-button outline" href="{WA}" target="_blank" rel="noopener">{T('Scrivici', 'Contact us')}</a></div></div></section>

    <section class="cv-experiences" id="{T('esperienze', 'experiences')}"><div class="cv-wrap"><div class="cv-centered" data-reveal><p class="cv-eyebrow">{T('Esplora', 'Explore')}</p><h2 class="cv-heading">{T('Roma a piedi, dal Vaticano al centro', 'Rome on foot, from the Vatican to the centre')}</h2><p>{T('San Pietro a 6 minuti, Castel Sant’Angelo a 12, Piazza Navona a 15 e il Pantheon a 20: qui ogni meta si raggiunge a piedi.', 'St. Peter’s in 6 minutes, Castel Sant’Angelo in 12, Piazza Navona in 15 and the Pantheon in 20: here everything is within walking distance.')}</p></div><div class="cv-destination-row">
{desthtml}
    </div><p class="cv-ulisse-tagline">{T('Dormire all’ombra del Cupolone', 'Sleep in the shadow of the great dome')}</p><a class="cv-button outline" href="{link('rome')}">{T('Roma &amp; Vaticano', 'Rome &amp; Vatican')}</a>
    </div></section>
  </main>

''' + footer()

def apt():
    title = T('L’appartamento | Vatican Glamorous · Passeggiata del Gelsomino', 'The apartment | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Il loft di Vatican Glamorous: zona giorno contemporanea, cucina completa, 2 balconi, 5° piano con ascensore a 200 m da San Pietro.', 'The Vatican Glamorous loft: contemporary living area, full kitchen, 2 balconies, 5th floor with lift 200 m from St. Peter’s.')
    f = [
        fig('A3', T('Zona giorno in stile loft con poltrona e libreria', 'Loft-style living area with armchair and bookcase'), T('Zona giorno', 'Living area')),
        fig('A4', T('Corridoio con panca blu e vista sulla sala da pranzo', 'Hallway with blue bench and view of the dining area'), T('Ingresso', 'Entrance')),
        fig('A5', T('Soggiorno luminoso con porta-finestra sul balcone', 'Bright living room with French window to the balcony'), T('Soggiorno', 'Living room')),
        fig('A6', T('Tavolino in vetro con guida di benvenuto', 'Glass coffee table with welcome guide'), T('Benvenuti', 'Welcome')),
        fig('A7', T('Dettaglio del tavolino e della guida', 'Coffee table and guide detail'), T('Dettagli', 'Details')),
        fig('A8', T('Angolo TV con libreria', 'TV corner with bookcase'), T('Angolo TV', 'TV corner')),
        fig('A9', T('Panca imbottita e opera d’arte contemporanea', 'Upholstered bench and contemporary artwork'), T('Arte alle pareti', 'Art on the walls')),
        fig('A10', T('Cabina armadio con ripiani rossi', 'Walk-in closet with red shelves'), T('Cabina armadio', 'Walk-in closet')),
        fig('A11', T('Composizione fotografica dell’appartamento', 'Photo collage of the apartment'), 'Vatican Glamorous'),
    ]
    return head(title, desc, 'A01') + header() + f'''
  <main>
{page_hero('A1', T('Soggiorno con libreria e Smart TV', 'Living room with bookcase and Smart TV'), T('Stile contemporaneo · Luce · Comfort', 'Contemporary style · Light · Comfort'), T('L’appartamento', 'The apartment'), T('Un loft raffinato al quinto piano di un palazzo d’epoca, a due passi da San Pietro.', 'A refined loft on the fifth floor of a period building, a short walk from St. Peter’s.'))}
<section class="cv-section cream" id="{T('foto', 'photos')}"><div class="cv-wrap">{centered(T('Fotografie', 'Photos'), T('Uno sguardo all’appartamento', 'A look at the apartment'))}
{coverflow('features', f)}
</div></section>
<section class="cv-section cv-villa-intro" id="{T('presentazione', 'about')}"><div class="cv-wrap cv-editorial"><div class="cv-editorial-copy"><p class="cv-eyebrow left">Vatican Glamorous</p><h2 class="cv-script-title">{T('Un loft contemporaneo vicino al Vaticano', 'A contemporary loft near the Vatican')}</h2><p>{T('Casa vacanze ad uso esclusivo, rinnovata di recente con cura in stile loft contemporaneo, ideale per famiglie e amici fino a 4 persone.', 'An exclusive-use holiday home, recently and carefully renovated in a contemporary loft style, ideal for families and friends of up to 4.')}</p><p>{T('Il nome “Passeggiata del Gelsomino” richiama il vicino e suggestivo viale che conduce allo Stato della Città del Vaticano.', 'The name “Passeggiata del Gelsomino” (Jasmine Walk) recalls the nearby, evocative avenue that leads to Vatican City.')}</p><p>{T('Siamo così vicini al centro che preferirai raggiungere ogni meta a piedi.', 'We are so close to the centre that you will want to walk everywhere.')}</p><div class="cv-facts"><div class="cv-fact"><strong>4</strong><span>{T('ospiti', 'guests')}</span></div><div class="cv-fact"><strong>5°</strong><span>{T('piano', 'floor')}</span></div><div class="cv-fact"><strong>2</strong><span>{T('balconi', 'balconies')}</span></div></div></div><div class="cv-editorial-media">{img('A2', T('Zona giorno con divano, tappeto e opera d’arte', 'Living area with sofa, rug and artwork'))}</div></div></section>
<section class="cv-section cream cv-villa-living" id="{T('cucina', 'kitchen')}"><div class="cv-wrap"><h2 class="cv-living-title">{T('Zona giorno e cucina', 'Living area &amp; kitchen')}</h2><div class="cv-editorial reverse"><div class="cv-editorial-copy"><p class="cv-script">{T('Spazi autentici.<br>Soggiorni indimenticabili.', 'Authentic spaces.<br>Unforgettable stays.')}</p><p>{T('Un ampio soggiorno in stile loft con divano letto king-size e una cucina completa di tutti gli elettrodomestici.', 'A spacious loft-style living room with a king-size sofa bed and a kitchen complete with all appliances.')}</p>{amen([T('Cucina completa', 'Full kitchen'), T('Lavastoviglie', 'Dishwasher'), T('Lavasciuga', 'Washer-dryer'), 'Wi‑Fi', T('Smart Monitor con Netflix e app streaming', 'Smart monitors with Netflix and streaming apps'), 'Amazon Alexa', T('Aria condizionata automatica', 'Automatic air conditioning'), T('Scrivania per smart-working', 'Desk for smart-working')])}</div><div class="cv-editorial-media">{img('A12', T('Cucina attrezzata con elettrodomestici in acciaio', 'Equipped kitchen with stainless-steel appliances'))}</div></div></div></section>
<section class="cv-section" id="{T('balconi', 'balconies')}"><div class="cv-wrap"><div class="cv-centered"><p class="cv-eyebrow">{T('All’aperto', 'Outdoors')}</p><h2 class="cv-heading">{T('I due balconi', 'The two balconies')}</h2></div><div class="cv-editorial"><div class="cv-editorial-copy"><p class="cv-script">{T('Colazione all’aria aperta', 'Breakfast in the open air')}</p><p>{T('L’appartamento dispone di due balconi, uno attrezzato con tavolino e sedute per la colazione o un aperitivo al tramonto, con vista sui tetti del quartiere.', 'The apartment has two balconies, one set up with a small table and seating for breakfast or a sunset aperitivo, overlooking the neighbourhood rooftops.')}</p>{amen([T('Tavolo per la colazione', 'Breakfast table'), T('Sedute da esterno', 'Outdoor seating'), T('Luce naturale tutto il giorno', 'Natural light all day'), T('Affaccio sul quartiere', 'Views over the neighbourhood')])}</div><div class="cv-editorial-media">{img('A13', T('Balcone con tavolino, sedie e sgabelli', 'Balcony with small table, chairs and stools'))}</div></div></div></section>
<section class="cv-section cream" id="{T('caratteristiche', 'features')}"><div class="cv-wrap">{centered(T('Dettagli', 'Details'), T('Caratteristiche della casa', 'Property features'))}{amen([T('5° piano con ascensore', '5th floor with lift'), T('Palazzo d’epoca', 'Period building'), T('Posto auto gratuito sotto il palazzo', 'Free parking below the building'), T('1 camera matrimoniale king-size', '1 king-size double bedroom'), T('Divano letto queen-size', 'Queen-size sofa bed'), T('1 bagno completo', '1 full bathroom'), T('Cabina armadio', 'Walk-in closet'), T('2 balconi', '2 balconies'), T('Culla e passeggino', 'Cot and stroller'), T('Animali di piccola taglia ammessi', 'Small pets welcome'), T('Biancheria, asciugamani e kit bagno inclusi', 'Bed linen, towels and toiletries included'), T('Vietato fumare in casa', 'No smoking indoors')])}</div></section>
{cta(T('Vivi Vatican Glamorous', 'Stay at Vatican Glamorous'), T('Verifica le date nel motore di prenotazione ufficiale.', 'Check dates in the official booking engine.'), T('Scopri la disponibilità', 'Check availability'))}
  </main>

''' + footer()

def rooms():
    title = T('Camere | Vatican Glamorous · Passeggiata del Gelsomino', 'Rooms | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Camera con letto king-size, divano letto queen-size e bagno completo: Vatican Glamorous ospita fino a 4 persone vicino a San Pietro.', 'A king-size bedroom, a queen-size sofa bed and a full bathroom: Vatican Glamorous sleeps up to 4 near St. Peter’s.')
    g1 = ('C01', T('Camera', 'Bedroom'), T('Camera matrimoniale', 'Double bedroom'))
    g2 = ('C02', T('Soggiorno', 'Living room'), T('Divano letto', 'Sofa bed'))
    f = [
        fig('C2', T('Letto king-size con cuscini blu e asciugamani', 'King-size bed with blue cushions and towels'), g1[2], g1),
        fig('C3', T('Testiera capitonné verde petrolio', 'Teal tufted headboard'), g1[2], g1),
        fig('C4', T('Letto con opere d’arte alle pareti', 'Bed with artworks on the walls'), g1[2], g1),
        fig('C5', T('Dettaglio della testiera e dei cuscini', 'Headboard and cushions detail'), g1[2], g1),
        fig('C6', T('Camera con scrivania e finestra', 'Bedroom with desk and window'), g1[2], g1),
        fig('C7', T('Comodino con lampada e sveglia', 'Bedside table with lamp and clock'), g1[2], g1),
        fig('C8', T('Camera con pannelli in legno e luci calde', 'Bedroom with wood panelling and warm lights'), g1[2], g1),
        fig('C9', T('Divano letto preparato con asciugamani', 'Sofa bed made up with towels'), g2[2], g2),
        fig('C10', T('Divano letto sotto il quadro in stile Art Déco', 'Sofa bed below the Art Deco-style painting'), g2[2], g2),
        fig('C11', T('Dettaglio del divano letto', 'Sofa bed detail'), g2[2], g2),
        fig('C12', T('Zona giorno con divano letto', 'Living area with sofa bed'), g2[2], g2),
    ]
    bath = [fig(f'C{i}', a, T('Bagno', 'Bathroom')) for i, a in zip(range(13, 19), [
        T('Bagno con box doccia e sanitari sospesi', 'Bathroom with shower cubicle and wall-hung fixtures'),
        T('Lavabo e box doccia', 'Washbasin and shower'),
        T('Bagno con pavimento a scacchi', 'Bathroom with chequered floor'),
        T('Doccia e mobile contenitore', 'Shower and storage unit'),
        T('Doccia con porta-finestra', 'Shower and French window'),
        T('Vista dall’ingresso del bagno', 'View from the bathroom door')])]
    prev = f'''<div class="cv-room-preview-grid"><div class="cv-room-preview"><h3>{g1[2]}</h3><p>{T('Un’ampia camera con letto king-size, testiera imbottita e arredi contemporanei.', 'A spacious bedroom with a king-size bed, upholstered headboard and contemporary furnishings.')}</p><div class="cv-detail-list"><span>{T('Letto king-size', 'King-size bed')}</span><span>Smart Monitor</span><span>{T('Aria condizionata', 'Air conditioning')}</span></div></div><div class="cv-room-preview"><h3>{g2[2]}</h3><p>{T('Nella zona giorno, un comodo divano letto queen-size per altri due ospiti.', 'In the living area, a comfortable queen-size sofa bed for two more guests.')}</p><div class="cv-detail-list"><span>{T('Queen-size', 'Queen-size')}</span><span>Smart TV</span><span>{T('Aria condizionata', 'Air conditioning')}</span></div></div></div>'''
    return head(title, desc, 'C01') + header() + f'''
  <main>
{page_hero('C1', T('Camera con letto king-size', 'Bedroom with king-size bed'), T('Zona notte', 'Sleeping areas'), T('Le Camere', 'The Rooms'), T('Una camera con letto king-size e un divano letto queen-size: fino a 4 ospiti.', 'A king-size bedroom and a queen-size sofa bed: up to 4 guests.'))}
<section class="cv-section" id="{T('foto-camere', 'room-photos')}"><div class="cv-wrap">{centered(T('Zona notte', 'Sleeping areas'), T('Le Camere', 'The Rooms'))}
{coverflow('rooms', f)}
{prev}
</div></section>
<section class="cv-section cream" id="{T('dotazioni', 'amenities')}"><div class="cv-wrap">{centered('Comfort', T('Dotazioni della zona notte', 'Sleeping area amenities'))}{amen([T('1 letto king-size', '1 king-size bed'), T('1 divano letto queen-size', '1 queen-size sofa bed'), T('Culla', 'Cot'), T('Cabina armadio', 'Walk-in closet'), T('Scrivania', 'Desk'), T('Aria condizionata', 'Air conditioning'), T('Biancheria inclusa', 'Bed linen included'), T('Asciugamani e kit bagno', 'Towels and toiletries')])}</div></section>
<section class="cv-section" id="{T('bagno', 'bathroom')}"><div class="cv-wrap">{centered(T('Comfort e funzionalità', 'Comfort and practicality'), T('Il bagno', 'The bathroom'), '<p>' + T('Scorri le fotografie del bagno completo con doccia.', 'Browse the photos of the full bathroom with shower.') + '</p>')}
{coverflow('bathrooms', bath, 'cv-bathroom-coverflow')}
</div></section>
{cta(T('Il tuo riposo vicino a San Pietro', 'Rest easy near St. Peter’s'), '', T('Verifica le date', 'Check dates'))}
  </main>

''' + footer()

def rome():
    title = T('Roma &amp; Vaticano | Vatican Glamorous · Passeggiata del Gelsomino', 'Rome &amp; Vatican | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Dintorni di Vatican Glamorous: San Pietro a 200 m, Musei Vaticani, Castel Sant’Angelo e come muoversi a Roma.', 'Around Vatican Glamorous: St. Peter’s 200 m away, the Vatican Museums, Castel Sant’Angelo and getting around Rome.')
    walk = [(T('Vaticano', 'Vatican'), 6), ('Castel Sant’Angelo', 12), ('Piazza Navona', 15), ('Pantheon', 20),
            (T('Ospedale Bambino Gesù', 'Bambino Gesù Hospital'), 14), (T('Isola Tiberina (Fatebenefratelli)', 'Tiber Island (Fatebenefratelli)'), 20)]
    wl = '<ul class="vg-walk">' + ''.join(f'<li><span>{n}</span><b>{m} min {T("a piedi", "on foot")}</b></li>' for n, m in walk) + '</ul>'
    how = [
        (T('A piedi', 'On foot'), T('Il modo migliore per vivere il quartiere: San Pietro, Borgo e Castel Sant’Angelo sono a pochi minuti.', 'The best way to enjoy the area: St. Peter’s, Borgo and Castel Sant’Angelo are minutes away.')),
        (T('In treno', 'By train'), T('La stazione di Roma San Pietro è vicina ed è collegata con altre stazioni della città. [testo da verificare]', 'Roma San Pietro station is close by and connected to other city stations. [text to be checked]')),
        (T('In autobus e metro', 'By bus and metro'), T('Il quartiere è ben servito dagli autobus; la metropolitana collega il Vaticano al resto della città. [testo da verificare]', 'The area is well served by buses; the metro links the Vatican with the rest of the city. [text to be checked]')),
        (T('In auto', 'By car'), T('Posto auto gratuito proprio sotto il palazzo: lasci l’auto e ti muovi a piedi.', 'Free parking right below the building: leave the car and explore on foot.')),
        (T('Bici e monopattini', 'Bikes and scooters'), T('Biciclette e monopattini in sharing sono disponibili ovunque nei dintorni.', 'Shared bikes and scooters are available all around the area.')),
        (T('Verde e sport', 'Green spaces'), T('Il grande parco di Villa Pamphili è ideale per una corsa al mattino.', 'The large Villa Pamphili park is ideal for a morning run.')),
    ]
    hw = '<div class="cv-info-grid">' + ''.join(f'<article class="cv-info-card"><h3>{h}</h3><p>{p}</p></article>' for h, p in how) + '</div>'
    return head(title, desc, 'R01') + header() + f'''
  <main>
{page_hero('R1', T('San Pietro illuminato al tramonto visto dal Tevere', 'St. Peter’s lit up at dusk seen from the Tiber'), T('Dintorni · San Pietro · Musei Vaticani', 'Surroundings · St. Peter’s · Vatican Museums'), T('Roma &amp; Vaticano', 'Rome &amp; Vatican'), T('Tutte le bellezze di Roma sono a pochi passi: il Vaticano è a 5 minuti a piedi.', 'All the beauty of Rome is just steps away: the Vatican is a 5-minute walk.'))}
<section class="cv-section cream" id="{T('dintorni', 'surroundings')}"><div class="cv-wrap cv-editorial"><div class="cv-editorial-copy"><p class="cv-eyebrow left">{T('Dintorni', 'Surroundings')}</p><h2>{T('Una casa nel centro di Roma', 'A home in the centre of Rome')}</h2><p>{T('Il quartiere è servito da bar e ristoranti dove gustare la cucina italiana e romana, e da mezzi pubblici per raggiungere ogni angolo della città.', 'The area is full of bars and restaurants serving Italian and Roman cuisine, with public transport to every corner of the city.')}</p>{wl}</div><div class="cv-editorial-media">{img('R2', T('Mappa: Vaticano a 2 minuti a piedi dall’appartamento', 'Map: the Vatican 2 minutes on foot from the apartment'))}</div></div></section>
<section class="cv-section" id="{T('san-pietro', 'st-peters')}"><div class="cv-wrap cv-editorial reverse"><div class="cv-editorial-copy"><p class="cv-script">{T('All’ombra del Cupolone', 'In the shadow of the great dome')}</p><h2>{T('San Pietro', 'St. Peter’s')}</h2><p>{T('La Basilica e Piazza San Pietro sono a circa 200 metri: ideale per pellegrini, udienze e celebrazioni, con la tranquillità di tornare a casa in pochi minuti. [testo segnaposto]', 'The Basilica and St. Peter’s Square are about 200 metres away: ideal for pilgrims, audiences and celebrations, with the peace of being back home in minutes. [placeholder text]')}</p></div><div class="cv-editorial-media">{img('R3', T('Cupola di San Pietro illuminata', 'St. Peter’s dome illuminated'))}</div></div></section>
<section class="cv-section sky" id="{T('musei-vaticani', 'vatican-museums')}"><div class="cv-wrap cv-editorial"><div class="cv-editorial-copy"><p class="cv-eyebrow left">{T('Arte', 'Art')}</p><h2>{T('Musei Vaticani', 'Vatican Museums')}</h2><p>{T('Musei Vaticani e Cappella Sistina a pochi minuti a piedi. Consigliamo di prenotare in anticipo biglietti o visite guidate con ingresso prioritario. [testo segnaposto]', 'The Vatican Museums and Sistine Chapel are a few minutes’ walk away. We recommend booking tickets or guided tours with priority entry in advance. [placeholder text]')}</p><a class="cv-button" href="{link('exp')}">{T('Tour ed esperienze', 'Tours &amp; experiences')}</a></div><div class="cv-editorial-media">{ph()}</div></div></section>
<section class="cv-section cream" id="{T('come-muoversi', 'getting-around')}"><div class="cv-wrap">{centered(T('Mobilità', 'Getting around'), T('Come muoversi', 'How to get around'))}{hw}</div></section>
{cta(T('La tua base a Roma', 'Your base in Rome'), '', T('Verifica le date', 'Check dates'))}
  </main>

''' + footer()

def gallery():
    title = T('Gallery | Vatican Glamorous · Passeggiata del Gelsomino', 'Gallery | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Foto e video di Vatican Glamorous, loft vicino a San Pietro a Roma.', 'Photos and video of Vatican Glamorous, a loft near St. Peter’s in Rome.')
    caps = [T('Zona giorno', 'Living area'), T('Soggiorno', 'Living room'), T('Zona giorno', 'Living area'), T('Cucina', 'Kitchen'), T('Ingresso', 'Entrance'),
            T('Soggiorno', 'Living room'), T('Benvenuti', 'Welcome'), T('Dettagli', 'Details'), T('Angolo TV', 'TV corner'),
            T('Camera', 'Bedroom'), T('Camera', 'Bedroom'), T('Camera', 'Bedroom'), T('Camera', 'Bedroom'), T('Camera', 'Bedroom'), T('Camera', 'Bedroom'), T('Camera', 'Bedroom'),
            T('Divano letto', 'Sofa bed'), T('Divano letto', 'Sofa bed'), T('Divano letto', 'Sofa bed'), T('Arte alle pareti', 'Art on the walls'), T('Cabina armadio', 'Walk-in closet'), T('Balcone', 'Balcony'),
            T('Bagno', 'Bathroom'), T('Bagno', 'Bathroom'), T('Bagno', 'Bathroom'), T('Bagno', 'Bathroom'), T('Bagno', 'Bathroom'), T('Bagno', 'Bathroom'), 'Vatican Glamorous']
    f = [fig(f'G{i}', f'{c} · Vatican Glamorous', c) for i, c in enumerate(caps, 2)]
    return head(title, desc, 'G01') + header() + f'''
  <main>
{page_hero('G1', T('Zona giorno in stile loft', 'Loft-style living area'), T('Foto · Video', 'Photos · Video'), 'Gallery', T('Tutti gli ambienti di Vatican Glamorous in un’unica galleria.', 'Every space at Vatican Glamorous in a single gallery.'))}
<section class="cv-section sky" id="{T('foto', 'photos')}"><div class="cv-wrap">{centered(T('Fotografie', 'Photos'), T('L’appartamento in immagini', 'The apartment in pictures'), '<p>' + T('Scorri le fotografie di tutti gli ambienti.', 'Browse photos of every room.') + '</p>')}
{coverflow('leisure', f)}
</div></section>
<section class="cv-section cream" id="video"><div class="cv-wrap">{centered(T('Filmato originale', 'Original footage'), T('Vatican Glamorous in video', 'Vatican Glamorous on video'))}<div class="cv-video-grid"><div class="cv-video-embed"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{YT}" title="Video Vatican Glamorous" allowfullscreen></iframe></div></div></div></section>
{cta(T('Ti immagini già qui?', 'Can you picture yourself here?'), '', T('Prenota direttamente', 'Book direct'))}
  </main>

''' + footer()

def exp():
    title = T('Esperienze | Vatican Glamorous · Passeggiata del Gelsomino', 'Experiences | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Tour, visite ed esperienze a Roma e in Vaticano per gli ospiti di Vatican Glamorous.', 'Tours, visits and experiences in Rome and the Vatican for Vatican Glamorous guests.')
    cards = [
        (img('E2', T('Cupola di San Pietro', 'St. Peter’s dome')), T('San Pietro', 'St. Peter’s'), T('Basilica e cupola', 'Basilica and dome')),
        (ph(), T('Musei Vaticani', 'Vatican Museums'), T('Cappella Sistina', 'Sistine Chapel')),
        (ph(), T('Roma antica', 'Ancient Rome'), T('Colosseo e Fori', 'Colosseum and Forums')),
        (ph(), 'Trastevere', T('Sapori romani', 'Roman flavours')),
    ]
    ch = ''.join(f'<article class="cv-card"><div class="cv-card-media">{i}</div><div class="cv-card-bottom"><div><h3>{h}</h3><small>{s}</small></div></div></article>' for i, h, s in cards)
    return head(title, desc, 'E01') + header() + f'''
  <main>
{page_hero('E1', T('San Pietro al tramonto', 'St. Peter’s at dusk'), T('Vaticano · Roma · Esperienze', 'Vatican · Rome · Experiences'), T('Esperienze', 'Experiences'), T('Pagina in preparazione: qui arriveranno le pagine della guida ospiti di Vatican Glamorous. [testo segnaposto]', 'Page in progress: the Vatican Glamorous guest guide pages will be added here. [placeholder text]'))}
<section class="cv-section"><div class="cv-wrap"><div class="cv-centered"><p class="cv-eyebrow">{T('Dintorni', 'Surroundings')}</p><h2 class="cv-heading">{T('Roma da vivere', 'Rome to experience')}</h2><p class="cv-script">{T('Il Vaticano sotto casa.', 'The Vatican on your doorstep.')}</p><p>{T('Visite guidate, ingressi prioritari ed esperienze scelte per i nostri ospiti. [testo segnaposto]', 'Guided visits, priority entry and experiences chosen for our guests. [placeholder text]')}</p></div><div class="cv-card-grid">{ch}</div></div></section>
<section class="cv-section sky"><div class="cv-wrap cv-editorial reverse"><div class="cv-editorial-copy"><p class="cv-script">{T('Una guida da portare con te', 'A guide to take with you')}</p><h2>{T('Guida ospiti', 'Guest guide')}</h2><p>{T('Consulta la guida di Vatican Glamorous con consigli sul quartiere, trasporti e attrazioni. [testo segnaposto]', 'Browse the Vatican Glamorous guide with tips on the area, transport and sights. [placeholder text]')}</p><a class="cv-button" href="{GUIDE}" target="_blank" rel="noopener">{T('Apri la guida', 'Open the guide')}</a></div><div class="cv-editorial-media">{ph()}</div></div></section>
{cta(T('La tua base in Vaticano', 'Your base at the Vatican'), '', T('Verifica le date', 'Check dates'))}
  </main>

''' + footer()

def info():
    title = T('Info e regole | Vatican Glamorous · Passeggiata del Gelsomino', 'Info &amp; house rules | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Contatti, regole della casa e informazioni utili per il soggiorno a Vatican Glamorous, Via S. Telesforo, Roma.', 'Contacts, house rules and useful information for your stay at Vatican Glamorous, Via S. Telesforo, Rome.')
    return head(title, desc, 'A05') + header() + f'''
  <main>
{page_hero('A5', T('Soggiorno luminoso di Vatican Glamorous', 'Bright living room at Vatican Glamorous'), T('Contatti · Regole · Collegamenti utili', 'Contacts · Rules · Useful links'), T('Informazioni', 'Information'), T('Tutto ciò che serve prima dell’arrivo e durante il soggiorno.', 'Everything you need before arrival and during your stay.'))}
<section class="cv-section cream"><div class="cv-wrap">{centered('Vatican Glamorous', T('Contatti e risorse', 'Contacts and resources'))}<div class="cv-info-grid">
<article class="cv-info-card"><h3>{T('Contatti', 'Contact')}</h3><p>Via S. Telesforo, Roma</p><a href="tel:{PHONE}">{PHONE_TXT}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WA}" target="_blank" rel="noopener">{T('Scrivi su WhatsApp', 'Message us on WhatsApp')}</a><a href="{MAPS}" target="_blank" rel="noopener">{T('Apri le indicazioni', 'Get directions')}</a></article>
<article class="cv-info-card"><h3>{T('Documenti', 'Documents')}</h3><a href="{GUIDE}" target="_blank" rel="noopener">{T('Guida ospiti', 'Guest guide')}</a><p>Vatican Glamorous · Passeggiata del Gelsomino<br>CIN {CIN}</p></article>
<article class="cv-info-card"><h3>{T('Informazioni essenziali', 'Essentials')}</h3><ul><li>{T('Soggiorno minimo: 2 notti', 'Minimum stay: 2 nights')}</li><li>{T('Fino a 4 ospiti', 'Up to 4 guests')}</li><li>{T('Indica il numero esatto di adulti e bambini al momento della prenotazione', 'Please state the exact number of adults and children when booking')}</li><li>{T('Animali di piccola taglia ammessi', 'Small pets welcome')}</li><li>{T('Vietato fumare all’interno', 'No smoking indoors')}</li><li>{T('Orari di check-in e check-out: [da completare]', 'Check-in and check-out times: [to be completed]')}</li></ul></article>
<article class="cv-info-card"><h3>{T('Servizi e soggiorno', 'Services')}</h3><ul><li>{T('Biancheria, asciugamani e kit bagno inclusi', 'Bed linen, towels and toiletries included')}</li><li>{T('Posto auto gratuito', 'Free parking')}</li><li>Wi‑Fi</li><li>{T('Smart Monitor e app streaming', 'Smart monitors and streaming apps')}</li><li>{T('Aria condizionata', 'Air conditioning')}</li><li>{T('Lavastoviglie e lavasciuga', 'Dishwasher and washer-dryer')}</li></ul></article>
<article class="cv-info-card"><h3>{T('Servizi fotografici', 'Photo shoots')}</h3><p>{T('Per set fotografici, riprese e soggiorni di lavoro contattaci per un’offerta personalizzata.', 'For photo shoots, filming and business stays, contact us for a tailored offer.')}</p><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></article>
<article class="cv-info-card"><h3>{T('Prenotazione diretta', 'Direct booking')}</h3><p>{T('La ricerca di date e ospiti è incorporata nel sito; disponibilità, condizioni e pagamento proseguono nel motore ufficiale Direct-book.', 'Date and guest search is built into the site; availability, terms and payment continue in the official Direct-book engine.')}</p><a class="cv-button" href="{link('book')}">{T('Apri il motore', 'Open the engine')}</a></article>
</div></div></section>
  </main>

''' + footer()

def book():
    L = LANG
    title = T('Prenota direttamente | Vatican Glamorous · Passeggiata del Gelsomino', 'Book direct | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Verifica la disponibilità e prenota Vatican Glamorous tramite il motore ufficiale.', 'Check availability and book Vatican Glamorous through the official engine.')
    anchor = T('motore', 'booking')
    return head(title, desc) + header() + f'''
  <main class="cream"><div class="cv-wrap cv-book-layout" id="{anchor}"><aside class="cv-book-intro"><p class="cv-eyebrow left">{T('Prenotazione ufficiale', 'Official booking')}</p><h1>{T('Prenota direttamente', 'Book direct')}</h1><p>{T('Inserisci i dati del soggiorno: la ricerca continua nel motore ufficiale Vatican Glamorous con date e ospiti già selezionati.', 'Enter your stay details: the search continues in the official Vatican Glamorous engine with dates and guests already selected.')}</p><div class="cv-info-card"><h3>{T('Contatto diretto', 'Direct contact')}</h3><a href="tel:{PHONE}">{PHONE_TXT}</a><a href="{WA}">WhatsApp</a><a href="mailto:{EMAIL}">Email</a><p>{T('Soggiorno minimo: 2 notti.', 'Minimum stay: 2 nights.')}</p></div><div class="cv-info-card"><h3>{T('Altre piattaforme', 'Other platforms')}</h3><div class="cv-platform-badges"><a href="{AIRBNB}" target="_blank" rel="noopener" aria-label="{T('Prenota su Airbnb', 'Book on Airbnb')}"><img src="{A('icons/airbnb.svg')}" alt="Airbnb"></a><a href="{BOOKING}" target="_blank" rel="noopener" aria-label="{T('Prenota su Booking.com', 'Book on Booking.com')}"><img src="{A('icons/booking.svg')}" alt="Booking.com"></a></div></div></aside><section><form class="cv-book-widget" data-direct-book data-locale="{L}"><h2>{T('Verifica la disponibilità', 'Check availability')}</h2><div class="cv-book-grid"><div><label for="book-in-{L}">{T('Arrivo', 'Check-in')}</label><input id="book-in-{L}" name="checkin" type="date" required></div><div><label for="book-out-{L}">{T('Partenza', 'Check-out')}</label><input id="book-out-{L}" name="checkout" type="date" required></div><div><label for="book-adults-{L}">{T('Adulti', 'Adults')}</label>{select('adults', f'book-adults-{L}', 4, 2)}</div><div><label for="book-children-{L}">{T('Bambini', 'Children')}</label>{select('children', f'book-children-{L}', 3, 0)}</div></div><button class="cv-button" type="submit">{T('Cerca nel motore ufficiale', 'Search the official engine')}</button><p class="cv-book-note">{T('Disponibilità, condizioni e pagamento sono gestiti in sicurezza da Direct-book.', 'Availability, terms and payment are handled securely by Direct-book.')}</p></form><div class="cv-book-fallback">{T('Preferisci aprire subito il motore completo?', 'Prefer to open the full engine now?')}<br><a class="cv-button" href="{DIRECT}?locale={L}" target="_blank" rel="noopener">{T('Apri Direct-book', 'Open Direct-book')}</a></div></section></div></main>
''' + footer()

def privacy():
    title = T('Informativa privacy | Vatican Glamorous · Passeggiata del Gelsomino', 'Privacy policy | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Informativa sul trattamento dei dati personali del sito Vatican Glamorous – Passeggiata del Gelsomino.', 'How Vatican Glamorous – Passeggiata del Gelsomino handles personal data.')
    if LANG == 'it':
        body = f'''<p class="cv-legal-updated">Ultimo aggiornamento: settembre 2026</p>
<p>Questa informativa è resa ai sensi degli articoli 13 e 14 del Regolamento (UE) 2016/679 (GDPR) a chi visita il sito www.vaticanglamorous.com e a chi contatta Vatican Glamorous tramite il sito.</p>
<h2>1. Titolare del trattamento</h2>
<p>Il titolare del trattamento è il gestore della casa vacanze Vatican Glamorous – Passeggiata del Gelsomino, Via S. Telesforo, Roma, Italia. CIN {CIN}. Per qualsiasi richiesta sulla privacy: <a href="mailto:{EMAIL}">{EMAIL}</a>, telefono <a href="tel:{PHONE}">{PHONE_TXT}</a>.</p>
<h2>2. Quali dati trattiamo</h2>
<ul><li><strong>Dati di navigazione.</strong> Il sito è ospitato su GitHub Pages (GitHub Inc.). Come per qualsiasi sito, il server registra dati tecnici come indirizzo IP, data e ora della richiesta e tipo di browser, per garantire il funzionamento e la sicurezza del servizio.</li><li><strong>Dati che ci invii tu.</strong> Se ci scrivi via email, telefono o WhatsApp, trattiamo i dati che ci fornisci (nome, recapiti, date del soggiorno, numero di ospiti, contenuto del messaggio) per risponderti.</li><li><strong>Dati di prenotazione.</strong> Il modulo "Trova la data perfetta" non conserva nulla sul nostro sito: le date e il numero di ospiti che inserisci vengono passati al motore di prenotazione ufficiale Direct-Book (direct-book.com), dove si completa la prenotazione. Le prenotazioni tramite Airbnb o Booking.com avvengono sui rispettivi siti.</li></ul>
<h2>3. Perché li trattiamo e su quale base</h2>
<ul><li>Rispondere alle tue richieste e fornirti informazioni sul soggiorno: misure precontrattuali richieste da te (art. 6.1.b GDPR).</li><li>Gestire la prenotazione e il soggiorno: esecuzione del contratto (art. 6.1.b) e obblighi di legge, per esempio la comunicazione degli ospiti all’autorità di pubblica sicurezza e gli adempimenti fiscali e sul contributo di soggiorno (art. 6.1.c).</li><li>Garantire il funzionamento e la sicurezza del sito: legittimo interesse (art. 6.1.f).</li></ul>
<h2>4. Cookie e contenuti di terze parti</h2>
<p>Il sito non utilizza cookie di profilazione né strumenti di statistica o pubblicità. Alcune pagine caricano contenuti di terze parti:</p>
<ul><li><strong>Google Fonts</strong> (Google), per i caratteri tipografici: il browser si collega ai server di Google, che ricevono il tuo indirizzo IP.</li><li><strong>Video YouTube</strong>, incorporati in modalità a privacy avanzata (youtube-nocookie.com): YouTube può memorizzare informazioni sul tuo dispositivo solo quando avvii la riproduzione.</li></ul>
<p>I link verso siti esterni (Direct-Book, Airbnb, Booking.com, WhatsApp, Google Maps) portano a servizi con proprie informative privacy, che ti invitiamo a consultare.</p>
<h2>5. Destinatari e trasferimenti fuori dall’UE</h2>
<p>I dati possono essere trattati dai fornitori dei servizi sopra indicati (hosting, posta elettronica, messaggistica, piattaforme di prenotazione), dal commercialista per gli adempimenti fiscali e dalle autorità competenti quando previsto dalla legge. Alcuni fornitori, come GitHub e Google, possono trattare i dati negli Stati Uniti, sulla base delle garanzie previste dal GDPR (per esempio l’EU-US Data Privacy Framework o le clausole contrattuali standard).</p>
<h2>6. Per quanto tempo conserviamo i dati</h2>
<p>I messaggi di contatto sono conservati per il tempo necessario a rispondere e a gestire l’eventuale soggiorno. I dati legati alla prenotazione sono conservati per il periodo richiesto dagli obblighi di legge, in particolare fiscali (di norma 10 anni). I dati tecnici di navigazione sono gestiti dal fornitore di hosting secondo le sue politiche.</p>
<h2>7. I tuoi diritti</h2>
<p>Puoi chiedere in qualsiasi momento l’accesso ai tuoi dati, la rettifica, la cancellazione, la limitazione del trattamento, la portabilità e opporti al trattamento basato sul legittimo interesse, scrivendo a <a href="mailto:{EMAIL}">{EMAIL}</a>. Hai anche il diritto di presentare reclamo al Garante per la protezione dei dati personali (<a href="https://www.garanteprivacy.it" target="_blank" rel="noopener">www.garanteprivacy.it</a>).</p>
<h2>8. Modifiche</h2>
<p>Questa informativa può essere aggiornata. La versione in vigore è sempre quella pubblicata su questa pagina.</p>'''
    else:
        body = f'''<p class="cv-legal-updated">Last updated: September 2026</p>
<p>This notice is provided under Articles 13 and 14 of Regulation (EU) 2016/679 (GDPR) to visitors of www.vaticanglamorous.com and to anyone who contacts Vatican Glamorous through the site.</p>
<h2>1. Data controller</h2>
<p>The data controller is the operator of the Vatican Glamorous – Passeggiata del Gelsomino holiday home, Via S. Telesforo, Rome, Italy. CIN {CIN}. For any privacy request: <a href="mailto:{EMAIL}">{EMAIL}</a>, phone <a href="tel:{PHONE}">{PHONE_TXT}</a>.</p>
<h2>2. What data we process</h2>
<ul><li><strong>Browsing data.</strong> The site is hosted on GitHub Pages (GitHub Inc.). As with any website, the server logs technical data such as IP address, date and time of the request and browser type, to keep the service running and secure.</li><li><strong>Data you send us.</strong> If you contact us by email, phone or WhatsApp, we process the data you provide (name, contact details, stay dates, number of guests, message content) to reply.</li><li><strong>Booking data.</strong> The "Find your perfect dates" form stores nothing on our site: the dates and number of guests you enter are passed to the official Direct-Book booking engine (direct-book.com), where the booking is completed. Bookings via Airbnb or Booking.com take place on their respective sites.</li></ul>
<h2>3. Purposes and legal basis</h2>
<ul><li>Replying to your requests and informing you about your stay: pre-contractual measures at your request (Art. 6.1.b GDPR).</li><li>Managing the booking and stay: performance of the contract (Art. 6.1.b) and legal obligations, such as reporting guests to the public security authorities and tax and tourist-tax requirements (Art. 6.1.c).</li><li>Keeping the site running and secure: legitimate interest (Art. 6.1.f).</li></ul>
<h2>4. Cookies and third-party content</h2>
<p>The site uses no profiling cookies and no analytics or advertising tools. Some pages load third-party content:</p>
<ul><li><strong>Google Fonts</strong> (Google), for typefaces: your browser connects to Google’s servers, which receive your IP address.</li><li><strong>YouTube videos</strong>, embedded in privacy-enhanced mode (youtube-nocookie.com): YouTube may store information on your device only when you start playback.</li></ul>
<p>Links to external sites (Direct-Book, Airbnb, Booking.com, WhatsApp, Google Maps) lead to services with their own privacy policies, which we invite you to read.</p>
<h2>5. Recipients and transfers outside the EU</h2>
<p>Data may be processed by the providers listed above (hosting, email, messaging, booking platforms), by our accountant for tax purposes and by the competent authorities where required by law. Some providers, such as GitHub and Google, may process data in the United States under the safeguards provided by the GDPR (for example the EU-US Data Privacy Framework or standard contractual clauses).</p>
<h2>6. How long we keep data</h2>
<p>Contact messages are kept for as long as needed to reply and manage any stay. Booking-related data is kept for the period required by law, in particular tax law (usually 10 years). Technical browsing data is handled by the hosting provider according to its policies.</p>
<h2>7. Your rights</h2>
<p>You may at any time request access to your data, rectification, erasure, restriction of processing and portability, and object to processing based on legitimate interest, by writing to <a href="mailto:{EMAIL}">{EMAIL}</a>. You also have the right to lodge a complaint with the Italian Data Protection Authority (<a href="https://www.garanteprivacy.it" target="_blank" rel="noopener">www.garanteprivacy.it</a>).</p>
<h2>8. Changes</h2>
<p>This notice may be updated. The version in force is always the one published on this page.</p>'''
    return head(title, desc) + header() + f'''
  <main>
{page_hero('A5', T('Soggiorno di Vatican Glamorous', 'Vatican Glamorous living room'), T('Privacy · Dati personali · Cookie', 'Privacy · Personal data · Cookies'), T('Informativa privacy', 'Privacy policy'), T('Come trattiamo i dati di chi visita il sito e di chi ci contatta.', 'How we handle the data of site visitors and of anyone who contacts us.'))}
<section class="cv-section cream"><div class="cv-wrap cv-legal-text">
{body}
</div></section>
  </main>

''' + footer()

BUILD = {'home': home, 'apt': apt, 'rooms': rooms, 'rome': rome, 'gallery': gallery, 'exp': exp, 'info': info, 'book': book, 'privacy': privacy}

for LANG in ('it', 'en'):
    for key in BUILD:
        CUR = key
        path = os.path.join(OUT, slug(key))
        os.makedirs(path, exist_ok=True)
        open(os.path.join(path, 'index.html'), 'w', encoding='utf-8').write(BUILD[key]())

# radice: lingua del browser (IT → /it/, altrimenti /en/)
open(os.path.join(OUT, 'index.html'), 'w').write('''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vatican Glamorous · Passeggiata del Gelsomino</title>
<meta name="description" content="Vatican Glamorous (Passeggiata del Gelsomino): casa vacanze a 200 m da San Pietro, Roma. Holiday home 200 m from St. Peter’s, Rome.">
<link rel="canonical" href="https://www.vaticanglamorous.com/it/">
<link rel="alternate" hreflang="it" href="https://www.vaticanglamorous.com/it/"><link rel="alternate" hreflang="en" href="https://www.vaticanglamorous.com/en/">
<script>location.replace(((navigator.language||'it').toLowerCase().indexOf('it')===0?'it/':'en/')+location.search);</script>
<meta http-equiv="refresh" content="1; url=it/">
</head><body><p><a href="it/">Italiano</a> · <a href="en/">English</a></p></body></html>
''')
urls = []
for key in BUILD:
    for lg in ('it', 'en'): urls.append(f'{DOMAIN}/{slug(key, lg)}')
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(OUT, '.nojekyll'), 'w').write('')
print('ok')
