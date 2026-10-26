#!/usr/bin/env python3
"""
Global Chef League — static site generator.

You do NOT need to run this to publish the site: every page is already built.
Run it only if you'd rather edit the settings, chefs, or events below once
and regenerate all pages:

    python3 _build/build.py

It rewrites the .html files in the site folder. Anything you hand-edited in
those .html files will be overwritten, so pick one way of editing and stick
with it.
"""
import html, os, json
from pathlib import Path

# ============================================================
# 1. SETTINGS — change these
# ============================================================
SITE_URL      = "https://globalchefleague.com"    # used for canonical links + sitemap
STRIPE_LINK   = "https://buy.stripe.com/aFa4gB5Kd0nX3OP5Y89ws02"
LANDING_MODE  = True   # True = recruitment landing page only (pre-launch). False = full 9-page site.
FORM_CONTACT  = "https://formspree.io/f/REPLACE_CONTACT_FORM_ID"
FORM_PROFILE  = "https://formspree.io/f/REPLACE_PROFILE_FORM_ID"
CONTACT_EMAIL = "chefbattle@hoptoit.events"
BASE_PATH     = "/"   # site root path. "/" for a custom domain (globalchefleague.com).
                      # For a github.io project URL use "/REPO-NAME/". Only the 404 page uses this.
YEAR          = "2026"

# ============================================================
# 2. CONTENT DATA
# ============================================================
SERVICES = ["Private dining", "Catering and special events", "Cooking classes", "Corporate events", "Culinary experiences"]
ROLES = ["League Chef", "Chapter President", "League Champion"]
TOPICS = ["League Chef membership", "Chef profiles", "Competitions", "Chapters", "Partnerships"]
COUNTRIES = ["United States", "Canada", "Mexico", "United Kingdom", "Other"]

# Sample chefs — illustrative only. Replace with real members.
# primary_role: "League Chef" or "Chapter President". achievements: ["League Champion"] etc.
CHEFS = [
    dict(slug="james-rivera", no="01", name="James Rivera", city="Los Angeles, California", region="California",
         primary_role="League Chef", achievements=[], titles=[], chapter="",
         specialty="Modern Mexican", rate="From $95/guest", stat_rate="$95 / guest", area="Greater Los Angeles",
         bio="James grew up cooking in his family's taquería in Boyle Heights and went on to run kitchens across Los Angeles. Today he cooks modern Mexican tasting menus for private dinners and small events, built around heirloom corn, wood-grilled proteins and salsas made to order.",
         services=[("Private dining", "From $95/guest"), ("Catering and special events", "From $65/guest"), ("Cooking classes", "From $80/person")],
         specialties=["Modern Mexican", "Heirloom corn", "Wood-fired", "Tasting menus"],
         email="james@example.com", phone="", website="#", instagram="#", booking=""),
    dict(slug="maria-santos", no="02", name="Maria Santos", city="Miami, Florida Chapter", region="Florida",
         primary_role="Chapter President", achievements=[], titles=[], chapter="Miami",
         specialty="Latin Caribbean", rate="From $85/guest", stat_rate="$85 / guest", area="South Florida",
         bio="Maria spent twelve years running banquet kitchens on Miami Beach before launching her own catering company. Her menus pull from her Cuban and Puerto Rican roots, cooked over live fire for groups of ten to four hundred. As Miami Chapter President she hosts the city's Chef Battle qualifiers.",
         services=[("Catering and special events", "From $85/guest"), ("Private dining", "From $140/guest"), ("Corporate events", "Contact for Pricing"), ("Culinary experiences", "Contact for Pricing")],
         specialties=["Cuban", "Puerto Rican", "Live-fire", "Seafood", "Large-format events"],
         email="maria@example.com", phone="", website="#", instagram="#", booking="#"),
    dict(slug="darnell-brooks", no="03", name="Darnell Brooks", city="Chicago, Illinois", region="Illinois",
         primary_role="League Chef", achievements=["League Champion"], titles=["Chicago Chef Battle Champion"], chapter="",
         specialty="Southern, Live-fire", rate="Contact for Pricing", stat_rate="Contact for Pricing", area="Chicagoland",
         bio="Darnell cooks Southern food the long way: whole-hog smoke, cast iron and slow braises. After years on the line in Chicago's West Loop he started a live-fire catering business, and he took the Chicago Chef Battle title on the strength of a smoked short rib nobody has stopped talking about.",
         services=[("Catering and special events", "Contact for Pricing"), ("Corporate events", "Contact for Pricing"), ("Culinary experiences", "Contact for Pricing")],
         specialties=["Southern", "Live-fire", "Smoked meats", "Cast iron"],
         email="darnell@example.com", phone="", website="#", instagram="#", booking=""),
    dict(slug="aiko-tanaka", no="04", name="Aiko Tanaka", city="Vancouver, Canada", region="British Columbia",
         primary_role="League Chef", achievements=[], titles=[], chapter="",
         specialty="Japanese, Plant-based", rate="From $120/class", stat_rate="$120 / class", area="Metro Vancouver",
         bio="Aiko trained in Osaka before moving to Vancouver, where she now teaches hands-on Japanese cooking classes with a plant-based focus. Her classes cover dashi, knife work and seasonal vegetable dishes, and she cooks private omakase-style dinners for small groups.",
         services=[("Cooking classes", "From $120/class"), ("Private dining", "From $150/guest"), ("Culinary experiences", "Contact for Pricing")],
         specialties=["Japanese", "Plant-based", "Knife skills", "Seasonal"],
         email="aiko@example.com", phone="", website="#", instagram="#", booking="#"),
    dict(slug="priya-nair", no="05", name="Priya Nair", city="London, United Kingdom", region="London",
         primary_role="League Chef", achievements=[], titles=[], chapter="",
         specialty="South Indian", rate="From £70/guest", stat_rate="£70 / guest", area="Greater London",
         bio="Priya cooks the South Indian food she grew up with in Kerala: coconut curries, fresh dosa and seafood moilee. She runs supper clubs across London and caters weddings and corporate events with menus built around regional spice blends she grinds herself.",
         services=[("Private dining", "From £70/guest"), ("Catering and special events", "From £45/guest"), ("Corporate events", "Contact for Pricing")],
         specialties=["South Indian", "Kerala", "Seafood", "Supper clubs"],
         email="priya@example.com", phone="", website="#", instagram="#", booking=""),
    dict(slug="luca-bianchi", no="06", name="Luca Bianchi", city="Pasadena, California", region="California",
         primary_role="League Chef", achievements=[], titles=[], chapter="",
         specialty="Italian, Fresh pasta", rate="From $110/guest", stat_rate="$110 / guest", area="San Gabriel Valley",
         bio="Luca learned to roll pasta in his grandmother's kitchen in Bologna and has been doing it by hand ever since. He cooks private Italian dinners across the San Gabriel Valley and teaches fresh-pasta classes for groups, couples and corporate team events.",
         services=[("Private dining", "From $110/guest"), ("Cooking classes", "From $95/person"), ("Corporate events", "Contact for Pricing")],
         specialties=["Italian", "Fresh pasta", "Emilia-Romagna", "Hand-rolled"],
         email="luca@example.com", phone="", website="#", instagram="#", booking="#"),
]
# Which chef is featured in the home hero card
FEATURED = "maria-santos"

# Sample events — replace with real dates. apply: link for the Apply button.
EVENTS = [
    dict(date="NOV 14", short="Nov 14", city="Pasadena", place="Pasadena, California", stage="City Battle", status="Applications open", apply="contact/?topic=Competitions"),
    dict(date="DEC 05", short="Dec 05", city="Las Vegas", place="Las Vegas, Nevada", stage="City Battle", status="Applications open", apply="contact/?topic=Competitions"),
    dict(date="JAN 23", short="Jan 23", city="Miami", place="Miami, Florida", stage="City Battle", status="Opening soon", apply="contact/?topic=Competitions"),
    dict(date="MAR 06", short="Mar 06", city="Chicago", place="Chicago, Illinois", stage="Regional Showdown", status="Qualifiers only", apply="contact/?topic=Competitions"),
]

PILLARS = [
    ("01", "Compete", "Take on talented chefs in official Chef Battle competitions, with the opportunity to advance toward the World Chef Cup. No additional competition entry fees for members."),
    ("02", "Get Discovered", "Create your own League Chef profile to showcase your experience, specialties, and culinary services."),
    ("03", "Get Booked", "Promote your rates and contact information so customers can reach you directly. No booking commissions or middlemen."),
]
PATH = [("01", "Compete locally", "Chef Battle city events", ""), ("02", "Advance regionally", "Chef Battle regional showdowns", ""), ("03", "Qualify for the World Battle", "World Chef Cup", "gold")]
INCLUDES = [
    ("01", "Compete in Chef Battle", "Apply to compete in official Chef Battle events around the world without additional competition entry fees. Competition spots are limited and selection is not guaranteed."),
    ("02", "Get Your Own League Chef Profile", "Showcase your experience, photos, specialties, and culinary services on your own public profile."),
    ("03", "Promote Your Services", "List your rates and contact information for private dining, catering, cooking classes, and more."),
    ("04", "Keep What You Earn", "Customers contact and book you directly. Global Chef League doesn't take a commission."),
    ("05", "Work Toward the World Chef Cup", "Compete for recognition and the opportunity to qualify for the World Battle."),
    ("06", "Stay Connected", "Get updates about upcoming competitions, league news, and opportunities for League Chefs."),
]
GLANCE = [("Annual membership", "$25/year", True), ("Membership title", "League Chef", False), ("Chef Battle entry fees", "Free for active members", True),
          ("Public chef profile", "Included", False), ("Promote culinary services", "Included", False), ("Booking commissions", "0%", True),
          ("Chapter President designation", "By appointment", False), ("League Champion recognition", "Earned through competition", False)]
FAQS = [
    ("Who can become a League Chef?", "Membership is open to professional chefs, private chefs, caterers, culinary students, and aspiring chefs. Individual competitions may have additional eligibility requirements."),
    ("Do I need to be a League Chef to compete in Chef Battle?", "Yes. Active Global Chef League membership is required to compete in official Chef Battle competitions."),
    ("Is there an additional competition entry fee?", "No. Active League Chefs do not pay additional Chef Battle competition entry fees. Travel, accommodations, and personal expenses are not included."),
    ("Can I promote my culinary services?", "Yes. Your membership includes a public League Chef profile where you can showcase your experience, services, rates, and contact information."),
    ("Does Global Chef League take a commission on bookings?", "No. Customers contact you directly, and you manage your own bookings and payments."),
    ("Will I receive guaranteed bookings?", "No. Your profile makes it easier for potential customers to discover you, but bookings are not guaranteed."),
    ("What is a Chapter President?", "Chapter Presidents are designated local leaders who help grow Global Chef League and support Chef Battle competitions in their markets."),
    ("What is a League Champion?", "League Champion is a recognition given to chefs who have earned an official championship title through a recognized competition."),
    ("Does membership renew automatically?", "Yes. Membership renews annually unless canceled before the next renewal date."),
    ("Can I cancel my membership?", "Yes. You can cancel future renewals through the subscription management link provided. Your membership remains active through the paid term, subject to the Membership Terms."),
]
ROLE_CARDS = [
    ("League Chef", "", "League Chefs", "The heart of Global Chef League. Culinary professionals who showcase their skills, promote their services, and participate in the league."),
    ("Chapter President", "navy", "Chapter Presidents", "Local leaders who help bring chefs together, grow the league, and support competitions in their communities."),
    ("League Champion", "gold", "League Champions", "Chefs recognized for earning official championship titles through competition."),
]

CTA_JOIN = "Become a League Chef — $25/Year"
SUPPORT = "Join Global Chef League for just $25 a year. Create your chef profile, promote your services, and apply to compete in Chef Battle events without additional entry fees."

# ============================================================
# 3. TEMPLATE HELPERS
# ============================================================
ROOT = Path(__file__).resolve().parent.parent
e = lambda s: html.escape(str(s), quote=True)

def badge(label, on_navy=False):
    if label == "Chapter President":
        cls = "badge--ink-inv" if on_navy else "badge--ink"
    elif label == "League Champion":
        cls = "badge--award"
    else:
        cls = "badge--outline-inv" if on_navy else "badge--outline"
    return f'<span class="badge {cls}">{e(label)}</span>'

def chef_badges(c, on_navy=False):
    labels = [c["primary_role"]] + c["achievements"]
    return '<div class="badges">' + "".join(badge(l, on_navy) for l in labels) + "</div>"

# Placeholder photos (free Unsplash License, loaded from Unsplash's CDN). Replace before launch.
UNSPLASH = "https://images.unsplash.com/{id}?auto=format&fit=crop&w={w}&q=70"
PHOTOS = {
    "profile":   "photo-1697898109582-40f15c65f174",   # chef in chef's hat holding a plated dish
    "dish":      "photo-1467003909585-2f8a72700288",   # salmon fillet with salsa
    "event1":    "photo-1555244162-803834f70033",      # catering buffet with chafing dishes
    "event2":    "photo-1503453776591-b4548af666a2",   # chef garnishing a dish
}

def ph(label, light=False, extra="", photo=None, w=900, pos="center"):
    img = ""
    if photo and PHOTOS.get(photo):
        src = UNSPLASH.format(id=PHOTOS[photo], w=w)
        img = f'<img src="{src}" alt="{e(label)}" loading="lazy" style="object-position:{pos}">'
    return f'<div class="ph{" ph--light" if light else ""}" {extra}>{e(label)}{img}</div>'

def head_block(title, rule_cls="rule", eyebrow=None, h="h2", hcls="h2", extra=""):
    eb = f'<div class="eyebrow">{e(eyebrow)}</div>' if eyebrow else ""
    return f'<div class="section-head">{eb}<{h} class="{hcls}">{title}<span class="dot">.</span></{h}><div class="{rule_cls}"></div>{extra}</div>'

def btn(label, href, kind="primary", size="", block=False, attrs=""):
    cls = f"btn btn--{kind}" + (f" btn--{size}" if size else "") + (" btn--block" if block else "")
    return f'<a class="{cls}" href="{e(href)}" {attrs}>{e(label)}</a>'

NAV = [("Find a Chef", "chefs/"), ("Competitions", "competitions/"), ("Membership", "membership/"), ("About", "about/")]

def page(path, title, desc, body, active=None, noindex=False):
    minimal = LANDING_MODE
    depth = path.count("/")  # "chefs/maria-santos/index.html" -> 2
    r = BASE_PATH if path == "404.html" else "../" * depth
    links = "".join(
        f'<a class="nav-link" href="{r}{href}"{" aria-current=\"page\"" if label == active else ""}>{label}</a>' for label, href in NAV)
    canonical = SITE_URL.rstrip("/") + "/" + path.replace("index.html", "")
    full_title = title if title.startswith("Global Chef League") else f"{title} | Global Chef League"
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    body = body.replace("{R}", r)
    if minimal:
        header = f'''<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{r or './'}" aria-label="Global Chef League home"><img src="{r}assets/img/gcl-logo-horizontal.svg" alt="Global Chef League" width="285" height="28"></a>
    <div class="head-cta"><span class="head-price">League Chef · $25/Year</span><a class="btn btn--primary btn--sm" href="{e(STRIPE_LINK)}">Join Now</a></div>
  </div>
</header>'''
        footer = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid foot-grid--min">
      <div><img src="{r}assets/img/gcl-logo-stacked-white.svg" alt="Global Chef League" width="115" height="96"><p class="foot-tag">Compete. Get Discovered. Get Booked.</p></div>
      <div class="foot-col"><div class="eyebrow">Join the League</div><a href="{e(STRIPE_LINK)}">Become a League Chef — $25/Year</a><a href="{r}#profile">See a Sample Profile</a><a href="{r}#faq">FAQ</a></div>
      <div class="foot-col"><div class="eyebrow">Questions</div><a href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a><span>Full site coming soon</span></div>
    </div>
    <div class="foot-bottom"><span>© <span id="year">{YEAR}</span> Global Chef League</span><span>GlobalChefLeague.com</span></div>
  </div>
</footer>'''
    else:
        header = f'''<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{r or './'}" aria-label="Global Chef League home"><img src="{r}assets/img/gcl-logo-horizontal.svg" alt="Global Chef League" width="285" height="28"></a>
    <button class="nav-toggle" aria-controls="site-nav" aria-expanded="false" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {links}
      <a class="btn btn--primary btn--sm" href="{r}membership/">Join Now</a>
    </nav>
  </div>
</header>'''
        footer = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div><img src="{r}assets/img/gcl-logo-stacked-white.svg" alt="Global Chef League" width="115" height="96"><p class="foot-tag">Compete. Get Discovered. Get Booked.</p></div>
      <div class="foot-col"><div class="eyebrow">Explore</div><a href="{r}chefs/">Find a Chef</a><a href="{r}competitions/">Competitions</a><a href="{r}membership/">Membership</a><a href="{r}about/">About</a><a href="{r}contact/">Contact</a></div>
      <div class="foot-col"><div class="eyebrow">Legal</div><a href="{r}membership-terms/">Membership Terms</a><a href="{r}privacy/">Privacy Policy</a><a href="{r}terms/">Website Terms</a><a href="{r}directory-disclaimer/">Directory Disclaimer</a></div>
      <div class="foot-col"><div class="eyebrow">The League</div><a href="{r}competitions/">Chef Battle</a><a href="{r}competitions/#world-chef-cup">World Chef Cup</a><span>ChefCon</span></div>
    </div>
    <div class="foot-bottom"><span>© <span id="year">{YEAR}</span> Global Chef League</span><span>GlobalChefLeague.com</span></div>
  </div>
</footer>'''
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{e(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Global Chef League">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(canonical)}">
<meta name="theme-color" content="#0F1E3C">
<link rel="icon" href="{r}assets/img/gcl-icon.svg" type="image/svg+xml">
<link rel="preload" href="{r}assets/fonts/montserrat-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}assets/fonts/barlow-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/css/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header}
<main id="main">
{body}
</main>
{footer}
<script src="{r}assets/js/site.js" defer></script>
</body>
</html>
"""
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    PAGES.append((path, noindex))

PAGES = []

def chef_by(slug):
    return next(c for c in CHEFS if c["slug"] == slug)

def options(items, placeholder, selected=""):
    o = f'<option value="">{e(placeholder)}</option>'
    return o + "".join(f'<option{" selected" if i == selected else ""}>{e(i)}</option>' for i in items)

# ============================================================
# 4. PAGES
# ============================================================
def home():
    f = chef_by(FEATURED)
    ticker = "".join(f'<a href="{{R}}competitions/#upcoming">{e(ev["short"])} <span class="city">· {e(ev["city"])}</span></a>' for ev in EVENTS)
    pillars = "".join(f'<div class="pillar"><div class="num">{n}</div><h3 class="h3">{e(t)}</h3><p>{e(b)}</p></div>' for n, t, b in PILLARS)
    cards = "".join(f'''<a class="chef-card" href="{{R}}chefs/{c["slug"]}/"><div class="photo">{ph("Chef photo", True)}<div class="ph-no">{c["no"]}</div></div><div class="info"><div class="name">Chef {e(c["name"])}</div><div class="muted">{e(c["city"])}</div>{chef_badges(c)}</div></a>''' for c in CHEFS[:4])
    path = "".join(f'<div class="path-step"><div class="num {g}">{n}</div><div class="t">{e(t)}</div><div class="s">{e(s)}</div></div>' for n, t, s, g in PATH)
    body = f'''
<section class="bg-navy hero">
  <div class="wrap hero-grid">
    <div class="stack-lg">
      <span class="badge badge--brand badge--capsule">League Chef Membership</span>
      <h1 class="h-hero">Compete.<br>Get Discovered.<br>Get Booked<span class="dot">.</span></h1>
      <p>Join Global Chef League as a League Chef to showcase your talent, promote your services, and compete in Chef Battle events around the world.</p>
      <div class="btn-row">{btn("Join for $25/Year", STRIPE_LINK, "primary", "lg")}{btn("Find a Chef", "{R}chefs/", "inverse", "lg")}</div>
    </div>
    <a class="feature-card" href="{{R}}chefs/{f["slug"]}/">
      <div class="ph" style="height:380px">League Chef portrait<div class="ph-no">{f["no"]}</div></div>
      <div class="info"><div class="name">Chef {e(f["name"])}</div><div class="muted">{e(f["city"])}</div><div class="badges">{badge(f["primary_role"])}{badge("League Chef") if f["primary_role"] != "League Chef" else ""}</div></div>
    </a>
  </div>
</section>
<div class="ticker" aria-label="Upcoming Chef Battle events"><div class="wrap"><span style="color:var(--red)">Up next</span>{ticker}</div></div>

<section class="section bg-bone">
  <div class="wrap">
    {head_block("More Opportunities for Chefs", eyebrow="Why Join")}
    <div class="grid g-3">{pillars}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="roster-head">
      <div class="stack"><div class="eyebrow">The Roster</div><h2 class="h2">Meet Our League Chefs<span class="dot">.</span></h2><div class="lead">Discover culinary talent from around the world.</div></div>
      <div class="stack-lg" style="gap:20px"><p>Explore chef profiles, browse services and rates, and connect directly with chefs for private dining, catering, cooking classes, and more.</p>{btn("Find a Chef", "{R}chefs/", "secondary")}</div>
    </div>
    <div class="grid g-4" style="gap:24px">{cards}</div>
    <p class="legal" style="margin-top:20px">Illustrative profiles; not actual GCL members.</p>
  </div>
</section>

<section class="section bg-navy">
  <div class="wrap split-72">
    <div class="stack" style="gap:20px">
      <div class="eyebrow">Chef Battle</div>
      <h2 class="h2">Take Your Skills to the Next Level<span class="dot">.</span></h2>
      <p style="font-size:18px">Chef Battle gives League Chefs the opportunity to compete, gain recognition, and work toward the World Chef Cup.</p>
      <p style="font-size:18px">Explore upcoming competitions and see where the next Chef Battle is happening.</p>
      {btn("Explore Competitions", "{R}competitions/")}
    </div>
    <div class="path-grid">{path}</div>
  </div>
</section>

<section class="section bg-bone">
  <div class="wrap join-grid">
    <div class="price-big" aria-label="$25 per year"><span class="cur">$</span><span class="amt">25</span><span class="per">/YEAR</span></div>
    <div class="stack" style="gap:18px">
      <div class="eyebrow">Just $25 Per Year</div>
      <h2 class="h2">Join Global Chef League<span class="dot">.</span></h2>
      <p class="measure" style="font-size:18px">{e(SUPPORT)}</p>
      {btn(CTA_JOIN, STRIPE_LINK, "primary", "lg")}
      <p class="legal measure">Competition participation is subject to eligibility, selection, and availability. Membership does not guarantee bookings or competition placement.</p>
    </div>
  </div>
</section>'''
    page("index.html", "Global Chef League — Compete. Get Discovered. Get Booked.",
         "Join Global Chef League as a League Chef for $25 a year. Showcase your talent, promote your culinary services, and compete in Chef Battle events.", body, active=None)

def landing():
    c = dict(chef_by("james-rivera"))
    # Landing version: no Chapter President references
    c.update(primary_role="League Chef", chapter="", city=c["city"].replace(" Chapter", ""),
             bio=c["bio"].replace(" As Miami Chapter President she hosts the city's Chef Battle qualifiers.", ""))
    first, rest = c["name"].split()[0], " ".join(c["name"].split()[1:])
    pillars = [
        ("01", "Get Discovered", "Your League Chef profile puts your photo, experience and specialties in the Global Chef League directory, so customers can find you by city, specialty and service."),
        ("02", "Promote Your Services", "Private dining, catering, cooking classes, corporate events. List what you offer and what you charge, priced your way."),
        ("03", "Get Booked Directly", "Customers contact you directly from your profile. No middlemen and no booking commissions. You keep what you earn."),
    ]
    pil = "".join(f'<div class="pillar"><div class="num">{n}</div><h3 class="h3">{e(t)}</h3><p>{e(b)}</p></div>' for n, t, b in pillars)
    order = ["02", "03", "04", "06", "01", "05"]
    incd = {n: (t, b) for n, t, b in INCLUDES}
    inc = "".join(f'<div class="inc"><div class="num">0{i+1}</div><div class="t">{e(incd[n][0])}</div><p>{e(incd[n][1])}</p></div>' for i, n in enumerate(order))
    glance = [("Public chef profile", "Included", False), ("Chef directory listing", "Included", False), ("Promote culinary services", "Included", False),
              ("Booking commissions", "0%", True), ("Annual membership", "$25/year", True), ("Membership title", "League Chef", False),
              ("Chef Battle entry fees", "Free for active members", True), ("League Champion recognition", "Earned through competition", False)]
    gl = "".join(f'<div class="glance-row"><span class="b">{e(b)}</span><span class="d{" hi" if hi else ""}">{e(d)}</span></div>' for b, d, hi in glance)
    faqs = [FAQS[3], FAQS[4], FAQS[5], FAQS[0],
            ("What goes on my profile?", "Your photo, a short bio, the services you offer with starting rates, your culinary specialties, a photo gallery, and how customers can reach you: email, phone, website, booking link and social media."),
            FAQS[1], FAQS[2], FAQS[8], FAQS[9]]
    fq = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    svcs = "".join(f'<div class="svc"><span class="n">{e(n)}</span><span class="r">{e(r)}</span></div>' for n, r in c["services"])
    specs = "".join(f'<span class="badge badge--wash">{e(x)}</span>' for x in c["specialties"])
    svc_tags = "".join(f'<span class="svc-tag">{e(x)}</span>' for x in SERVICES)
    steps = [("01", "Join for $25/Year", "Check out securely through Stripe. Your membership starts right away."),
             ("02", "Build Your Profile", "Add your photo, bio, services, rates, specialties and how customers can reach you."),
             ("03", "Get Listed & Get Booked", "We verify your membership and publish your profile in the League Chef directory.")]
    how = "".join(f'<div class="pillar"><div class="num">{n}</div><h3 class="h3">{e(t)}</h3><p>{e(b)}</p></div>' for n, t, b in steps)
    path = "".join(f'<div class="path-step"><div class="num {g}">{n}</div><div class="t">{e(t)}</div><div class="s">{e(x)}</div></div>' for n, t, x, g in PATH)
    body = f'''
<section class="bg-navy hero">
  <div class="wrap hero-grid">
    <div class="stack-lg">
      <span class="badge badge--brand badge--capsule">Now Accepting League Chef Profiles</span>
      <h1 class="h-hero">Get Discovered.<br>Get Booked<span class="dot">.</span></h1>
      <p>Promote yourself and your culinary services with a League Chef profile in the Global Chef League directory. Showcase your experience, list your services and rates, and let customers contact you directly, with no booking commissions.</p>
      <div class="btn-row">{btn("Join Now — $25/Year", STRIPE_LINK, "primary", "lg")}{btn("See a Sample Profile", "#profile", "inverse", "lg")}</div>
      <p class="legal">Secure checkout through Stripe. Renews yearly; cancel anytime.</p>
    </div>
    <div class="price-card">
      <div class="top"><span>League Chef Membership</span><span class="badge badge--brand">Annual</span></div>
      <div class="price-big" aria-label="$25 per year"><span class="cur">$</span><span class="amt">25</span><span class="per">/YEAR</span></div>
      <ul class="ticks">
        <li>Your own public chef profile</li>
        <li>Listed in the League Chef directory</li>
        <li>Promote your services and rates</li>
        <li>0% booking commissions</li>
        <li>Plus: Chef Battle with no entry fees</li>
      </ul>
      {btn("Join Now", STRIPE_LINK, "primary", "lg", block=True)}
    </div>
  </div>
</section>

<section class="svc-strip">
  <div class="wrap"><span class="label">Get found for</span>{svc_tags}</div>
</section>

<section class="section" id="profile" style="scroll-margin-top:76px">
  <div class="wrap">
    <div class="roster-head">
      <div class="stack"><div class="eyebrow">Your Profile</div><h2 class="h2">Your Profile. Your Business<span class="dot">.</span></h2><div class="rule"></div></div>
      <p style="font-size:18px">Every League Chef gets a public profile page in the Global Chef League directory. It works like your own chef website: your story, your services, your rates and your contact details in one shareable link. Here's what yours could look like.</p>
    </div>
    <div class="mock" aria-label="Sample League Chef profile">
      <div class="mock-bar"><span></span><span></span><span></span><div class="mock-url">globalchefleague.com/chefs/{c["slug"]}</div></div>
      <div class="mock-hero">
        <div class="mock-photo">{ph("Your profile photo", photo="profile", w=700, pos="center 20%")}<span class="pin">1</span></div>
        <div class="stack" style="gap:18px">
          <div class="crumbs">Find a Chef / {e(c["region"])}</div>
          <div class="badges">{badge("League Chef", True)}</div>
          <div class="mock-h1">Chef {e(first)}<br>{e(rest)}<span class="dot">.</span></div>
          <div class="profile-loc">{e(c["city"])}</div>
          <div class="stats"><div class="stat"><span class="label">Starting at</span><span class="v">{e(c["stat_rate"])}</span></div><div class="stat"><span class="label">Service area</span><span class="v">{e(c["area"])}</span></div><div class="stat"><span class="label">Specialty</span><span class="v">{e(c["specialty"])}</span></div></div>
        </div>
      </div>
      <div class="mock-body">
        <div>
          <div class="p-sec"><h2>About Me</h2><div class="rule rule--sm"></div><p>{e(c["bio"])}</p></div>
          <div class="p-sec"><h2>My Services <span class="pin pin--inline">2</span></h2><div class="rule rule--sm"></div><div class="svc-list">{svcs}</div></div>
          <div class="p-sec" style="margin-bottom:32px"><h2>Culinary Specialties</h2><div class="rule rule--sm"></div><div class="badges" style="gap:8px">{specs}</div></div>
          <div class="gallery mock-gallery">{ph("Signature dish", True, photo="dish", w=1000)}{ph("Event photo", True, photo="event1", w=600)}{ph("Event photo", True, photo="event2", w=600)}<span class="pin pin--gallery">3</span></div>
        </div>
        <div class="contact-card mock-card">
          <span class="pin pin--corner">4</span>
          <div class="eyebrow">Contact &amp; Bookings</div>
          <div class="t">Interested in working with Chef {e(c["name"])}?</div>
          <p>Contact the chef directly to discuss services, availability, and pricing.</p>
          <span class="btn btn--primary btn--lg btn--block" aria-hidden="true">Contact Chef</span>
          <div class="contact-links"><span>Website</span><span>Instagram</span><span>Booking Website</span></div>
          <p class="legal">This chef operates independently. All inquiries, bookings, payments, and service arrangements are handled directly with the chef.</p>
        </div>
      </div>
    </div>
    <div class="grid g-4 callouts">
      <div><span class="pin pin--inline">1</span><div class="t">Your photo &amp; story</div><p>A headshot and bio that show who you are, where you cook and what makes your food yours.</p></div>
      <div><span class="pin pin--inline">2</span><div class="t">Services &amp; rates</div><p>List each service with a starting rate, or "Contact for Pricing". You set your prices.</p></div>
      <div><span class="pin pin--inline">3</span><div class="t">Your best work</div><p>A gallery of signature dishes and events so customers can see what they're booking.</p></div>
      <div><span class="pin pin--inline">4</span><div class="t">Direct contact</div><p>Email, phone, website, Instagram and booking link. Customers reach you, not us.</p></div>
    </div>
    <p class="legal" style="margin-top:28px">Sample profile for illustration. Not an actual Global Chef League member.</p>
    <div style="margin-top:40px">{btn("Create Your Profile — $25/Year", STRIPE_LINK, "primary", "lg")}</div>
  </div>
</section>

<section class="section bg-bone">
  <div class="wrap">
    {head_block("Promote Yourself. Keep What You Earn", eyebrow="Why Join")}
    <div class="grid g-3">{pil}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head_block("How It Works", eyebrow="Three Steps")}
    <div class="grid g-3">{how}</div>
  </div>
</section>

<section class="section bg-bone">
  <div class="wrap">
    {head_block("Your League Chef Membership Includes", hcls="h2 h2--sm")}
    <div class="grid g-3" style="gap:48px 40px">{inc}</div>
  </div>
</section>

<section class="section bg-navy">
  <div class="wrap split-72">
    <div class="stack" style="gap:20px">
      <div class="eyebrow">Plus: Chef Battle</div>
      <h2 class="h2">Put Your Skills to the Test<span class="dot">.</span></h2>
      <p style="font-size:18px">Your membership also makes you eligible for Chef Battle, our live culinary competitions, with no additional entry fees. Compete locally, advance regionally, and qualify for the World Battle.</p>
    </div>
    <div class="path-grid">{path}</div>
  </div>
</section>

<section class="section">
  <div class="wrap side-grid">
    <div class="stack"><div class="eyebrow">Membership at a Glance</div><h2 class="h2 h2--sm">One Membership<span class="dot">.</span></h2><div class="rule"></div><p>Join Global Chef League for just $25 a year. Create your chef profile, promote your services, and get booked directly, plus apply to compete in Chef Battle events without additional entry fees.</p></div>
    <div class="glance"><div class="glance-row head"><span>Benefit</span><span>Details</span></div>{gl}</div>
  </div>
</section>

<section class="section--band bg-navy">
  <div class="wrap band-grid">
    <div class="stack" style="gap:14px">
      <h2 class="h2">Get Listed for $25/Year</h2>
      <p style="font-size:18px">Your own League Chef profile, your services and rates, and direct bookings with no commissions. One annual membership.</p>
      <p class="legal" style="margin-top:8px">Membership renews automatically each year unless canceled. Membership does not guarantee bookings. Competition participation is subject to eligibility, selection, and availability.</p>
    </div>
    {btn("Join Now", STRIPE_LINK, "primary", "lg")}
  </div>
</section>

<section class="section" id="faq" style="scroll-margin-top:76px">
  <div class="wrap side-grid">
    <div class="stack"><h2 class="h2 h2--sm">Frequently Asked Questions<span class="dot">.</span></h2><div class="rule"></div><p>Still have questions? Email <a href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a>.</p></div>
    <div class="faq">{fq}</div>
  </div>
</section>
<script type="application/ld+json">{faq_ld}</script>'''
    page("index.html", "Global Chef League — Promote Your Culinary Services | League Chef Directory",
         "Get discovered and get booked. Create a League Chef profile in the Global Chef League directory for $25 a year: showcase your experience, list your services and rates, and keep 100% of your bookings.", body)

def directory():
    rows = ""
    for c in CHEFS:
        roles = [c["primary_role"]] + c["achievements"]
        rows += f'''<div class="dir-row" data-name="{e(c["name"])}" data-city="{e(c["city"])}" data-specialty="{e(c["specialty"] + " " + " ".join(c["specialties"]))}" data-services="{e("|".join(s for s, _ in c["services"]))}" data-roles="{e("|".join(roles))}">
  <span class="dir-no">{c["no"]}</span>
  <div class="dir-chef"><div class="dir-thumb">{ph("", True)}</div><div><a class="dir-name" href="{{R}}chefs/{c["slug"]}/">Chef {e(c["name"])}</a>{chef_badges(c)}</div></div>
  <span class="dir-cell"><span class="k">Location</span>{e(c["city"])}</span>
  <span class="dir-cell"><span class="k">Specialty</span>{e(c["specialty"])}</span>
  <span class="dir-cell c-rate"><span class="k">Starting rate</span>{e(c["rate"])}</span>
  {btn("View Chef Profile", "{R}chefs/" + c["slug"] + "/", "secondary", "sm")}
</div>'''
    tags = "".join(f'<button type="button" class="badge badge--tag" data-service="{e(s)}" aria-pressed="false">{e(s)}</button>' for s in SERVICES)
    body = f'''
<section class="bg-navy page-hero page-hero--search">
  <div class="wrap stack" style="gap:22px">
    <div class="eyebrow">Discover Culinary Talent Near You.</div>
    <h1 class="h1">Find a League Chef<span class="dot">.</span></h1>
    <p>Looking for a private chef, caterer, or cooking instructor? Explore Global Chef League members, browse their services and rates, and contact chefs directly.</p>
  </div>
</section>
<section style="padding-bottom:96px">
  <div class="wrap">
    <form class="search-panel" id="dir-form" role="search">
      <div class="field"><label for="f-search">Search</label><input class="input" id="f-search" name="q" type="search" placeholder="Search by chef name, city, or specialty."></div>
      <div class="field"><label for="f-service">Service</label><select class="select" id="f-service" name="service">{options(SERVICES, "All services")}</select></div>
      <div class="field"><label for="f-role">Designation</label><select class="select" id="f-role" name="designation">{options(ROLES, "All chefs")}</select></div>
      <button class="btn btn--primary btn--lg" type="submit">Search</button>
    </form>
    <div class="filter-tags"><span class="label">Find chefs offering:</span>{tags}</div>
    <div class="dir-count">Explore Our League Chefs · <span id="dir-count-n">{len(CHEFS)} profiles</span></div>
    <div class="dir" id="directory">
      <div class="dir-row dir-head"><span>No.</span><span>Chef</span><span>Location</span><span>Specialty</span><span class="c-rate">Starting rate</span><span></span></div>
      {rows}
    </div>
    <p class="dir-empty" id="dir-empty">No chefs match that search yet. Try a different city, specialty, or service.</p>
    <p class="legal" style="margin-top:20px">Illustrative profiles; not actual GCL members.</p>
    <div class="cta-band" style="margin-top:72px">
      <div class="stack"><h2 class="h2">Are You a Chef?</h2><p style="font-size:18px">Join Global Chef League, create your own League Chef profile, and promote your services to potential customers.</p></div>
      {btn(CTA_JOIN, STRIPE_LINK, "primary", "lg")}
    </div>
    <p class="legal" style="margin-top:24px">Bookings and payments are arranged directly with each chef. Global Chef League does not manage or guarantee services.</p>
  </div>
</section>'''
    page("chefs/index.html", "Find a Chef", "Find a League Chef for private dining, catering, cooking classes, corporate events and culinary experiences. Contact chefs directly — no booking commissions.", body, active="Find a Chef")

def profile(c):
    first = c["name"].split()[0]
    rest = " ".join(c["name"].split()[1:])
    stats = [("Starting at", c["stat_rate"], "")]
    if c["area"]: stats.append(("Service area", c["area"], ""))
    if c["primary_role"] == "Chapter President" and c["chapter"]:
        stats.append(("Chapter", c["chapter"], ""))
    elif c["titles"]:
        stats.append(("Title", c["titles"][0], "gold sm"))
    stat_html = "".join(f'<div class="stat"><span class="label">{e(k)}</span><span class="v {g}">{e(v)}</span></div>' for k, v, g in stats)
    svcs = "".join(f'<div class="svc"><span class="n">{e(n)}</span><span class="r">{e(r)}</span></div>' for n, r in c["services"])
    specs = "".join(f'<span class="badge badge--wash">{e(s)}</span>' for s in c["specialties"])
    badges_hdr = "".join(badge(l, True) for l in [c["primary_role"]] + c["achievements"] + (["League Chef"] if c["primary_role"] != "League Chef" else []))
    if c["email"]:
        contact_href = f'mailto:{c["email"]}?subject=' + "Inquiry%20via%20Global%20Chef%20League"
    elif c["phone"]:
        contact_href = "tel:" + c["phone"]
    else:
        contact_href = c["booking"]
    links = []
    if c["website"]: links.append(f'<a href="{e(c["website"])}" rel="noopener">Website</a>')
    if c["instagram"]: links.append(f'<a href="{e(c["instagram"])}" rel="noopener">Instagram</a>')
    if c["booking"]: links.append(f'<a href="{e(c["booking"])}" rel="noopener">Booking Website</a>')
    titles = ""
    if c["titles"]:
        titles = '<div class="p-sec"><h2>Championship Titles</h2><div class="rule rule--sm"></div><div class="badges">' + "".join(f'<span class="badge badge--award" style="height:30px;padding:0 12px;font-size:13px">★ {e(t)}</span>' for t in c["titles"]) + "</div></div>"
    body = f'''
<section class="bg-navy profile-hero">
  <div class="wrap profile-grid">
    <div class="profile-photo">{ph("Profile photo")}</div>
    <div class="stack" style="gap:22px;padding-bottom:8px">
      <div class="crumbs"><a href="{{R}}chefs/">Find a Chef</a> / {e(c["region"])}</div>
      <div class="badges">{badges_hdr}</div>
      <h1 class="h-hero">Chef {e(first)}<br>{e(rest)}<span class="dot">.</span></h1>
      <div class="profile-loc">{e(c["city"])}</div>
      <div class="stats{" two" if len(stats) == 2 else ""}">{stat_html}</div>
    </div>
  </div>
</section>
<section class="profile-body">
  <div class="wrap profile-cols">
    <div>
      <p class="sample-note">Sample profile for layout. Not an actual Global Chef League member.</p>
      <div class="p-sec"><h2>About Me</h2><div class="rule rule--sm"></div><p>{e(c["bio"])}</p></div>
      {titles}
      <div class="p-sec"><h2>My Services</h2><div class="rule rule--sm"></div><div class="svc-list">{svcs}</div></div>
      <div class="p-sec"><h2>Culinary Specialties</h2><div class="rule rule--sm"></div><div class="badges" style="gap:8px">{specs}</div></div>
      <div class="gallery">{ph("Signature dish", True)}{ph("Event photo", True)}{ph("Event photo", True)}</div>
    </div>
    <aside class="contact-card">
      <div class="eyebrow">Contact &amp; Bookings</div>
      <div class="t">Interested in working with Chef {e(c["name"])}?</div>
      <p>Contact the chef directly to discuss services, availability, and pricing.</p>
      {btn("Contact Chef", contact_href, "primary", "lg", block=True)}
      {'<div class="contact-links">' + "".join(links) + '</div>' if links else ""}
      <p class="legal">This chef operates independently. All inquiries, bookings, payments, and service arrangements are handled directly with the chef.</p>
    </aside>
  </div>
</section>'''
    page(f"chefs/{c['slug']}/index.html", f"Chef {c['name']}", f"Chef {c['name']} — {c['specialty']} chef in {c['city']}. {c['rate']}. View services and contact the chef directly.", body, active="Find a Chef")

def competitions():
    rows = "".join(f'''<div class="ev-row">
  <span class="ev-date">{e(ev["date"])}</span>
  <div><span class="ev-name">Chef Battle {e(ev["city"])}</span><span class="muted">{e(ev["place"])}</span></div>
  <span class="dir-cell ev-stage">{e(ev["stage"])}</span>
  <span class="ev-status{" open" if ev["status"] == "Applications open" else ""}">{e(ev["status"])}</span>
  {btn("Apply", "{R}" + ev["apply"], "primary" if ev["status"] == "Applications open" else "secondary", "sm")}
</div>''' for ev in EVENTS)
    body = f'''
<section class="bg-navy page-hero">
  <div class="wrap stack" style="gap:22px">
    <div class="eyebrow">Chef Battle · World Chef Cup</div>
    <h1 class="h1">Ready to<br>Compete?</h1>
    <p>Put your skills to the test, take on other talented chefs, and compete for recognition on the road to the World Chef Cup.</p>
  </div>
</section>
<section class="section">
  <div class="wrap grid g-2" style="gap:56px">
    <div class="comp-card" id="chef-battle">
      <div class="photo" style="width:100%">{ph("Chef Battle — live service")}</div>
      <span class="badge badge--brand">Chef Battle</span>
      <h2 class="h2">Your City. Your Competition.</h2>
      <p>Chef Battle brings chefs together for live culinary competitions in cities around the world.</p>
      <p>Show off your skills, compete in front of judges and an audience, and earn the opportunity to advance.</p>
      {btn("Find a Competition", "#upcoming")}
    </div>
    <div class="comp-card" id="world-chef-cup">
      <div class="photo" style="width:100%">{ph("World Chef Cup — finals stage")}</div>
      <span class="badge badge--award">World Chef Cup</span>
      <h2 class="h2">The Global Stage Awaits.</h2>
      <p>The World Chef Cup brings qualifying chefs together to compete for international recognition and the championship title.</p>
      {btn("Learn More", "{R}about/", "secondary")}
    </div>
  </div>
</section>
<section class="section bg-bone" id="upcoming" style="scroll-margin-top:76px">
  <div class="wrap">
    <div class="roster-head">
      <div class="stack"><h2 class="h2">Upcoming Competitions<span class="dot">.</span></h2><p style="font-size:18px">Find an upcoming Chef Battle event near you and apply to compete.</p></div>
    </div>
    <div class="events">
      <div class="ev-row ev-head"><span>Date</span><span>Event</span><span>Stage</span><span>Status</span><span></span></div>
      {rows}
    </div>
    <p class="legal" style="margin-top:20px">Sample listings for layout only.</p>
  </div>
</section>
<section class="section--band bg-navy">
  <div class="wrap band-grid">
    <div class="stack" style="gap:14px"><h2 class="h2">Want to Compete?</h2><p style="font-size:18px">Become a League Chef to be eligible to participate in official Chef Battle events.</p><p class="legal">Competition participation and advancement are subject to official rules and qualification requirements.</p></div>
    {btn(CTA_JOIN, STRIPE_LINK, "primary", "lg")}
  </div>
</section>'''
    page("competitions/index.html", "Competitions", "Compete in Chef Battle city events and regional showdowns, and qualify for the World Chef Cup. See upcoming competitions and apply.", body, active="Competitions")

def membership():
    inc = "".join(f'<div class="inc"><div class="num">{n}</div><div class="t">{e(t)}</div><p>{e(b)}</p></div>' for n, t, b in INCLUDES)
    gl = "".join(f'<div class="glance-row"><span class="b">{e(b)}</span><span class="d{" hi" if hi else ""}">{e(d)}</span></div>' for b, d, hi in GLANCE)
    fq = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQS)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]})
    body = f'''
<section class="bg-bone page-hero">
  <div class="wrap hero-grid mem-grid">
    <div class="stack" style="gap:22px">
      <div class="eyebrow">More Exposure. More Opportunities. One Membership.</div>
      <h1 class="h1">Become a League Chef<span class="dot">.</span></h1>
      <p class="body-lg">Whether you're an executive chef, private chef, caterer, or just getting started, Global Chef League helps you showcase your skills, connect with potential customers, and compete.</p>
    </div>
    <div class="price-card">
      <div class="top"><span>League Chef Membership</span><span class="badge badge--brand">Annual</span></div>
      <div class="price-big" aria-label="$25 per year"><span class="cur">$</span><span class="amt">25</span><span class="per">/YEAR</span></div>
      <div class="note">No additional Chef Battle competition entry fees. No booking commissions.</div>
      {btn(CTA_JOIN, STRIPE_LINK, "primary", "lg", block=True)}
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    {head_block("Your League Chef Membership Includes", hcls="h2 h2--sm")}
    <div class="grid g-3" style="gap:48px 40px">{inc}</div>
  </div>
</section>
<section style="padding-bottom:104px">
  <div class="wrap side-grid">
    <div class="stack"><div class="eyebrow">Membership at a Glance</div><h2 class="h2 h2--sm">One Membership<span class="dot">.</span></h2><div class="rule"></div><p>{e(SUPPORT)}</p></div>
    <div class="glance"><div class="glance-row head"><span>Benefit</span><span>Details</span></div>{gl}</div>
  </div>
</section>
<section class="section--band bg-navy">
  <div class="wrap band-grid">
    <div class="stack" style="gap:14px">
      <h2 class="h2">Join Today for $25/Year</h2>
      <p style="font-size:18px">Become an official League Chef with one annual membership.</p>
      <p style="font-size:18px">No additional Chef Battle competition entry fees. No booking commissions.</p>
      <p class="legal" style="margin-top:8px">Membership renews automatically each year unless canceled. Competition participation is subject to eligibility, selection, and availability.</p>
    </div>
    {btn(CTA_JOIN, STRIPE_LINK, "primary", "lg")}
  </div>
</section>
<section class="section" id="faq">
  <div class="wrap side-grid">
    <div class="stack"><h2 class="h2 h2--sm">Frequently Asked Questions<span class="dot">.</span></h2><div class="rule"></div></div>
    <div class="faq">{fq}</div>
  </div>
</section>
<script type="application/ld+json">{faq_ld}</script>'''
    page("membership/index.html", "Membership — $25/Year", "Become a League Chef for $25 a year: a public chef profile, no Chef Battle entry fees, and 0% booking commissions.", body, active="Membership")

def about():
    roles = "".join(f'<div class="role {rc}">{badge(b)}<div class="t">{e(t)}</div><p>{e(d)}</p></div>' for b, rc, t, d in ROLE_CARDS)
    body = f'''
<section class="section--md">
  <div class="wrap about-intro">
    <h1 class="h1">Built for Chefs<span class="dot">.</span></h1>
    <div class="stack" style="gap:18px">
      <p>Global Chef League gives chefs more ways to showcase their talent, grow their reputation, and connect with new opportunities.</p>
      <p>Through Chef Battle competitions, the World Chef Cup, and our online chef directory, we're creating a place where culinary professionals can compete, get discovered, and promote what they do best.</p>
      <p>Whether you're an established chef or building your career, there's a place for you in the league.</p>
    </div>
  </div>
</section>
<div class="wrap"><div class="wide-photo">{ph("Chef Battle crowd and judges")}</div></div>
<section class="section">
  <div class="wrap">
    {head_block("Our League", eyebrow="League Roles & Local Chapters")}
    <div class="grid g-3" style="margin-bottom:56px">{roles}</div>
    {btn("Become a League Chef", "{R}membership/", "primary", "lg")}
  </div>
</section>'''
    page("about/index.html", "About", "Global Chef League brings the excitement, prestige and community of professional sports to the culinary industry through Chef Battle, the World Chef Cup and our chef directory.", body, active="About")

def contact():
    body = f'''
<div class="contact-split">
  <section class="bg-navy left">
    <h1 class="h1 h1--sm">Get in Touch<span class="dot">.</span></h1>
    <p>Have a question about League Chef membership, chef profiles, competitions, chapters, or partnerships?</p>
    <p>Send us a message and we'll be happy to help.</p>
    <p class="legal" style="margin-top:auto">Or email <a href="mailto:{e(CONTACT_EMAIL)}" style="color:#fff">{e(CONTACT_EMAIL)}</a></p>
  </section>
  <section class="right">
    <form action="{e(FORM_CONTACT)}" method="POST" data-ajax data-success="Thanks! Your message has been sent. We'll get back to you soon." class="stack-lg" style="align-items:stretch">
      <input type="hidden" name="_subject" value="GCL website — contact form">
      <input type="text" name="_gotcha" class="sr-only" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="form-grid">
        <div class="field"><label for="c-name">Name <span class="req">*</span></label><input class="input" id="c-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="c-email">Email <span class="req">*</span></label><input class="input" id="c-email" name="email" type="email" required autocomplete="email"></div>
      </div>
      <div class="field"><label for="c-topic">Topic</label><select class="select" id="c-topic" name="topic">{options(TOPICS, "Choose a topic")}</select></div>
      <div class="field"><label for="c-msg">Message <span class="req">*</span></label><textarea class="textarea" id="c-msg" name="message" rows="7" required></textarea></div>
      <div class="form-msg" aria-live="polite"></div>
      <div><button class="btn btn--primary btn--lg" type="submit">Send Message</button></div>
    </form>
  </section>
</div>
<script>
(function(){{var t=new URLSearchParams(location.search).get('topic');if(t){{var s=document.getElementById('c-topic');for(var i=0;i<s.options.length;i++){{if(s.options[i].text===t){{s.selectedIndex=i}}}}}}}})();
</script>'''
    page("contact/index.html", "Contact", "Questions about League Chef membership, chef profiles, competitions, chapters or partnerships? Contact Global Chef League.", body)

def welcome():
    steps = [("01", "Membership purchased", "done"), ("02", "Submit your profile", "now"), ("03", "We verify your membership", ""), ("04", "Profile published in the directory", "")]
    st = "".join(f'<div class="step {c}"><span class="num">{n}</span><span class="t">{e(t)}</span><span class="tick">{"✓" if c == "done" else ""}</span></div>' for n, t, c in steps)
    body = f'''
<section class="section--md bg-bone">
  <div class="wrap welcome-grid">
    <div class="stack" style="gap:22px">
      <span class="badge badge--brand badge--capsule">Thanks for joining!</span>
      <h1 class="h1 h1--sm">You're In! Welcome to Global Chef League<span class="dot">.</span></h1>
      <p class="lead">You're officially on your way to becoming a published League Chef.</p>
      <p class="body-lg">Now it's time to create your professional profile so people can discover you and your services.</p>
      <p class="body-lg">Add your photo, experience, specialties, rates, and contact information. Once your membership is verified and your profile is approved, we'll publish it in the directory.</p>
      {btn("Create My League Chef Profile", "{R}submit-profile/", "primary", "lg")}
    </div>
    <div class="stack-lg" style="align-items:stretch">
      <div class="steps">{st}</div>
      <div class="stack" style="gap:14px"><p>{"Watch your email for league updates and the first Chef Battle competition announcements." if LANDING_MODE else "In the meantime, explore upcoming Chef Battle competitions and watch your email for league updates."}</p>{"" if LANDING_MODE else btn("Explore Competitions", "{R}competitions/", "secondary")}</div>
    </div>
  </div>
</section>'''
    page("welcome/index.html", "Welcome to the League", "Thanks for joining Global Chef League. Create your League Chef profile.", body, noindex=True)

def submit_profile():
    secs = [("01", "The Basics", "basics"), ("02", "Your Cooking", "cooking"), ("03", "Rates & Contact", "rates")]
    idx = "".join(f'<a href="#{a}"><span class="num">{n}</span><span class="t">{e(t)}</span></a>' for n, t, a in secs)
    checks = "".join(f'<label class="check"><input type="checkbox" name="services[]" value="{e(s)}"> {e(s)}</label>' for s in SERVICES)
    def inp(id_, label, name, type_="text", req=False, ph_="", extra=""):
        r = ' <span class="req">*</span>' if req else ""
        return f'<div class="field"><label for="{id_}">{e(label)}{r}</label><input class="input" id="{id_}" name="{name}" type="{type_}"{" required" if req else ""}{f" placeholder=\"{e(ph_)}\"" if ph_ else ""} {extra}></div>'
    body = f'''
<section class="bg-navy page-hero">
  <div class="wrap submit-head">
    <h1 class="h1 h1--sm">Create Your League Chef Profile<span class="dot">.</span></h1>
    <div class="stack" style="gap:14px">
      <p>Tell us about yourself, your culinary background, and the services you offer.</p>
      <p>Your profile will give potential customers a place to discover your work, see your rates, and contact you directly.</p>
      <p>Once submitted, our team will review your information and publish your profile after confirming your active membership.</p>
    </div>
  </div>
</section>
<section class="section--md">
  <div class="wrap submit-cols">
    <nav class="sec-index" aria-label="Form sections">{idx}</nav>
    <form action="{e(FORM_PROFILE)}" method="POST" enctype="multipart/form-data" data-ajax data-success="Profile submitted! We'll verify your membership and email you when your profile is live.">
      <input type="hidden" name="_subject" value="GCL website — new League Chef profile">
      <input type="text" name="_gotcha" class="sr-only" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="fsec" id="basics">
        <div class="fsec-title"><span class="num">01</span> The Basics</div>
        <div class="basics">
          <div class="field"><span class="flabel">Profile photo <span class="req">*</span></span>
            <label class="upload"><input type="file" id="photo" name="photo" accept="image/*" required><span class="plus">+</span><span class="label">Upload profile photo</span><span class="hint">JPG or PNG, portrait, at least 800px wide</span></label>
          </div>
          <div class="form-grid" style="align-content:start">
            {inp("p-name", "Chef name", "chef_name", req=True, extra='autocomplete="name"')}
            {inp("p-email-private", "Your email (private)", "account_email", "email", req=True, extra='autocomplete="email"')}
            {inp("p-city", "City", "city", req=True)}
            {inp("p-state", "State/Region", "state_region")}
            <div class="field"><label for="p-country">Country <span class="req">*</span></label><select class="select" id="p-country" name="country" required>{options(COUNTRIES, "Select country")}</select></div>
            <div class="field"><span class="flabel">League designation</span><div class="desig"><span class="badge badge--outline">League Chef</span><span class="hint">Assigned on approval</span></div></div>
          </div>
        </div>
      </div>
      <div class="fsec" id="cooking">
        <div class="fsec-title"><span class="num">02</span> Your Cooking</div>
        <div class="field"><label for="p-bio">Biography <span class="req">*</span></label><textarea class="textarea" id="p-bio" name="biography" rows="5" required></textarea><span class="hint">Professional background, culinary experience, and specialties.</span></div>
        <div class="field"><span class="flabel">Services offered <span class="req">*</span></span><div class="checks" data-require-one>{checks}</div></div>
        {inp("p-spec", "Culinary specialties", "specialties", req=True, ph_="e.g. Latin Caribbean, Live-fire, Seafood")}
      </div>
      <div class="fsec" id="rates">
        <div class="fsec-title"><span class="num">03</span> Rates &amp; Contact</div>
        <div class="form-grid">
          {inp("p-rate", "Starting rates", "starting_rates", ph_="From $85/guest or Contact for Pricing")}
          {inp("p-area", "Service area", "service_area")}
          {inp("p-pemail", "Public contact email", "public_email", "email", extra="data-contact-method")}
          {inp("p-phone", "Public phone", "public_phone", "tel", extra="data-contact-method")}
          {inp("p-web", "Website", "website", "url", ph_="https://")}
          {inp("p-book", "Booking link", "booking_link", "url", ph_="https://", extra="data-contact-method")}
          <div class="field span2"><label for="p-social">Social media</label><input class="input" id="p-social" name="social_media" placeholder="Instagram, TikTok, Facebook URLs"></div>
        </div>
        <p class="hint">At least one public contact method or booking link is required for publication.</p>
      </div>
      <div class="submit-bar">
        <label class="check"><input type="checkbox" name="permission" value="yes" required> Only include photos and contact information that you have permission to publish.</label>
        <div class="form-msg" aria-live="polite" style="width:100%"></div>
        <button class="btn btn--primary btn--lg" type="submit">Submit My Profile</button>
      </div>
    </form>
  </div>
</section>'''
    page("submit-profile/index.html", "Create Your League Chef Profile", "Submit your League Chef profile to Global Chef League.", body, noindex=True)

LEGAL = {
    "membership-terms": ("Membership Terms", None),
    "privacy": ("Privacy Policy", None),
    "terms": ("Website Terms", None),
    "directory-disclaimer": ("Directory Disclaimer", [
        "Global Chef League provides an online directory where League Chefs can showcase their experience, services, rates, and contact information.",
        "Chefs listed in the directory operate independently. All inquiries, bookings, payments, and service arrangements are handled directly between the customer and the chef.",
        "Bookings and payments are arranged directly with each chef. Global Chef League does not manage or guarantee services, and does not take a commission on bookings.",
        "Designations such as League Chef, Chapter President, and League Champion describe a chef's role or recognition within Global Chef League. They are not a guarantee of the quality, safety, licensing, or insurance of any service.",
        "Customers are responsible for confirming a chef's qualifications, licensing, insurance, and availability before booking.",
    ]),
}

def legal_pages():
    for slug, (title, paras) in LEGAL.items():
        if paras:
            content = "".join(f"<p>{e(p)}</p>" for p in paras)
            note = '<p class="sample-note">Draft for review — have your attorney approve before launch.</p>'
        else:
            content = f'<p>The full {e(title)} will be published here before launch.</p><p>Questions in the meantime? <a href="mailto:{e(CONTACT_EMAIL)}">Email us</a>.</p>'
            note = '<p class="sample-note">Placeholder — paste your attorney-approved text here.</p>'
        body = f'''
<section class="bg-navy page-hero" style="padding:72px 0"><div class="wrap"><h1 class="h1 h1--sm">{e(title)}<span class="dot">.</span></h1></div></section>
<section class="section--md"><div class="wrap legal-body">{note}{content}</div></section>'''
        page(f"{slug}/index.html", title, f"Global Chef League {title}.", body, noindex=not paras)

def not_found():
    body = f'''
<section class="bg-navy page-hero" style="padding:120px 0">
  <div class="wrap stack" style="gap:22px">
    <div class="eyebrow">Error 404</div>
    <h1 class="h1">Off the Menu<span class="dot">.</span></h1>
    <p>We couldn't find that page. It may have moved, or the link may be out of date.</p>
    <div class="btn-row">{btn("Back to Home", "{R}", "primary", "lg")}{"" if LANDING_MODE else btn("Find a Chef", "{R}chefs/", "inverse", "lg")}</div>
  </div>
</section>'''
    page("404.html", "Page Not Found", "Page not found.", body, noindex=True)

def sitemap():
    urls = "".join(f"  <url><loc>{SITE_URL.rstrip('/')}/{p.replace('index.html', '')}</loc></url>\n" for p, ni in PAGES if not ni)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL.rstrip('/')}/sitemap.xml\n")

if __name__ == "__main__":
    if LANDING_MODE:
        landing(); welcome(); submit_profile(); legal_pages(); not_found()
    else:
        home(); directory()
        for c in CHEFS: profile(c)
        competitions(); membership(); about(); contact(); welcome(); submit_profile(); legal_pages(); not_found()
    sitemap()
    print(f"Built {len(PAGES)} pages into {ROOT}")
