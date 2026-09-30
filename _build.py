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
V = '73'  # versione cache CSS/JS

GYG_PID = 'OPQQF64'
GYG = {  # stessi link della guida ospiti (Best of Rome); San Pietro: pagina attrazione GetYourGuide con il tuo codice
 'stpeter': 'https://www.getyourguide.com/st-peter-s-basilica-l2617/',
 'vatican': 'https://www.getyourguide.com/it-it/roma-l33/biglietto-di-ingresso-prioritario-per-i-musei-vaticani-e-la-cappella-sistina-t62214/',
 'colosseum': 'https://www.getyourguide.com/it-it/roma-l33/colosseo-foro-romano-e-palatino-tour-guidato-t195566/',
 'food': 'https://www.getyourguide.com/it-it/roma-l33/roma-tour-gastronomico-di-trastevere-e-campo-de-fiori-t460750/',
}
def gyg(key): return f'{GYG[key]}?partner_id={GYG_PID}&amp;cmp=vaticanglamorous_{key}'
LANG = 'it'
def T(it, en): return it if LANG == 'it' else en

PAGES = [  # chiave, slug it, slug en, voce di menu it, en
    ('home', '', '', 'Home', 'Home'),
    ('apt', 'appartamento', 'apartment', "L’appartamento", 'The apartment'),
    ('rooms', 'ambienti', 'spaces', 'Zona notte', 'Sleeping areas'),
    ('rome', 'roma-vaticano', 'rome-vatican', 'Roma &amp; Vaticano', 'Rome &amp; Vatican'),
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

from PIL import Image as _Im
_SIZES = {}
def _size(f):
    if f not in _SIZES:
        try:
            with _Im.open(os.path.join(OUT, 'assets', f)) as im: _SIZES[f] = im.size
        except Exception: _SIZES[f] = None
    return _SIZES[f]

def img(code, alt, cls='', lazy=True, extra='', file=None):
    f = file or f'photos/{code[0]}{int(code[1:]):02d}.webp'
    wh = _size(f); dim = f' width="{wh[0]}" height="{wh[1]}"' if wh else ''
    c = f' class="{cls}"' if cls else ''
    l = ' loading="lazy"' if lazy else ('' if lazy is None else ' fetchpriority="high"')
    return f'<img{c} src="{A(f)}" alt="{alt}"{dim}{l}{' decoding="async"' if lazy else ''} data-photo-code="{code}"{extra}>'

def ph(code, text_it='Foto in arrivo', text_en='Photo coming soon'):
    return f'<div class="vg-placeholder" data-photo-code="{code}">{T(text_it, text_en)}</div>'

def fig(code, alt, cap=None, group=None):
    g = ''
    if group: g = f' data-coverflow-group="{group[0]}" data-group-label="{group[1]}" data-group-name="{group[2]}"'
    cap = alt if cap is None else cap
    fc = f'<figcaption class="cv-photo-caption">{cap}</figcaption>' if cap else ''
    return f'<figure class="cv-photo"{g}>{img(code, alt, lazy=None)}{fc}</figure>'

def coverflow(kind, figs, extra_cls=''):
    c = 'cv-photo-grid' + (' ' + extra_cls if extra_cls else '')
    return f'<div class="{c}" data-coverflow="{kind}">\n' + '\n'.join(figs) + '\n</div>'

def amen(items): return '<ul class="cv-amenities">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

# ---------------------------------------------------------------- HEAD / HEADER / FOOTER
OG_ANCHOR = {'H13': 0.30}   # posizione verticale del ritaglio (0 = in alto, 1 = in basso)
def og_image(code):
    """Crea assets/og/<codice>.jpg (1200x630) dalla foto e ne restituisce l'URL assoluto."""
    from PIL import Image as _I
    dst = os.path.join(OUT, 'assets', 'og', f'{code}.jpg')
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        im = _I.open(os.path.join(OUT, 'assets', f'photos/{code[0]}{int(code[1:]):02d}.webp')).convert('RGB')
        W, H = im.size; tw, th = 1200, 630
        ch = min(H, int(W * th / tw)); cw = int(ch * tw / th)
        left = (W - cw) // 2; top = int((H - ch) * OG_ANCHOR.get(code, 0.4))
        im = im.crop((left, top, left + cw, top + ch)).resize((tw, th), _I.LANCZOS)
        q = 84
        while True:
            im.save(dst, 'JPEG', quality=q, optimize=True, progressive=True)
            if os.path.getsize(dst) < 280_000 or q <= 60: break
            q -= 4
    return f'{DOMAIN}/assets/og/{code}.jpg'

SEO = {  # titolo (max ~65 caratteri) e descrizione (max ~160) per Google, pagina per pagina (IT, EN)
 'home': (('Vatican Glamorous · Loft vicino al Vaticano con parcheggio gratuito',
           'Vatican Glamorous (Passeggiata del Gelsomino): casa vacanze di lusso a 200 m da San Pietro. 4 ospiti, posto auto gratuito, 2 balconi. Miglior prezzo diretto.'),
          ('Vatican Glamorous · Luxury Loft near the Vatican, Free Parking',
           'Vatican Glamorous (Passeggiata del Gelsomino): luxury holiday home 200 m from St. Peter’s, Rome. Sleeps 4, free parking, 2 balconies. Best price when you book direct.')),
 'apt':  (('L’appartamento · Loft contemporaneo vicino a San Pietro',
           'Loft contemporaneo di Vatican Glamorous – Passeggiata del Gelsomino: cucina completa, 2 balconi, Wi‑Fi, aria condizionata, 5° piano con ascensore, zona Vaticano.'),
          ('The Apartment · Contemporary Loft near St. Peter’s, Rome',
           'The Vatican Glamorous – Passeggiata del Gelsomino loft: full kitchen, 2 balconies, Wi‑Fi, air conditioning, 5th floor with lift in Rome’s Vatican area.')),
 'rooms':(('Zona notte · Camera king-size e divano letto | Vatican Glamorous',
           'Camera matrimoniale king-size e ampio living in stile loft con divano letto king-size: Vatican Glamorous ospita comodamente fino a 4 persone vicino al Vaticano.'),
          ('Sleeping Areas · King-size Bedroom & Sofa Bed | Vatican Glamorous',
           'King-size double bedroom and a wide loft-style living room with king-size sofa bed: Vatican Glamorous comfortably sleeps up to 4 guests near the Vatican.')),
 'rome': (('Roma & Vaticano · Alloggio per pellegrini vicino a San Pietro',
           'Casa vacanze per pellegrini a 2 minuti a piedi da San Pietro: Musei Vaticani, Castel Sant’Angelo, stazione Roma San Pietro e posto auto gratuito.'),
          ('Rome & Vatican · Pilgrim Stay near St. Peter’s | Vatican Glamorous',
           'Holiday home for pilgrims, a 2-minute walk from St. Peter’s: Vatican Museums, Castel Sant’Angelo, Roma San Pietro station and free parking.')),
 'exp':  (('Esperienze · Tour e visite a Roma e in Vaticano | Vatican Glamorous',
           'Tour, visite guidate e ingressi prioritari a Roma e in Vaticano per gli ospiti di Vatican Glamorous – Passeggiata del Gelsomino, vicino a San Pietro.'),
          ('Experiences · Tours in Rome and the Vatican | Vatican Glamorous',
           'Tours, guided visits and priority entry in Rome and the Vatican for guests of Vatican Glamorous – Passeggiata del Gelsomino, near St. Peter’s.')),
 'info': (('Info e regole della casa · Vatican Glamorous – Passeggiata del Gelsomino',
           'Contatti, regole della casa e servizi inclusi a Vatican Glamorous – Passeggiata del Gelsomino, Via S. Telesforo, Roma. CIN IT058091C2ZV2HSZ96.'),
          ('Info & House Rules · Vatican Glamorous – Passeggiata del Gelsomino',
           'Contacts, house rules and included services at Vatican Glamorous – Passeggiata del Gelsomino, Via S. Telesforo, Rome. CIN IT058091C2ZV2HSZ96.')),
 'book': (('Prenota direttamente · Miglior prezzo garantito | Vatican Glamorous',
           'Prenota Vatican Glamorous – Passeggiata del Gelsomino al miglior prezzo garantito: loft vicino al Vaticano con parcheggio gratuito, fino a 4 ospiti.'),
          ('Book Direct · Best Price Guaranteed | Vatican Glamorous',
           'Book Vatican Glamorous – Passeggiata del Gelsomino at the best guaranteed price: loft near the Vatican with free parking, sleeps up to 4.')),
 'privacy':(('Privacy e cookie policy | Vatican Glamorous – Passeggiata del Gelsomino',
           'Privacy e cookie policy della Casa Vacanze Vatican Glamorous – Passeggiata del Gelsomino, Roma.'),
          ('Privacy and Cookie Policy | Vatican Glamorous – Passeggiata del Gelsomino',
           'Privacy and cookie policy of the Vatican Glamorous – Passeggiata del Gelsomino Holiday Home, Rome.')),
}

def head(title, desc, image='H01'):
    if CUR in ('home', 'book', 'privacy') or image == 'H01': image = 'H13'
    ogimg = og_image(image)
    t, d = SEO[CUR][0 if LANG == 'it' else 1]
    title, desc = t.replace('&', '&amp;').replace('&amp;amp;', '&amp;'), d
    url_it = DOMAIN + '/' + slug(CUR, 'it'); url_en = DOMAIN + '/' + slug(CUR, 'en')
    url = url_it if LANG == 'it' else url_en
    kw = T('Vatican Glamorous, Passeggiata del Gelsomino, casa vacanze vicino al Vaticano, loft di lusso Roma, appartamento vacanze San Pietro, alloggio pellegrini Roma, casa vacanze Roma con parcheggio gratuito, affitto breve Roma Vaticano',
           'Vatican Glamorous, Passeggiata del Gelsomino, holiday home near the Vatican, luxury loft Rome, apartment near St. Peter’s Basilica, pilgrim stay Rome, holiday home Rome free parking, Rome short stay Vatican')
    home_url = DOMAIN + '/' + slug('home')
    graph = [{'@type': 'WebSite', '@id': DOMAIN + '/#website', 'name': 'Vatican Glamorous', 'alternateName': ['Passeggiata del Gelsomino', 'Vatican Glamorous – Passeggiata del Gelsomino'], 'url': DOMAIN + '/', 'inLanguage': ['it', 'en']}]
    if CUR == 'home':
        graph.append({
            '@type': 'VacationRental', '@id': DOMAIN + '/#vacationrental',
            'name': 'Vatican Glamorous', 'alternateName': 'Passeggiata del Gelsomino',
            'description': desc, 'url': url,
            'image': [f'{DOMAIN}/assets/photos/{c}.webp' for c in ('H01', 'H13', 'H26', 'H11', 'H16', 'H17')],
            'telephone': PHONE, 'email': EMAIL, 'identifier': CIN,
            'address': {'@type': 'PostalAddress', 'streetAddress': 'Via San Telesforo', 'addressLocality': 'Roma', 'addressRegion': 'RM', 'addressCountry': 'IT'},
            'petsAllowed': True, 'numberOfRooms': 2, 'numberOfBedrooms': 1, 'numberOfBathroomsTotal': 1,
            'containsPlace': {'@type': 'Accommodation', 'additionalType': 'EntirePlace', 'occupancy': {'@type': 'QuantitativeValue', 'maxValue': 4},
                'bed': [{'@type': 'BedDetails', 'numberOfBeds': 1, 'typeOfBed': 'King'}, {'@type': 'BedDetails', 'numberOfBeds': 1, 'typeOfBed': 'Sofa bed (king-size)'}],
                'amenityFeature': [{'@type': 'LocationFeatureSpecification', 'name': n, 'value': True} for n in ('Free parking', 'Wi-Fi', 'Kitchen', 'Dishwasher', 'Washer dryer', 'Air conditioning', 'Elevator', 'Balcony', 'Crib', 'Smart TV', 'Workspace', 'Bed linen and towels')]},
            'sameAs': [AIRBNB, BOOKING],
        })
    else:
        name = P[CUR][3] if LANG == 'it' else P[CUR][4]
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Vatican Glamorous', 'item': home_url},
            {'@type': 'ListItem', 'position': 2, 'name': name.replace('&amp;', '&'), 'item': url}]})
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    ld = f'\n  <script type="application/ld+json">{ld}</script>'
    pre = f'\n  <link rel="preload" as="image" href="{A("photos/H01.webp")}" fetchpriority="high">' if CUR == 'home' else ''
    ld = pre + ld
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
  <meta property="og:image" content="{ogimg}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Vatican Glamorous – Passeggiata del Gelsomino">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="{T('it_IT', 'en_GB')}">
  <meta property="og:locale:alternate" content="{T('en_GB', 'it_IT')}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{ogimg}">
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
    menu = ['home', 'apt', 'rooms', 'rome', 'exp', 'info']
    nav = ''.join(f'<a{" class=\"active\"" if k == CUR else ""} href="{link(k)}">{P[k][3] if LANG == "it" else P[k][4]}</a>' for k in menu)
    other = 'en' if LANG == 'it' else 'it'
    vb = T('https://www.villabrando.com/it/', 'https://www.villabrando.com/en/')
    nav += f'<a class="vg-nav-retreat" href="{vb}" target="_blank" rel="noopener">Our Coastal Retreat</a>'
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
    <div><h3>{T('Esplora', 'Explore')}</h3><a href="{link('apt')}">{T('L’appartamento', 'The apartment')}</a><a href="{link('rooms')}">{T('Zona notte', 'Sleeping areas')}</a><a href="{link('rome')}">{T('Roma &amp; Vaticano', 'Rome &amp; Vatican')}</a><a href="{link('exp')}">{T('Esperienze', 'Experiences')}</a></div>
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
        ('H13', T('Camera con letto king-size', 'Bedroom with king-size bed')),
        ('H26', T('Salotto con divano letto, tappeto e opera d’arte', 'Living room with sofa bed, rug and artwork')),
        ('H11', T('Soggiorno con libreria e Smart TV', 'Living room with bookcase and Smart TV')),
        ('H12', T('Cucina attrezzata', 'Fully equipped kitchen')),
        ('H14', T('Camera con scrivania, TV e accesso al corridoio', 'Bedroom with desk, TV and door to the hallway')),
        ('H15', T('Divano letto king-size', 'King-size sofa bed')),
        ('H16', T('Balcone con tavolo per la colazione', 'Balcony with breakfast table')),
        ('H17', T('Bagno completo', 'Full bathroom')),
        ('H18', T('Luce naturale in soggiorno', 'Natural light in the living room')),
        ('H19', T('Ingresso e corridoio', 'Entrance and hallway')),
        ('H21', T('Cabina armadio', 'Walk-in closet')),
        ('H22', T('Camera con scrivania', 'Bedroom with desk')),
    ]
    cards = [
        ('apt', 'H2', T('L’appartamento', 'The apartment'), T('Loft, cucina e spazio all’aperto', 'Loft, kitchen and outdoor space'), T('Zona giorno di Vatican Glamorous', 'Vatican Glamorous living area')),
        ('rooms', 'H3', T('Gli ambienti', 'The spaces'), T('Camera e living in stile loft', 'Bedroom and loft-style living'), T('Camera con letto king-size', 'Bedroom with king-size bed')),
        ('rome', 'H4', T('Roma &amp; Vaticano', 'Rome &amp; Vatican'), T('San Pietro a 200 m', 'St. Peter’s 200 m away'), T('Piazza San Pietro al tramonto', 'St. Peter’s Square at sunset')),
        ('apt#' + T('spazio-esterno', 'outdoor-space'), 'H5', T('Lo spazio all’aperto', 'The outdoor space'), T('Colazione all’aperto', 'Breakfast outdoors'), T('Balcone attrezzato con tavolino e sedute', 'Balcony set up with table and seating')),
    ]
    benefits = [
        ('<svg viewBox="0 0 32 32"><path d="M4 15 16 5l12 10v12H9V15"/><path d="M13 27v-8h6v8"/></svg>', T('Fino a 4 persone', 'Up to 4 guests'), ''),
        ('<svg viewBox="0 0 32 32"><path d="M16 29s9-9 9-17a9 9 0 1 0-18 0c0 8 9 17 9 17Z"/><circle cx="16" cy="12" r="3"/></svg>', T('A 200 m da San Pietro', '200 m from St. Peter’s'), ''),
        ('<svg viewBox="0 0 32 32"><rect x="5" y="5" width="22" height="22" rx="3"/><path d="M13 23V9h5a4 4 0 0 1 0 8h-5"/></svg>', T('Posto auto gratuito', 'Free parking'), T('Proprio sotto il palazzo', 'Right below the building')),
        ('<svg viewBox="0 0 32 32"><path d="M5 27h22M7 27V15h18v12M7 19h18M11 19v8M16 19v8M21 19v8"/><path d="M11 15V7h10v8"/></svg>', T('Spazio all’aperto', 'Outdoor space'), ''),
        ('<svg viewBox="0 0 32 32"><rect x="8" y="4" width="16" height="24" rx="2"/><path d="m12 12 4-4 4 4M12 20l4 4 4-4"/></svg>', T('5° piano con ascensore', '5th floor with lift'), ''),
        ('<svg viewBox="0 0 32 32"><path d="M5 24V12h22v12M5 19h22M9 12V8h14v4"/><path d="M5 24v3M27 24v3"/></svg>', T('Biancheria inclusa', 'Linen included'), T('Lenzuola, asciugamani e kit bagno inclusi', 'Bed linen, towels and bathroom kit included')),
    ]
    b = ''.join(f'<div class="cv-benefit"><span class="cv-benefit-icon">{s}</span><span><strong>{t}</strong>{f'<span>{u}</span>' if u else ''}</span></div>' for s, t, u in benefits)
    cardhtml = '\n'.join(f'''      <a class="cv-card" href="{link(k.split('#')[0]) + ('#' + k.split('#')[1] if '#' in k else '')}" data-reveal><div class="cv-card-media">{img(c, alt, extra=' data-no-lightbox')}</div><div class="cv-card-bottom"><div><h3>{h}</h3><small>{s}</small></div><span class="cv-card-arrow">→</span></div></a>''' for k, c, h, s, alt in cards)
    NL = ' data-lightbox-single'
    dest = [
        (img('H7', T('Mappa: San Pietro a pochi minuti a piedi dall’appartamento', 'Map: St. Peter’s a few minutes’ walk from the apartment'), extra=NL), T('San Pietro', 'St. Peter’s'), 6),
        (img('R4', T('Musei Vaticani e Cappella Sistina', 'Vatican Museums and Sistine Chapel'), extra=NL, file=T('photos/R04.webp', 'photos/R04-en.webp')), T('Musei Vaticani', 'Vatican Museums'), 20),
        (img('H8', T('Castel Sant’Angelo e Ponte Sant’Angelo al tramonto', 'Castel Sant’Angelo and Ponte Sant’Angelo at sunset'), extra=NL), 'Castel Sant’Angelo', 12),
        (img('H9', T('Piazza Navona con la Fontana dei Quattro Fiumi', 'Piazza Navona with the Fountain of the Four Rivers'), extra=NL), 'Piazza Navona', 15),
    ]
    walk = lambda m: f'<p class="vg-dest-time">{m} min {T("a piedi", "on foot")}</p>' if m else ''
    desthtml = '\n'.join(f'      <article class="cv-destination" data-reveal><div class="cv-destination-image">{i}</div><h3>{h}</h3>{walk(m)}</article>' for i, h, m in dest)
    adults = select('adults', f'cv-adulti-{L}', 4, 2)
    kids = select('children', f'cv-bambini-{L}', 3, 0)
    return head(title, desc) + header() + f'''
  <main id="{T('inizio', 'top')}">
    <section class="cv-hero">
      <div class="cv-hero-bg">{img('H1', T('Zona giorno luminosa di Vatican Glamorous', 'Bright living area at Vatican Glamorous'), lazy=False)}</div>
      <div class="cv-wrap cv-hero-inner">
        <div class="cv-hero-copy" data-reveal><p class="cv-kicker">{T('Casa vacanze a Roma · zona Vaticano', 'Holiday home in Rome · Vatican area')}</p><h1 class="cv-title">Vatican <span class="vg-glam">Glamorous</span></h1><p class="vg-hero-sub">Passeggiata del Gelsomino</p><p class="cv-script">{T('Parcheggia l’auto ed entra in Vaticano a piedi', 'Park your car and walk into the Vatican')}</p><p class="cv-locations">{T('San Pietro · Musei Vaticani · Centro storico', 'St. Peter’s · Vatican Museums · Historic centre')}</p><a class="cv-button" href="{link('book')}">{T('Prenota direttamente', 'Book direct')}</a></div>
        <form class="cv-booking" data-booking-form data-booking-url="{link('book')}" data-locale="{L}" aria-label="{T('Ricerca disponibilità', 'Availability search')}" data-reveal><h2>{T('Trova la data perfetta', 'Find your perfect dates')}</h2><div class="cv-date-row"><div class="cv-field"><label for="cv-arrivo-{L}">{T('Arrivo', 'Check-in')}</label><input id="cv-arrivo-{L}" name="checkin" type="date" required></div><div class="cv-field"><label for="cv-partenza-{L}">{T('Partenza', 'Check-out')}</label><input id="cv-partenza-{L}" name="checkout" type="date" required></div><div class="cv-field"><label for="cv-adulti-{L}">{T('Adulti', 'Adults')}</label>{adults}</div><div class="cv-field"><label for="cv-bambini-{L}">{T('Bambini', 'Children')}</label>{kids}</div></div><button class="cv-button" type="submit">{T('Cerca', 'Search')}</button><div class="vg-booking-foot"><p class="cv-minimum vg-rule-min">{T('Soggiorno minimo: 2 notti', 'Minimum stay: 2 nights')}</p><p class="cv-pet vg-rule-pet">🐾 {T('animali ammessi', 'pets welcome')}</p><div class="cv-hero-platforms"><span>{T('Prenota anche su', 'Also book on')}</span><div class="cv-platform-badges"><a href="{AIRBNB}" target="_blank" rel="noopener" aria-label="{T('Prenota su Airbnb', 'Book on Airbnb')}"><img src="{A('icons/airbnb.svg')}" alt="Airbnb" data-no-lightbox></a><a href="{BOOKING}" target="_blank" rel="noopener" aria-label="{T('Prenota su Booking.com', 'Book on Booking.com')}"><img src="{A('icons/booking.svg')}" alt="Booking.com" data-no-lightbox></a></div></div><div class="cv-hero-platforms vg-contact-row"><span>{T('Contattaci', 'Contact us')}</span><div class="vg-contact-icons"><a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24"><path d="M12 3.2a8.8 8.8 0 0 0-7.6 13.2L3.3 20.7l4.4-1.1A8.8 8.8 0 1 0 12 3.2Z"/><path d="M8.9 7.9c.2-.4.4-.4.7-.4h.5c.2 0 .4 0 .5.4l.7 1.7c.1.2 0 .4-.1.6l-.5.6c-.1.1-.1.3 0 .5a6.4 6.4 0 0 0 3 2.7c.2.1.4 0 .5-.1l.6-.7c.2-.2.4-.2.6-.1l1.6.8c.2.1.4.2.4.4 0 .5-.2 1.2-.8 1.6-.6.4-1.5.6-2.9.1a9 9 0 0 1-4.7-4.2c-.8-1.4-.6-2.5-.1-3Z"/></svg></a><a href="tel:{PHONE}" aria-label="{T('Telefono', 'Phone')} {PHONE_TXT}"><svg viewBox="0 0 24 24"><path d="M6.6 3.5h2.6l1.3 4.2-1.9 1.4a11.5 11.5 0 0 0 6.3 6.3l1.4-1.9 4.2 1.3v2.6c0 1.2-1 2.1-2.2 2A16.6 16.6 0 0 1 4.6 5.7c-.1-1.2.8-2.2 2-2.2Z"/></svg></a><a href="mailto:{EMAIL}" aria-label="Email {EMAIL}"><svg viewBox="0 0 24 24"><rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/></svg></a></div></div></div></form>
      </div>
    </section>

    <section class="cv-benefits" id="{T('informazioni', 'highlights')}"><div class="cv-wrap cv-benefit-grid">{b}</div></section>

    <section class="cv-about" id="{T('presentazione', 'about')}"><div class="cv-wrap"><p class="cv-unique vg-scores-line"><b>★</b> {T('4.95 su Airbnb · 9.8 su Booking.com', '4.95 on Airbnb · 9.8 on Booking.com')}</p><div class="cv-centered" data-reveal><img class="vg-logo-full" src="{A('brand/logo-vatican-glamorous.png')}" alt="Vatican Glamorous – Passeggiata del Gelsomino, {T('appartamento in stile contemporaneo', 'a contemporary style apartment')}" width="1040" height="754" data-no-lightbox><h2 class="cv-heading">{T('Un loft contemporaneo a due passi da San Pietro', 'A contemporary loft a stone’s throw from St. Peter’s')}</h2><p class="cv-script">{T('Spazi autentici.<br>Soggiorni indimenticabili.', 'Authentic spaces.<br>Unforgettable stays.')}</p></div>{coverflow('home', [fig(c, a) for c, a in teaser], 'cv-home-teaser')}<div class="cv-home-teaser-footer"><p class="cv-tagline-uses"><em>{T('Ideale per famiglie, amici, pellegrini, smart-working, set fotografici e riprese.', 'Ideal for families, friends, pilgrims, smart-working, photo shoots and filming.')}</em></p><p>{T('Vatican Glamorous è una casa vacanze ad uso esclusivo, rinnovata in stile loft contemporaneo, al quinto piano (con ascensore) di un tipico palazzo d’epoca a circa 200 metri dalla Basilica di San Pietro.', 'Vatican Glamorous is an exclusive-use holiday home, renovated in a contemporary loft style, on the fifth floor (with lift) of a typical period building about 200 metres from St. Peter’s Basilica.')}</p><p>{T('Ospita comodamente fino a 4 persone: una camera con letto king-size, un comodo divano letto king-size nella zona giorno, cucina completa, bagno e un balconcino attrezzato per la colazione all’aperto, più un secondo balcone. Il posto auto gratuito si trova proprio sotto il palazzo.', 'It comfortably sleeps up to 4 guests: a bedroom with a king-size bed, a comfortable king-size sofa bed in the living area, a full kitchen, a bathroom and a small balcony set up for breakfast outdoors, plus a second balcony. Free parking is right below the building.')}</p><a class="cv-button" href="{link('book')}">{T('Scopri la disponibilità', 'Check availability')}</a></div></div></section>

    <section class="cv-discover" id="{T('scopri', 'discover')}"><div class="cv-wrap"><div class="cv-centered" data-reveal><p class="cv-eyebrow">{T('Scopri', 'Discover')}</p><h2 class="cv-heading">{T('Stile, comfort e il Vaticano sotto casa.', 'Style, comfort and the Vatican on your doorstep.')}</h2></div><div class="cv-card-grid">
{cardhtml}
    </div></div></section>

    <section class="cv-ribbon"><div class="cv-wrap cv-ribbon-grid"><div class="cv-award" data-reveal><strong>{T('Le vostre splendide recensioni', 'Your wonderful reviews')}</strong><div class="vg-scores"><span>★ 4.95 Airbnb</span><span>9.8/10 Booking.com</span></div><span>Booking.com · Traveller Review Award 2026</span></div><div class="cv-film" data-reveal><p>{T('Cerchi una location per un servizio fotografico?<br>Contattaci per un’offerta dedicata.', 'Looking for a location for a photo shoot?<br>Contact us for a tailored offer.')}</p><a class="cv-button outline" href="{WA}" target="_blank" rel="noopener">{T('Scrivici', 'Contact us')}</a></div></div></section>

    <section class="cv-experiences" id="{T('esperienze', 'experiences')}"><div class="cv-wrap"><div class="cv-centered" data-reveal><p class="cv-eyebrow">{T('Esplora', 'Explore')}</p><h2 class="cv-heading">{T('Roma a piedi, dal Vaticano al centro', 'Rome on foot, from the Vatican to the centre')}</h2><p class="vg-walk-intro">{T('Tempi a piedi dall’appartamento', 'Walking times from the apartment')}</p><p class="vg-walk-sub">{T('Le principali mete si raggiungono a piedi: anche il Pantheon è a soli 20 minuti.', 'The main sights are within walking distance: even the Pantheon is only 20 minutes away.')}</p></div><div class="cv-destination-row">
{desthtml}
    </div><p class="cv-ulisse-tagline">{T('Dormire all’ombra del Cupolone', 'Sleep in the shadow of the great dome')}</p><a class="cv-button outline" href="{link('rome')}">{T('Roma &amp; Vaticano', 'Rome &amp; Vatican')}</a>
    </div></section>

    <section class="cv-cta-band vg-best-band"><div class="cv-wrap"><h2>{T('Prenota direttamente con noi', 'Book directly with us')}</h2><p class="vg-best-band-script">{T('e ottieni il miglior prezzo garantito!', 'and get the best guaranteed price!')}</p><a class="cv-button" href="{link('book')}">{T('Prenota direttamente', 'Book direct')}</a></div></section>
  </main>

''' + footer()

def apt():
    title = T('L’appartamento | Vatican Glamorous · Passeggiata del Gelsomino', 'The apartment | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Il loft di Vatican Glamorous: zona giorno contemporanea, cucina completa, 2 balconi, 5° piano con ascensore a 200 m da San Pietro.', 'The Vatican Glamorous loft: contemporary living area, full kitchen, 2 balconies, 5th floor with lift 200 m from St. Peter’s.')
    f = [
        fig('A3', T('Sala in stile loft con poltrona, libreria e vista sulla zona pranzo', 'Loft-style living room with armchair, bookcase and view of the dining area'), T('Zona giorno', 'Living area')),
        fig('A4', T('Ingresso con panca blu e vista sulla zona pranzo e la cucina', 'Entrance with blue bench and view of the dining area and kitchen'), T('Ingresso', 'Entrance')),
        fig('A5', T('Soggiorno luminoso con porta-finestra sul balcone', 'Bright living room with French window to the balcony'), T('Soggiorno', 'Living room')),
        fig('A6', T('Tavolino in vetro con guida di benvenuto', 'Glass coffee table with welcome guide'), T('Benvenuti', 'Welcome')),
        fig('A9', T('Panca imbottita e opera d’arte contemporanea', 'Upholstered bench and contemporary artwork'), T('Arte alle pareti', 'Art on the walls')),
        fig('A10', T('Cabina armadio con ripiani rossi', 'Walk-in closet with red shelves'), T('Cabina armadio', 'Walk-in closet')),
        fig('A11', T('Composizione fotografica dell’appartamento', 'Photo collage of the apartment'), 'Vatican Glamorous'),
        fig('A14', T('Dettagli della camera: comodino, lampada e testiera', 'Bedroom details: bedside table, lamp and headboard'), T('Camera', 'Bedroom')),
    ]
    return head(title, desc, 'A01') + header() + f'''
  <main>
{page_hero('A1', T('Soggiorno con libreria e Smart TV', 'Living room with bookcase and Smart TV'), T('Stile contemporaneo · Luce · Comfort', 'Contemporary style · Light · Comfort'), T('L’appartamento', 'The apartment'), T('Un loft raffinato al quinto piano di un palazzo d’epoca, a due passi da San Pietro.', 'A refined loft on the fifth floor of a period building, a short walk from St. Peter’s.'))}
<section class="vg-featbar" aria-label="{T('Dotazioni principali', 'Main amenities')}"><div class="cv-wrap"><ul class="vg-feat-list"><li><svg viewBox="0 0 32 32"><path d="M5 12h22v14H5z"/><path d="M5 17h22M11 21h2"/><path d="M10 12V6M16 12V6M22 12V6"/></svg><span>{T('Cucina completa', 'Full kitchen')}</span></li><li><svg viewBox="0 0 32 32"><rect x="6" y="4" width="20" height="24" rx="2"/><path d="M6 10h20"/><circle cx="16" cy="19" r="5"/></svg><span>{T('Lavastoviglie', 'Dishwasher')}</span></li><li><svg viewBox="0 0 32 32"><rect x="6" y="4" width="20" height="24" rx="2"/><circle cx="16" cy="18" r="6"/><path d="M10 8h2"/></svg><span>{T('Lavasciuga', 'Washer-dryer')}</span></li><li><svg viewBox="0 0 32 32"><path d="M4 12a17 17 0 0 1 24 0M8 16a11 11 0 0 1 16 0M12 20a5 5 0 0 1 8 0"/><circle cx="16" cy="24" r="1.5"/></svg><span>{'Wi‑Fi'}</span></li><li><svg viewBox="0 0 32 32"><rect x="4" y="6" width="24" height="16" rx="2"/><path d="M11 27h10M16 22v5"/></svg><span>{T('Smart Monitor con Netflix', 'Smart monitors with Netflix')}</span></li><li><svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="11"/><path d="M11 18a6 6 0 1 1 10 0"/></svg><span>{'Amazon Alexa'}</span></li><li><svg viewBox="0 0 32 32"><rect x="4" y="7" width="24" height="9" rx="2"/><path d="M8 20c1 2 1 4 0 6M16 20c1 2 1 4 0 6M24 20c1 2 1 4 0 6"/></svg><span>{T('Aria condizionata', 'Air conditioning')}</span></li><li><svg viewBox="0 0 32 32"><path d="M4 12h24M7 12v14M25 12v14M18 12v8h7"/><rect x="10" y="4" width="10" height="6" rx="1"/></svg><span>{T('Scrivania per smart-working', 'Smart-working desk')}</span></li><li><svg viewBox="0 0 32 32"><path d="M9 12V5h14v7"/><rect x="5" y="12" width="22" height="10" rx="2"/><path d="M9 18h14v9H9z"/></svg><span>{T('Stampante', 'Printer')}</span></li><li class="vg-feat-guide"><a href="{GUIDE}" target="_blank" rel="noopener"><svg viewBox="0 0 32 32"><rect x="9" y="3" width="14" height="26" rx="3"/><path d="M14 25h4M13 9h6M13 13h6M13 17h4"/></svg><span><strong>{T('Guida ospiti digitale', 'Digital guest guide')}</strong><small>{T('casa, zona, tour, ristoranti, attività e mappe', 'house, area, tours, restaurants, activities and maps')}</small></span></a></li></ul></div></section>
<section class="cv-section cream" id="{T('foto', 'photos')}"><div class="cv-wrap">{centered(T('Fotografie', 'Photos'), T('Uno sguardo all’appartamento', 'A look at the apartment'))}
{coverflow('features', f)}
</div></section>
<section class="cv-section cv-villa-intro" id="{T('presentazione', 'about')}"><div class="cv-wrap cv-editorial"><div class="cv-editorial-copy"><p class="cv-eyebrow left">Vatican Glamorous</p><h2 class="cv-script-title">{T('Un loft contemporaneo vicino al Vaticano', 'A contemporary loft near the Vatican')}</h2><p>{T('Casa vacanze ad uso esclusivo, rinnovata di recente con cura in stile loft contemporaneo, ideale per famiglie e amici fino a 4 persone.', 'An exclusive-use holiday home, recently and carefully renovated in a contemporary loft style, ideal for families and friends of up to 4.')}</p><p>{T('Il nome “Passeggiata del Gelsomino” richiama il vicino e suggestivo viale che conduce allo Stato della Città del Vaticano.', 'The name “Passeggiata del Gelsomino” (Jasmine Walk) recalls the nearby, evocative avenue that leads to Vatican City.')}</p><p>{T('Siamo così vicini al centro che preferirai raggiungere ogni meta a piedi.', 'We are so close to the centre that you will want to walk everywhere.')}</p><div class="cv-facts"><div class="cv-fact"><strong>4</strong><span>{T('ospiti', 'guests')}</span></div><div class="cv-fact"><strong>5°</strong><span>{T('piano', 'floor')}</span></div><div class="cv-fact"><strong>2</strong><span>{T('balconi', 'balconies')}</span></div></div></div><div class="cv-editorial-media">{img('A2', T('Zona giorno con divano, tappeto e opera d’arte', 'Living area with sofa, rug and artwork'))}</div></div></section>
<section class="cv-section cream cv-villa-living" id="{T('cucina', 'kitchen')}"><div class="cv-wrap"><h2 class="cv-living-title">{T('Zona giorno e cucina', 'Living area &amp; kitchen')}</h2><div class="cv-editorial reverse"><div class="cv-editorial-copy"><p class="cv-script">{T('Spazi autentici.<br>Soggiorni indimenticabili.', 'Authentic spaces.<br>Unforgettable stays.')}</p><p>{T('Un ampio soggiorno in stile loft con divano letto king-size e una cucina completa di tutti gli elettrodomestici.', 'A spacious loft-style living room with a king-size sofa bed and a kitchen complete with all appliances.')}</p>{amen([T('Cucina completa', 'Full kitchen'), T('Lavastoviglie', 'Dishwasher'), T('Lavasciuga', 'Washer-dryer'), 'Wi‑Fi', T('Smart Monitor con Netflix e app streaming', 'Smart monitors with Netflix and streaming apps'), 'Amazon Alexa', T('Aria condizionata automatica', 'Automatic air conditioning'), T('Scrivania per smart-working', 'Desk for smart-working'), T('Stampante', 'Printer')])}</div><div class="cv-editorial-media">{img('A12', T('Cucina attrezzata con elettrodomestici in acciaio', 'Equipped kitchen with stainless-steel appliances'))}</div></div></div></section>
<section class="cv-section cv-villa-living vg-outdoor" id="{T('spazio-esterno', 'outdoor-space')}"><div class="cv-wrap"><div class="cv-editorial"><h2 class="cv-living-title">{T('Lo spazio all’aperto', 'The outdoor space')}</h2><div class="cv-editorial-copy"><p class="cv-script">{T('Colazione all’aria aperta', 'Breakfast in the open air')}</p><p>{T('Un piccolo balcone tutto per voi, attrezzato con tavolino e sedute: perfetto per la colazione in due o in quattro, o per un aperitivo al tramonto con vista sui tetti del quartiere. L’appartamento ha anche un secondo balcone.', 'A small balcony all to yourselves, set up with a table and seating: perfect for breakfast for two or four, or a sunset aperitivo overlooking the neighbourhood rooftops. The apartment also has a second balcony.')}</p>{amen([T('Tavolino per la colazione in 2–4', 'Breakfast table for 2–4'), T('Sedute da esterno', 'Outdoor seating'), T('Luce naturale tutto il giorno', 'Natural light all day'), T('Affaccio sul quartiere', 'Views over the neighbourhood')])}</div><div class="cv-editorial-media">{img('A13', T('Balcone con tavolino, sedie e sgabelli', 'Balcony with small table, chairs and stools'))}</div></div></div></section>
<section class="cv-section cream" id="{T('caratteristiche', 'features')}"><div class="cv-wrap">{centered(T('Dettagli', 'Details'), T('Caratteristiche della casa', 'Property features'))}{amen([T('5° piano con ascensore', '5th floor with lift'), T('Palazzo d’epoca', 'Period building'), T('Posto auto gratuito sotto il palazzo', 'Free parking below the building'), T('1 camera matrimoniale king-size', '1 king-size double bedroom'), T('Ampio soggiorno con divano letto king-size', 'Wide living room with king-size sofa bed'), T('1 bagno completo', '1 full bathroom'), T('Cabina armadio', 'Walk-in closet'), T('2 balconi', '2 balconies'), T('Culla e passeggino', 'Cot and stroller'), T('Animali di piccola taglia ammessi', 'Small pets welcome'), T('Biancheria, asciugamani e kit bagno inclusi', 'Bed linen, towels and toiletries included'), T('Nel centro di Roma, accanto al Vaticano', 'In the centre of Rome, next to the Vatican'), T('Vicino alla stazione Roma San Pietro', 'Close to Roma San Pietro railway station'), T('Vietato fumare in casa', 'No smoking indoors')])}</div></section>
{cta(T('Vivi Vatican Glamorous', 'Stay at Vatican Glamorous'), T('Verifica le date nel motore di prenotazione ufficiale.', 'Check dates in the official booking engine.'), T('Scopri la disponibilità', 'Check availability'))}
  </main>

''' + footer()

def rooms():
    title = T('Zona notte | Vatican Glamorous · Passeggiata del Gelsomino', 'Sleeping areas | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Camera con letto king-size, divano letto king-size e bagno completo: Vatican Glamorous ospita fino a 4 persone vicino a San Pietro.', 'A king-size bedroom, a king-size sofa bed and a full bathroom: Vatican Glamorous sleeps up to 4 near St. Peter’s.')
    g1 = ('C01', T('Camera', 'Bedroom'), T('Camera matrimoniale', 'Double bedroom'))
    g2 = ('C02', T('Soggiorno', 'Living room'), T('Divano letto', 'Sofa bed'))
    f = [
        fig('C4', T('Letto con opere d’arte alle pareti', 'Bed with artworks on the walls'), g1[2], g1),
        fig('C2', T('Letto king-size con cuscini blu e asciugamani', 'King-size bed with blue cushions and towels'), g1[2], g1),
        fig('C5', T('Dettaglio della testiera e dei cuscini', 'Headboard and cushions detail'), g1[2], g1),
        fig('C6', T('Camera con scrivania e finestra', 'Bedroom with desk and window'), g1[2], g1),
        fig('C7', T('Comodino con lampada e sveglia', 'Bedside table with lamp and clock'), g1[2], g1),
        fig('C8', T('Camera con pannelli in legno e luci calde', 'Bedroom with wood panelling and warm lights'), g1[2], g1),
        fig('C19', T('Camera con scrivania, TV e accesso al corridoio', 'Bedroom with desk, TV and door to the hallway'), g1[2], g1),
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
    prev = f'''<div class="cv-room-preview-grid"><div class="cv-room-preview"><h3>{g1[2]}</h3><p>{T('Un’ampia camera con letto king-size, testiera imbottita e arredi contemporanei.', 'A spacious bedroom with a king-size bed, upholstered headboard and contemporary furnishings.')}</p><div class="cv-detail-list"><span>{T('Letto king-size', 'King-size bed')}</span><span>Smart Monitor</span><span>{T('Aria condizionata', 'Air conditioning')}</span><span>Wi‑Fi</span><span>Amazon Alexa</span></div></div><div class="cv-room-preview"><h3>{g2[2]}</h3><p>{T('Nella zona giorno, un comodo divano letto king-size per altri due ospiti.', 'In the living area, a comfortable king-size sofa bed for two more guests.')}</p><div class="cv-detail-list"><span>{T('King-size', 'King-size')}</span><span>Smart TV</span><span>{T('Aria condizionata', 'Air conditioning')}</span><span>Wi‑Fi</span><span>Amazon Alexa</span></div></div></div>'''
    return head(title, desc, 'C01') + header() + f'''
  <main>
{page_hero('C1', T('Camera con letto king-size', 'Bedroom with king-size bed'), T('Zone notte e riposo', 'Sleeping and resting areas'), T('Gli ambienti', 'The spaces'), T('Una camera matrimoniale king-size e un ampio living in stile loft con divano letto king-size: ospita comodamente fino a 4 persone.', 'A king-size double bedroom and a wide loft-style living room with a king-size sofa bed: comfortably sleeps up to 4 guests.'))}
<section class="cv-section" id="{T('foto-ambienti', 'space-photos')}"><div class="cv-wrap">{centered(T('Zone riposo', 'Places to rest'), T('Gli ambienti', 'The spaces'))}
{coverflow('rooms', f)}
{prev}
</div></section>
<section class="cv-section cream" id="{T('dotazioni', 'amenities')}"><div class="cv-wrap">{centered('Comfort', T('Dotazioni della zona notte', 'Sleeping area amenities'))}{amen([T('1 letto king-size', '1 king-size bed'), T('1 divano letto king-size', '1 king-size sofa bed'), T('Culla', 'Cot'), T('Cabina armadio', 'Walk-in closet'), T('Scrivania', 'Desk'), T('Aria condizionata', 'Air conditioning'), 'Wi‑Fi', T('Biancheria inclusa', 'Bed linen included'), T('Asciugamani e kit bagno', 'Towels and toiletries')])}</div></section>
<section class="cv-section" id="{T('bagno', 'bathroom')}"><div class="cv-wrap">{centered(T('Comfort e funzionalità', 'Comfort and practicality'), T('Il bagno', 'The bathroom'), '<p>' + T('Scorri le fotografie del bagno completo con doccia.', 'Browse the photos of the full bathroom with shower.') + '</p>')}
{coverflow('bathrooms', bath, 'cv-bathroom-coverflow')}
</div></section>
{cta(T('Il tuo riposo vicino a San Pietro', 'Rest easy near St. Peter’s'), '', T('Verifica le date', 'Check dates'))}
  </main>

''' + footer()

def rome():
    title = T('Roma &amp; Vaticano | Vatican Glamorous · Passeggiata del Gelsomino', 'Rome &amp; Vatican | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Dintorni di Vatican Glamorous: San Pietro a 200 m, soggiorno per pellegrini, Musei Vaticani, Castel Sant’Angelo e come muoversi a Roma.', 'Around Vatican Glamorous: St. Peter’s 200 m away, pilgrim lodging, the Vatican Museums, Castel Sant’Angelo and getting around Rome.')
    walk = [(T('Vaticano', 'Vatican'), 6), ('Castel Sant’Angelo', 12), ('Piazza Navona', 15), ('Pantheon', 20),
            (T('Ospedale Bambino Gesù', 'Bambino Gesù Hospital'), 14), (T('Isola Tiberina · Ospedale Gemelli Isola (Fatebenefratelli)', 'Tiber Island · Gemelli Isola Hospital (Fatebenefratelli)'), 20)]
    wl = '<ul class="vg-walk">' + ''.join(f'<li><span>{n}</span><b>{m} min {T("a piedi", "on foot")}</b></li>' for n, m in walk) + '</ul>'
    how = [
        (T('A piedi', 'On foot'), T('Il modo migliore per vivere il quartiere: San Pietro, Borgo e Castel Sant’Angelo sono a pochi minuti.', 'The best way to enjoy the area: St. Peter’s, Borgo and Castel Sant’Angelo are minutes away.')),
        (T('In treno', 'By train'), T('La stazione ferroviaria di Roma San Pietro è a pochi passi ed è collegata con altre stazioni della città.', 'Roma San Pietro railway station is just a short walk away and connected to other city stations.')),
        (T('In autobus e metro', 'By bus and metro'), T('Il quartiere è ben servito dagli autobus; la metropolitana collega il Vaticano al resto della città. [testo da verificare]', 'The area is well served by buses; the metro links the Vatican with the rest of the city. [text to be checked]')),
        (T('In auto', 'By car'), T('Posto auto gratuito proprio sotto il palazzo: lasci l’auto e ti muovi a piedi.', 'Free parking right below the building: leave the car and explore on foot.')),
        (T('Bici e monopattini', 'Bikes and scooters'), T('Biciclette e monopattini in sharing sono disponibili ovunque nei dintorni.', 'Shared bikes and scooters are available all around the area.')),
        (T('Verde e sport', 'Green spaces'), T('Il grande parco di Villa Pamphili è ideale per una corsa al mattino.', 'The large Villa Pamphili park is ideal for a morning run.')),
    ]
    hw = '<div class="cv-info-grid">' + ''.join(f'<article class="cv-info-card"><h3>{h}</h3><p>{p}</p></article>' for h, p in how) + '</div>'
    return head(title, desc, 'R01') + header() + f'''
  <main>
{page_hero('R1', T('San Pietro illuminato al tramonto visto dal Tevere', 'St. Peter’s lit up at dusk seen from the Tiber'), T('Dintorni · San Pietro · Musei Vaticani', 'Surroundings · St. Peter’s · Vatican Museums'), T('Roma &amp; Vaticano', 'Rome &amp; Vatican'), T('Tutte le bellezze di Roma sono a pochi passi: il Vaticano è a 5 minuti a piedi.', 'All the beauty of Rome is just steps away: the Vatican is a 5-minute walk.'))}
<section class="cv-section cream vg-surround" id="{T('dintorni', 'surroundings')}"><div class="cv-wrap cv-editorial"><div class="cv-editorial-copy"><p class="cv-eyebrow left">{T('Dintorni', 'Surroundings')}</p><h2>{T('Una casa nel centro di Roma', 'A home in the centre of Rome')}</h2><p>{T('Il quartiere è servito da bar e ristoranti dove gustare la cucina italiana e romana, e da mezzi pubblici per raggiungere ogni angolo della città.', 'The area is full of bars and restaurants serving Italian and Roman cuisine, with public transport to every corner of the city.')}</p>{wl}</div><div class="cv-editorial-media">{img('R2', T('Mappa: Vaticano a 2 minuti a piedi dall’appartamento', 'Map: the Vatican 2 minutes on foot from the apartment'))}</div></div></section>
<section class="cv-section vg-stpeter" id="{T('san-pietro', 'st-peters')}"><div class="cv-wrap cv-editorial reverse"><div class="cv-editorial-copy"><p class="cv-script">{T('All’ombra del Cupolone', 'In the shadow of the great dome')}</p><h2>{T('San Pietro', 'St. Peter’s')}</h2><p>{T('La Basilica e Piazza San Pietro sono a circa 200 metri: ideale per pellegrini, udienze e celebrazioni, con la tranquillità di tornare a casa in pochi minuti. [testo segnaposto]', 'The Basilica and St. Peter’s Square are about 200 metres away: ideal for pilgrims, audiences and celebrations, with the peace of being back home in minutes. [placeholder text]')}</p></div><div class="cv-editorial-media">{img('R3', T('Piazza San Pietro e la Basilica al tramonto', 'St. Peter’s Square and Basilica at sunset'))}</div></div></section>
<section class="cv-section cream" id="{T('pellegrini', 'pilgrims')}"><div class="cv-wrap">{centered(T('Soggiorno per pellegrini', 'Pilgrim lodging'), T('Il Vaticano con comfort e comodità', 'The Vatican area with comfort and convenience'), '<p>' + T('Stai organizzando una visita in Vaticano? Soggiorna nella nostra casa, così vicina da sentirti già dentro lo Stato della Città del Vaticano: raggiungi facilmente le celebrazioni storiche e spirituali di Roma e poi ritrovi la tranquillità della nostra residenza, con posto auto gratuito proprio sotto casa.', 'Planning a visit to the Vatican? Stay at our charming home, so close you will feel you are already inside Vatican City: enjoy easy access to Rome’s historical and spiritual celebrations, then retreat to the tranquillity of our residence, with free parking right below.') + '</p><p class="cv-script vg-why">' + T('Perché scegliere la nostra casa a Roma?', 'Why choose our holiday home in Rome?') + '</p>')}<div class="cv-info-grid"><article class="cv-info-card"><h3>{T('Vicinanza al Vaticano (2 min. a piedi)', 'Proximity to the Vatican (2 min. walk)')}</h3><p>{T('A pochi passi dal cuore degli eventi vaticani: partecipi pienamente alle celebrazioni e torni in un rifugio tranquillo.', 'Just a short distance from the heart of the Vatican events, so you can fully take part in the celebrations and return to a peaceful retreat.')}</p></article><article class="cv-info-card"><h3>{T('Scoperta culturale', 'Cultural exploration')}</h3><p>{T('Scopri la storia e le meraviglie di Roma e dei suoi dintorni, con gite verso luoghi iconici e angoli nascosti.', 'Discover the rich history and wonders of Rome and its surroundings, with day trips to iconic landmarks and hidden gems.')}</p></article><article class="cv-info-card"><h3>{T('Comfort esclusivo', 'Exclusive comfort')}</h3><p>{T('Un appartamento accogliente, ideale per 4 amici o una famiglia che cerca una base centrale e comoda per il proprio pellegrinaggio.', 'A welcoming apartment, ideal for 4 friends or a family looking for a central, convenient base for their pilgrimage.')}</p></article><article class="cv-info-card"><h3>{T('Parcheggio gratuito', 'Free car parking')}</h3><p>{T('Posto auto privato gratuito proprio sotto il palazzo: la tranquillità di alloggiare vicino a San Pietro.', 'Secure, free private car parking just under the building: peace of mind, close to St. Peter’s Basilica.')}</p></article></div><p style="max-width:720px;margin:26px auto 0;text-align:center">{T('Prenota ora e vivi Roma e il Vaticano in un equilibrio indimenticabile tra spiritualità e relax.', 'Book your stay now and enjoy Rome and Vatican City with an unforgettable blend of spiritual fulfilment and relaxation.')}</p><div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:18px"><a class="cv-button" href="{link('book')}">{T('Prenota direttamente', 'Book direct')}</a><a class="cv-button outline" href="{link('exp')}">{T('Tour e attività', 'Tours &amp; activities')}</a></div></div></section>
<section class="cv-section sky" id="{T('musei-vaticani', 'vatican-museums')}"><div class="cv-wrap cv-editorial"><div class="cv-editorial-copy"><p class="cv-eyebrow left">{T('Arte', 'Art')}</p><h2>{T('Musei Vaticani', 'Vatican Museums')}</h2><p>{T('Musei Vaticani e Cappella Sistina a pochi minuti a piedi. Consigliamo di prenotare in anticipo biglietti o visite guidate con ingresso prioritario. [testo segnaposto]', 'The Vatican Museums and Sistine Chapel are a few minutes’ walk away. We recommend booking tickets or guided tours with priority entry in advance. [placeholder text]')}</p><a class="cv-button" href="{link('exp')}">{T('Tour ed esperienze', 'Tours &amp; experiences')}</a></div><div class="cv-editorial-media">{img('R4', T('Musei Vaticani e Cappella Sistina', 'Vatican Museums and Sistine Chapel'), file=T('photos/R04.webp', 'photos/R04-en.webp'))}</div></div></section>
<section class="cv-section cream" id="{T('come-muoversi', 'getting-around')}"><div class="cv-wrap">{centered(T('Mobilità', 'Getting around'), T('Come muoversi', 'How to get around'))}{hw}</div></section>
{cta(T('La tua base a Roma', 'Your base in Rome'), '', T('Verifica le date', 'Check dates'))}
  </main>

''' + footer()

def exp():
    title = T('Esperienze | Vatican Glamorous · Passeggiata del Gelsomino', 'Experiences | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Tour, visite ed esperienze a Roma e in Vaticano per gli ospiti di Vatican Glamorous.', 'Tours, visits and experiences in Rome and the Vatican for Vatican Glamorous guests.')
    cards = [
        (img('E2', T('Piazza San Pietro al tramonto', 'St. Peter’s Square at sunset'), extra=' data-no-lightbox'), T('San Pietro', 'St. Peter’s'), T('Basilica e cupola', 'Basilica and dome')),
        (img('E3', T('Musei Vaticani e Cappella Sistina', 'Vatican Museums and Sistine Chapel'), file=T('photos/R04.webp', 'photos/R04-en.webp')), T('Musei Vaticani', 'Vatican Museums'), T('Cappella Sistina', 'Sistine Chapel')),
        (img('E4', T('Colosseo e Fori Imperiali al tramonto', 'Colosseum and Imperial Forums at sunset'), extra=' data-no-lightbox'), T('Roma antica', 'Ancient Rome'), T('Colosseo e Fori', 'Colosseum and Forums')),
        (img('E5', T('Food tour a Trastevere', 'Trastevere food tour'), extra=' data-no-lightbox'), 'Trastevere', T('Sapori romani', 'Roman flavours')),
    ]
    keys = ['stpeter', 'vatican', 'colosseum', 'food']
    ch = ''.join(f'<a class="cv-card" href="{gyg(k)}" target="_blank" rel="noopener sponsored" aria-label="{h} ({T("si apre in una nuova scheda", "opens in a new tab")})"><div class="cv-card-media">{i}</div><div class="cv-card-bottom"><div><h3>{h}</h3><small>{s}</small></div><span class="cv-card-arrow">→</span></div></a>' for (i, h, s), k in zip(cards, keys))
    return head(title, desc, 'E01') + header() + f'''
  <main>
{page_hero('E1', T('San Pietro al tramonto', 'St. Peter’s at dusk'), T('Vaticano · Roma · Esperienze', 'Vatican · Rome · Experiences'), T('Esperienze', 'Experiences'), T('Pagina in preparazione: qui arriveranno le pagine della guida ospiti di Vatican Glamorous. [testo segnaposto]', 'Page in progress: the Vatican Glamorous guest guide pages will be added here. [placeholder text]'))}
<section class="cv-section"><div class="cv-wrap"><div class="cv-centered"><p class="cv-eyebrow">{T('Dintorni', 'Surroundings')}</p><h2 class="cv-heading">{T('Roma da vivere', 'Rome to experience')}</h2><p class="cv-script">{T('Il Vaticano sotto casa.', 'The Vatican on your doorstep.')}</p><p>{T('Visite guidate, ingressi prioritari ed esperienze scelte per i nostri ospiti. [testo segnaposto]', 'Guided visits, priority entry and experiences chosen for our guests. [placeholder text]')}</p></div><div class="cv-card-grid">{ch}</div></div></section>
<section class="cv-section sky vg-guide"><div class="cv-wrap cv-editorial reverse"><div class="cv-editorial-copy"><p class="cv-script">{T('Una guida da portare con te', 'A guide to take with you')}</p><h2>{T('Guida ospiti', 'Guest guide')}</h2><p>{T('Consulta la guida di Vatican Glamorous con consigli sul quartiere, trasporti e attrazioni. [testo segnaposto]', 'Browse the Vatican Glamorous guide with tips on the area, transport and sights. [placeholder text]')}</p><a class="cv-button" href="{GUIDE}" target="_blank" rel="noopener">{T('Apri la guida', 'Open the guide')}</a></div><div class="cv-editorial-media">{img('E6', T('La guida ospiti di Vatican Glamorous sullo smartphone', 'The Vatican Glamorous guest guide on a smartphone'))}</div></div></section>
{cta(T('La tua base in Vaticano', 'Your base at the Vatican'), '', T('Verifica le date', 'Check dates'))}
  </main>

''' + footer()

def info():
    title = T('Info e regole | Vatican Glamorous · Passeggiata del Gelsomino', 'Info &amp; house rules | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Contatti, regole della casa e informazioni utili per il soggiorno a Vatican Glamorous, Via S. Telesforo, Roma.', 'Contacts, house rules and useful information for your stay at Vatican Glamorous, Via S. Telesforo, Rome.')
    return head(title, desc, 'I01') + header() + f'''
  <main>
{page_hero('I1', T('Soggiorno luminoso di Vatican Glamorous', 'Bright living room at Vatican Glamorous'), T('Contatti · Regole · Collegamenti utili', 'Contacts · Rules · Useful links'), T('Informazioni', 'Information'), T('Tutto ciò che serve prima dell’arrivo e durante il soggiorno.', 'Everything you need before arrival and during your stay.'))}
<section class="cv-section cream"><div class="cv-wrap">{centered('Vatican Glamorous', T('Contatti e risorse', 'Contacts and resources'))}<div class="cv-info-grid">
<article class="cv-info-card"><h3>{T('Contatti', 'Contact')}</h3><p>Via S. Telesforo, Roma</p><a href="tel:{PHONE}">{PHONE_TXT}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WA}" target="_blank" rel="noopener">{T('Scrivi su WhatsApp', 'Message us on WhatsApp')}</a><a href="{MAPS}" target="_blank" rel="noopener">{T('Apri le indicazioni', 'Get directions')}</a></article>
<article class="cv-info-card"><h3>{T('Documenti', 'Documents')}</h3><a href="{GUIDE}" target="_blank" rel="noopener">{T('Guida ospiti', 'Guest guide')}</a><p>Vatican Glamorous · Passeggiata del Gelsomino<br>CIN {CIN}</p></article>
<article class="cv-info-card"><h3>{T('Informazioni essenziali', 'Essentials')}</h3><ul><li>{T('Soggiorno minimo: 2 notti', 'Minimum stay: 2 nights')}</li><li>{T('Ospita comodamente fino a 4 persone', 'Comfortably sleeps up to 4 guests')}</li><li>{T('Indica il numero esatto di adulti e bambini al momento della prenotazione', 'Please state the exact number of adults and children when booking')}</li><li>{T('Animali di piccola taglia ammessi', 'Small pets welcome')}</li><li>{T('Vietato fumare all’interno', 'No smoking indoors')}</li><li>{T('Orari di check-in e check-out: [da completare]', 'Check-in and check-out times: [to be completed]')}</li></ul></article>
<article class="cv-info-card"><h3>{T('Servizi e soggiorno', 'Services')}</h3><ul><li>{T('Biancheria, asciugamani e kit bagno inclusi', 'Bed linen, towels and toiletries included')}</li><li>{T('Posto auto gratuito', 'Free parking')}</li><li>Wi‑Fi</li><li>{T('Smart Monitor e app streaming', 'Smart monitors and streaming apps')}</li><li>{T('Aria condizionata', 'Air conditioning')}</li><li>{T('Lavastoviglie e lavasciuga', 'Dishwasher and washer-dryer')}</li></ul></article>
<article class="cv-info-card"><h3>{T('Servizi fotografici', 'Photo shoots')}</h3><p>{T('Per set fotografici, riprese e soggiorni di lavoro contattaci per un’offerta personalizzata.', 'For photo shoots, filming and business stays, contact us for a tailored offer.')}</p><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></article>
<article class="cv-info-card"><h3>Privacy</h3><p>{T('I dati degli ospiti sono usati solo per la registrazione obbligatoria presso la Polizia di Stato (AlloggiatiWEB) e per l’invio dei codici di accesso. Non sono diffusi né usati per altri scopi.', 'Guest data is used only for the mandatory registration with the Police (AlloggiatiWEB) and for sending access codes. It is not disclosed or used for any other purpose.')}</p><a href="{link('privacy')}">{T('Leggi l’informativa completa', 'Read the full policy')}</a></article>
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
    title = T('Privacy e cookie policy | Vatican Glamorous · Passeggiata del Gelsomino', 'Privacy and cookie policy | Vatican Glamorous · Passeggiata del Gelsomino')
    desc = T('Privacy e cookie policy della Casa Vacanze Vatican Glamorous – Passeggiata del Gelsomino.', 'Privacy and cookie policy of the Vatican Glamorous – Passeggiata del Gelsomino Holiday Home.')
    PM = EMAIL
    if LANG == 'it':
        body = f'''<h2>Privacy e cookie policy Casa Vacanze Vatican Glamorous – Passeggiata del Gelsomino</h2>
<p>La presente informativa viene resa ai sensi del Reg. (UE) 2016/679 del 27/04/2016 relativo alla protezione delle persone fisiche con riguardo al trattamento dei dati personali (GDPR), e contiene informazioni sul trattamento dei dati personali che vengono raccolti dalla Casa Vacanze Passeggiata del Gelsomino e ne descrive le modalità di utilizzo.</p>
<p>In ogni caso tutti i dati acquisiti verranno trattati nel rispetto del GDPR, nonché secondo i canoni di riservatezza connaturati allo svolgimento dell’attività.</p>
<p>I dati personali potranno essere messi a disposizione dell’Autorità Giudiziaria e/o delle Forze di Polizia, dietro loro specifica richiesta, per ottemperare a requisiti legali o normativi ovvero ai fini dell’individuazione degli autori di eventuali fatti illeciti commessi a danno della Casa Vacanze.</p>
<p>Il trattamento sarà svolto preferibilmente in via elettronica con l’ausilio di strumenti informatici. In particolare, potrà essere inviato un messaggio di testo sul proprio cellulare per poter riempire in autonomia un modulo informatizzato, che sarà automaticamente inviato alle Forze di Polizia dopo il controllo di correttezza dei dati, con la finalità di registrare la vostra presenza; oppure gli stessi dati personali potranno essere raccolti attraverso cellulare al momento dell’arrivo da parte di personale dedicato, oppure potranno essere raccolti su un modulo cartaceo.</p>
<h2>Natura dei dati personali, finalità e destinatari del trattamento</h2>
<p>I dati personali raccolti presso l’interessato saranno trattati per la sola comunicazione alle Autorità di Polizia (portale AlloggiatiWEB) circa la propria presenza in loco, oppure per l’invio delle credenziali di accesso alle serrature elettroniche della Casa Vacanze. Gli stessi dati non saranno trattenuti o registrati per altri motivi. I dati personali non saranno oggetto di diffusione, se non imposta da norme di legge oppure espressamente autorizzata.</p>
<h2>Conservazione dei dati</h2>
<p>Tenuto conto degli scopi per cui sono stati raccolti, dell’adempimento degli obblighi di legge ovvero della tutela dei diritti del titolare, tali dati saranno conservati per un periodo non superiore a quello necessario e comunque per un periodo in linea con il termine consentito dalla legge vigente.</p>
<p>Con specifico riferimento all’attività di videosorveglianza, la informiamo che le immagini personali raccolte saranno conservate per non più di 24 ore, e che le stesse non potranno essere diffuse o comunicate a terzi salvo che per esigenze di polizia o di giustizia.</p>
<h2>Sito web e cookie</h2>
<p>Questo sito non utilizza cookie di profilazione né strumenti di statistica o pubblicità. Le prenotazioni si completano su piattaforme esterne (Direct-book, Airbnb, Booking.com), che applicano le proprie informative.</p>
<h2>Titolare del trattamento</h2>
<p>Per qualsiasi ulteriore informazione potrà rivolgersi al Titolare del trattamento, Casa Vacanze Passeggiata del Gelsomino (Via S. Telesforo, Roma – CIN {CIN}), tramite email: <a href="mailto:{PM}">{PM}</a>. Ad esso potrà rivolgersi per far valere i suoi diritti e in particolare per accedere ai suoi dati personali, per richiederne la rettifica, la cancellazione o la portabilità, la limitazione del trattamento o per opporsi ad esso. Nel contattare il Titolare del trattamento, dovrà accertarsi di includere il proprio nome, indirizzo email, indirizzo postale e numero di telefono, per essere sicuro che la sua richiesta possa essere gestita correttamente. Resta salvo il diritto di proporre reclamo al Garante per la protezione dei dati personali.</p>
<h2>Accettazione</h2>
<p>Visitando il sito web di Vatican Glamorous – Passeggiata del Gelsomino lei conferma di avere letto e compreso la presente informativa.</p>'''
    else:
        body = f'''<h2>Privacy and cookie policy of the Vatican Glamorous – Passeggiata del Gelsomino Holiday Home</h2>
<p>This information is provided pursuant to Reg. (EU) 2016/679 of 27/04/2016 on the protection of individuals with regard to the processing of personal data (GDPR) and contains information on the processing of personal data collected by the Passeggiata del Gelsomino Holiday Home, describing how it is used.</p>
<p>In any case, all the data acquired will be processed in compliance with the GDPR, as well as according to the standards of confidentiality inherent in the performance of the activity.</p>
<p>Personal data may be made available to the Judicial Authority and/or the Police Forces, upon their specific request, to comply with legal or regulatory requirements or for the purpose of identifying the authors of any unlawful acts committed to the detriment of the Holiday Home.</p>
<p>Processing will preferably be carried out electronically with the help of IT tools. In particular, a text message may be sent to your mobile phone so that you can fill in a form yourself, which will be automatically sent to the police after the data has been checked, in order to record your presence; alternatively, the same personal data may be collected on a mobile phone upon arrival by dedicated staff, or on a paper form.</p>
<h2>Nature of personal data, purposes and recipients of processing</h2>
<p>The personal data collected from the data subject will be processed only for communication to the Police Authorities (AlloggiatiWEB portal) about your presence on site, or for sending access credentials to the electronic locks of the Holiday Home. The same data will not be retained or recorded for other reasons. Personal data will not be disseminated, unless required by law or expressly authorised.</p>
<h2>Data retention</h2>
<p>Considering the purposes for which they were collected, the fulfilment of legal obligations or the protection of the rights of the owner, such data will be kept for a period not exceeding that necessary and in any case for a period in line with the term allowed by current law.</p>
<p>With specific reference to video surveillance, we inform you that the personal images collected will be kept for no more than 24 hours, and that they will not be disseminated or communicated to third parties except for police or justice needs.</p>
<h2>Website and cookies</h2>
<p>This website uses no profiling cookies and no analytics or advertising tools. Bookings are completed on external platforms (Direct-book, Airbnb, Booking.com), which apply their own privacy policies.</p>
<h2>Data controller</h2>
<p>For any further information you can contact the Data Controller, Passeggiata del Gelsomino Holiday Home (Via S. Telesforo, Rome – CIN {CIN}), by email: <a href="mailto:{PM}">{PM}</a>. You can contact the Data Controller to exercise your rights, in particular to access your personal data, to request its rectification, erasure or portability, restriction of processing, or to object to it. Please include your name, email address, postal address and telephone number so that your request can be properly handled. You also have the right to lodge a complaint with the Italian Data Protection Authority (Garante per la protezione dei dati personali).</p>
<h2>Acceptance</h2>
<p>By visiting the Vatican Glamorous – Passeggiata del Gelsomino website you confirm that you have read and understood this statement.</p>'''
    return head(title, desc) + header() + f'''
  <main>
{page_hero('P1', T('Soggiorno di Vatican Glamorous', 'Vatican Glamorous living room'), T('Privacy · Cookie', 'Privacy · Cookies'), 'Privacy', T('Privacy e cookie policy della Casa Vacanze.', 'Privacy and cookie policy of the Holiday Home.'))}
<section class="cv-section cream"><div class="cv-wrap cv-legal-text">
{body}
</div></section>
  </main>

''' + footer()


BUILD = {'home': home, 'apt': apt, 'rooms': rooms, 'rome': rome, 'exp': exp, 'info': info, 'book': book, 'privacy': privacy}

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
<meta property="og:type" content="website"><meta property="og:site_name" content="Vatican Glamorous · Passeggiata del Gelsomino">
<meta property="og:title" content="Vatican Glamorous · Passeggiata del Gelsomino">
<meta property="og:description" content="Casa vacanze di lusso a 200 m da San Pietro, Roma · Luxury holiday home 200 m from St. Peter’s, Rome.">
<meta property="og:url" content="https://www.vaticanglamorous.com/">
<meta property="og:image" content="'''+og_image('H13')+'''">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Vatican Glamorous – Passeggiata del Gelsomino">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="'''+og_image('H13')+'''">
<link rel="canonical" href="https://www.vaticanglamorous.com/it/">
<link rel="alternate" hreflang="it" href="https://www.vaticanglamorous.com/it/"><link rel="alternate" hreflang="en" href="https://www.vaticanglamorous.com/en/">
<script>location.replace(((navigator.language||'it').toLowerCase().indexOf('it')===0?'it/':'en/')+location.search);</script>
<meta http-equiv="refresh" content="1; url=it/">
</head><body><p><a href="it/">Italiano</a> · <a href="en/">English</a></p></body></html>
''')
import datetime
today = datetime.date.today().isoformat()
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for key in BUILD:
    for lg in ('it', 'en'):
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{a}" href="{DOMAIN}/{slug(key, a)}"/>' for a in ('it', 'en')) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}/{slug(key, "en")}"/>'
        pr = '1.0' if key == 'home' else ('0.3' if key == 'privacy' else '0.8')
        sm.append(f'  <url><loc>{DOMAIN}/{slug(key, lg)}</loc><lastmod>{today}</lastmod><priority>{pr}</priority>{alts}</url>')
sm.append('</urlset>')
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
# vecchi indirizzi del Google Site: rimandano alla pagina nuova corrispondente
OLD = {'eng': 'en/', 'book-your-stay': 'en/book/', 'pilgrim-stay': 'en/rome-vatican/#pilgrims', 'holiday-home-vatican-pilgrims': 'en/rome-vatican/#pilgrims', 'tours-events': 'en/experiences/', 'welcomebook': GUIDE}
for old, new in OLD.items():
    os.makedirs(os.path.join(OUT, old), exist_ok=True)
    target = new if new.startswith('http') else '../' + new
    canon = new if new.startswith('http') else f'{DOMAIN}/{new.split("#")[0]}'
    open(os.path.join(OUT, old, 'index.html'), 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><title>Vatican Glamorous · Passeggiata del Gelsomino</title><meta name="robots" content="noindex"><link rel="canonical" href="{canon}"><meta http-equiv="refresh" content="0; url={target}"></head><body><a href="{target}">Vatican Glamorous</a></body></html>')
# pagina 404
open(os.path.join(OUT, '404.html'), 'w').write('''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pagina non trovata · Vatican Glamorous</title><meta name="robots" content="noindex"><style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#fbf8f0;color:#123e5b;font-family:Georgia,serif;text-align:center;padding:24px}a{color:#a8801f;font-family:Arial,sans-serif;font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:.8rem;margin:0 10px}</style></head><body><div><h1>Vatican Glamorous</h1><p>Pagina non trovata · Page not found</p><p><a href="/it/">Italiano</a><a href="/en/">English</a></p></div></body></html>''')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(OUT, '.nojekyll'), 'w').write('')
print('ok')
