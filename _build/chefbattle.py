# Chef Battle section of the Global Chef League site.
# Loaded by build.py (exec'd into its namespace, so it can use page(), btn(), e(), etc.).
#
# Content carried over from chefbattle.events and restyled in the GCL look.
# Edit copy, numbers and forms here, then run: python3 _build/build.py

CB_IMG = "assets/img/chef-battle/"
OPERATOR_FORM = "https://forms.gle/3E6wzB1EidKPjdC36"
INTL_OPERATOR_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSfNG9JY7pl4KMQUHPLtv9dJq6WF1TLsnlqdZvOGwcsUd9dACA/viewform?usp=header"

def cb_mail(subject):
    from urllib.parse import quote
    return f"mailto:{CONTACT_EMAIL}?subject={quote(subject)}"

def pic(name, alt, cls="", pos="center"):
    return f'<div class="pic {cls}"><img src="{{R}}{CB_IMG}{name}" alt="{e(alt)}" style="object-position:{pos}"></div>'

def cb_hero(eyebrow, title, sub, buttons, image=None, image_alt="", pos="center", extra=""):
    media = f'<div class="cb-hero-media">{pic(image, image_alt, pos=pos)}</div>' if image else ""
    return f'''
<section class="bg-navy cb-hero{" cb-hero--media" if image else ""}">
  <div class="wrap cb-hero-grid">
    <div class="stack-lg">
      <div class="eyebrow">{eyebrow}</div>
      <h1 class="h-hero">{title}</h1>
      <p class="cb-sub">{sub}</p>
      <div class="btn-row">{buttons}</div>
      {extra}
    </div>
    {media}
  </div>
</section>'''

def strip(items):
    return '<div class="cb-strip"><div class="wrap">' + "".join(f"<span>{e(i)}</span>" for i in items) + "</div></div>"

def numbered(items, cols=2):
    return f'<div class="grid g-{cols} cb-num">' + "".join(
        f'<div class="pillar"><div class="num">{n}</div><div class="label">{e(k)}</div><h3 class="h3">{e(t)}</h3><p>{e(b)}</p></div>'
        for n, k, t, b in items) + "</div>"

def ticklist(items):
    return '<ul class="cb-list">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"

def terms(items, note=""):
    cells = "".join(f'<div class="cb-term"><div class="v">{e(v)}</div><div class="label">{e(k)}</div></div>' for v, k in items)
    return f'<div class="cb-terms">{cells}</div>' + (f'<p class="legal" style="margin-top:20px">{e(note)}</p>' if note else "")

def traits():
    T = [("Entrepreneurial", "You see opportunities and go after them."), ("Connected", "You know your local food and business community."),
         ("Organized", "You can manage moving pieces and follow a plan."), ("Relationship-Driven", "You build trust and get people on board."),
         ("Community-Minded", "You care about the people and places in your city.")]
    return '<div class="cb-traits">' + "".join(f'<div class="cb-trait"><div class="t">{e(a)}</div><p>{e(b)}</p></div>' for a, b in T) + "</div>"

def logo_wall(logos, cols=4):
    return f'<div class="cb-logos" style="--cols:{cols}">' + "".join(
        f'<div class="cb-logo"><img src="{{R}}{CB_IMG}logo-{f}" alt="{e(a)}"></div>' for f, a in logos) + "</div>"

PARTNER_LOGOS = [("performance-foodservice.png", "Performance Foodservice"), ("smart-final.png", "Smart & Final"), ("smart-foodservice.png", "Smart Foodservice Warehouse Stores"),
                 ("breakthru.png", "Breakthru Beverage Group"), ("red-bull.png", "Red Bull"), ("boxed-water.png", "Boxed Water"),
                 ("iowa-pork.png", "Iowa Pork"), ("t-mobile.png", "T-Mobile")]
PRESS_LOGOS = [("la-times.png", "Los Angeles Times"), ("chicago-tribune.png", "Chicago Tribune"), ("review-journal-logo.png", "Las Vegas Review-Journal"),
               ("food-beverage-magazine.png", "Food & Beverage Magazine")]
NATIONALS_PARTNERS = [("hofbrauhaus.png", "Hofbräuhaus Las Vegas"), ("breakthru.png", "Breakthru Beverage"), ("fresh-and-less.png", "Fresh and Less Market"),
                      ("boxed-water.png", "Boxed Water"), ("red-bull.png", "Red Bull"), ("food-beverage-magazine.png", "Food & Beverage Magazine")]

STAGES = [("01", "Local Battle", "Chefs compete in cities across the globe. A mystery ingredient basket, often featuring a sponsor's hero product, kicks off each event. 45 minutes. Full kitchen. Live audience.", ""),
          ("02", "World Battle", "City champions advance to the World Battle. One chef. One title. The World Battle champion is crowned on stage in front of thousands, with your brand written into every moment of the journey.", "gold")]

# ------------------------------------------------------------------
# /chef-battle/
# ------------------------------------------------------------------
def cb_home():
    pillars = [("Live Competition", "Real chefs, real pressure, real results in front of a live crowd."),
               ("Global Tour", "City champions advance to the World Battle."),
               ("Audience Tasting", "Every attendee samples the dishes and takes part in the verdict."),
               ("Brand Integration", "Sponsored ingredients and activations built into every battle.")]
    pil = "".join(f'<div class="cb-pillar"><div class="t">{e(t)}</div><p>{e(b)}</p></div>' for t, b in pillars)
    stages = "".join(f'<div class="cb-stage{" cb-stage--gold" if g else ""}"><div class="num">{n}</div><div class="t">{e(t)}</div><p>{e(b)}</p></div>' for n, t, b, g in STAGES)
    taste = [("T", "Taste", "Overall flavor, balance, and enjoyment of the dish"), ("A", "Appearance", "Visual presentation and plating artistry"),
             ("S", "Skill", "Execution with precision and professional consistency"), ("T", "Technique", "Command of cooking methods and kitchen craft"),
             ("E", "Execution", "Overall ability to deliver a complete, cohesive dish under pressure")]
    tst = "".join(f'<div class="cb-letter"><div class="l">{l}</div><div class="t">{e(t)}</div><p>{e(d)}</p></div>' for l, t, d in taste)
    aud = [("61%", "Aged 25–44"), ("$85K", "Average household income"), ("3.1M+", "People reached"), ("58%", "Female audience")]
    audh = "".join(f'<div class="cb-stat"><div class="v">{v}</div><div class="label">{e(k)}</div></div>' for v, k in aud)
    ways = [("Compete", "Become a League Chef and apply to compete in Chef Battle events, with no additional entry fees.", "Become a League Chef", "{R}"),
            ("Bring It to Your City", "Lead Chef Battle in your market as a Local Operator and share in the event profit.", "Become an Operator", "{R}chef-battle/operators/"),
            ("Corporate Team Building", "Bring the Chef Battle format to your team, on-site, off-site or as a private event.", "Plan a Team Event", "{R}chef-battle/team-building/"),
            ("Sponsor a Battle", "Put your product at the center of the challenge in front of engaged food lovers.", "Request the Deck", cb_mail("Chef Battle sponsorship deck"))]
    wh = "".join(f'<div class="cb-way"><div class="t">{e(t)}</div><p>{e(b)}</p>{btn(c, h, "secondary", "sm")}</div>' for t, b, c, h in ways)
    body = f'''
{cb_hero("Chef Battle · A Global Chef League Competition",
         'The Heat<br>Is On<span class="dot">.</span>',
         "Chef Battle is the live culinary competition tour of Global Chef League. Real chefs, real pressure, real crowds, in 20+ markets nationwide.",
         btn("Compete in Chef Battle", "{R}", "primary", "lg") + btn("See How It Works", "#format", "inverse", "lg"),
         "competition-floor.jpg", "Chefs competing on the Chef Battle floor", "center")}

<section class="section" id="about">
  <div class="wrap">
    <div class="roster-head">
      <div class="stack"><div class="eyebrow">What Is Chef Battle</div><h2 class="h2">Where Skill Meets Spectacle<span class="dot">.</span></h2><div class="rule"></div></div>
      <p style="font-size:18px">Chef Battle is a live, head-to-head cooking competition where local chefs go against each other in front of a paying audience. Every event features competing chefs, celebrity judges, a live emcee, and audience tasting. Attendees don't just watch. They eat, vote, and interact throughout.</p>
    </div>
    <div class="cb-pillars">{pil}</div>
    <div class="cb-mosaic">
      {pic("competing.jpg", "Chef competing live")}{pic("plating.jpg", "Chef plating a dish")}{pic("crowd.jpg", "Chef Battle event crowd")}{pic("judges.jpg", "Judges tasting panel")}
    </div>
  </div>
</section>

<section class="section--band bg-bone">
  <div class="wrap band-grid">
    <div class="cb-bignum"><span class="num">200,000+</span><span class="label">Product samples per season</span></div>
    <p class="measure" style="font-size:18px">Not impressions: real moments of trial. Over 200,000 product samples delivered per season to engaged food lovers across 20+ markets. Real people, real taste, real engagement.</p>
  </div>
</section>

<section class="section bg-navy" id="format" style="scroll-margin-top:76px">
  <div class="wrap">
    <div class="section-head"><div class="eyebrow">The Competition Format</div><h2 class="h2">Local Battles. Global Glory<span class="dot">.</span></h2><div class="rule"></div>
      <p class="measure" style="font-size:18px;color:var(--on-navy)">Chefs compete in cities across the globe. The best rise through the ranks, and one chef earns the World Battle title.</p></div>
    <div class="cb-stages cb-stages--2">{stages}</div>
    <p class="legal" style="margin-top:28px">Competing in Chef Battle requires an active League Chef membership. <a href="{{R}}" style="color:#fff">Become a League Chef</a>.</p>
  </div>
</section>

<section class="section" id="judging">
  <div class="wrap">
    <div class="roster-head">
      <div class="stack"><div class="eyebrow">The Judging Framework</div><h2 class="h2">Judged on the T.A.S.T.E. Framework<span class="dot">.</span></h2><div class="rule"></div></div>
      <p style="font-size:18px">Every dish at Chef Battle is evaluated across five criteria: a scoring system built to reward not just flavor, but the full range of a chef's abilities under live competition pressure.</p>
    </div>
    <div class="cb-letters">{tst}</div>
    <div class="cb-callout">
      <span class="badge badge--award">Crowd's Choice Award</span>
      <div><div class="t">The People's Verdict</div><p>Beyond the judges' scores, the audience votes for their favorite dish of the night. The Crowd's Choice winner takes home a separate title, because in Chef Battle the fans are always part of the competition.</p></div>
    </div>
  </div>
</section>

<section class="section bg-bone">
  <div class="wrap cb-feature">
    {pic("winners.jpg", "Mike Pascua, Chef Battle National Champion", "cb-feature-pic", "center 35%")}
    <div class="stack" style="gap:18px">
      <div class="eyebrow">Latest Results · Chef Battle Nationals</div>
      <h2 class="h2">Mike Pascua Takes the National Title<span class="dot">.</span></h2>
      <p style="font-size:18px">Fifteen city champions. Three nights in Las Vegas. Orange County's Mike Pascua outcooked the field to claim the Chef Battle National Champion title and the $5,000 prize.</p>
      {btn("See the Nationals Recap", "{R}chef-battle/nationals/", "primary", "lg")}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head_block("Industry Recognition", eyebrow="Trusted By & As Seen In")}
    <div class="label" style="margin-bottom:16px">A few of the brands we work with</div>
    {logo_wall(PARTNER_LOGOS)}
    <div class="label" style="margin:40px 0 16px">A few places you might have spotted us</div>
    {logo_wall(PRESS_LOGOS)}
  </div>
</section>

<section class="section bg-navy">
  <div class="wrap split-72">
    <div class="stack" style="gap:18px">
      <div class="eyebrow">Who's in the Room</div>
      <h2 class="h2">An Audience That Eats It Up<span class="dot">.</span></h2>
      <p style="font-size:18px;color:var(--on-navy)">Chef Battle draws passionate food fans: the kind who seek out new flavors, follow chefs on social, and make purchasing decisions based on culinary experiences.</p>
      <ul class="cb-list cb-list--inv">
        <li>Live events outperform digital for brand recall, product trial intent, and purchase conversion, especially in food and beverage.</li>
        <li>Ingredient brands win here. When your product is the hero of the challenge, it's not an ad. It's a story told live, in front of hundreds.</li>
        <li>Content lives on. Every event generates organic social, recap video, and editorial coverage that extends well beyond event day.</li>
      </ul>
    </div>
    <div class="cb-stats">{audh}</div>
  </div>
</section>

<section class="section" id="get-involved">
  <div class="wrap">
    {head_block("Step Into Our Kitchen", eyebrow="Get Involved")}
    <div class="cb-ways">{wh}</div>
  </div>
</section>'''
    page("chef-battle/index.html", "Chef Battle — The Live Culinary Competition",
         "Chef Battle is Global Chef League's live culinary competition tour: real chefs, real pressure, real crowds in 20+ markets. Compete, sponsor, host or bring Chef Battle to your city.",
         body, active="Chef Battle")

# ------------------------------------------------------------------
# /chef-battle/nationals/  (merges the old nationals + case-study pages)
# ------------------------------------------------------------------
NAT_CHEFS = {
    "one": [("oscar-sanchez", "Oscar Sanchez", "Executive Chef + Owner, Oscar Catering", "Las Vegas Champion", True),
            ("khaddy-moore", "Khaddy Moore", "Chef, Maestoso", "San Diego Champion", False),
            ("taylor-figueroa", "Taylor Figueroa", "Chef/Owner, Botanist", "Portland Champion", False),
            ("ladonna-bell", "LaDonna Bell", "Personal Chef, LaDonna's Innovative Chef Services", "Quad Cities Champion", True),
            ("david-adlard", "David Adlard", "Chef/Owner, Candle in the Woods", "Spokane Champion", True),
            ("ariella-katzberg", "Ariella Katzberg", "District Manager, Wendy's", "Orange County Champion", False),
            ("chris-jones", "Chris Jones", "Cook, The Savory Grill", "Kansas City Champion", False),
            ("brittiney-moore", "Brittiney Moore", "Executive Chef, 8th Wonder Cuisine", "Charleston Champion", False)],
    "two": [("brandon-yamasaki", "Brandon Yamasaki", "Cook, Jackie Rey's Hilo", "Hawaii Champion", True),
            ("deanna-delmar", "Deanna Delmar", "Sous Chef, Korner Pocket / Popa Kona Restaurant and Cafe", "Hawaii Champion", False),
            ("justin-scardina", "Justin Scardina", "Chef/Owner, La Rana Bistro / driftless food & catering", "Chicago Champion", False),
            ("travis-tveit", "Travis Tveit", "Head Chef, Iron Goat Brewery", "Spokane Champion", True),
            ("jon-vanhusen", "Jon VanHusen", "Executive Chef, Nice Touch Catering", "Las Vegas Champion", False),
            ("april-muhammad", "April Muhammad", "Co-Founder, Magic City Flavors", "Alabama Champion", True),
            ("mike-pascua", "Mike Pascua", "Executive Chef, Lounge Group", "Orange County Champion", True)],
}

def chef_cards(rows):
    out = ""
    for slug, name, role, city, finalist in rows:
        champ = slug == "mike-pascua"
        tag = '<span class="badge badge--award">National Champion</span>' if champ else ('<span class="badge badge--ink">Finalist</span>' if finalist else "")
        out += f'''<div class="cb-chef{" cb-chef--champ" if champ else ""}">
  <div class="pic"><img src="{{R}}{CB_IMG}chef-{slug}.jpg" alt="{e(name)}"></div>
  <div class="info"><div class="name">{e(name)}</div><div class="city">{e(city)}</div><div class="role">{e(role)}</div>{f'<div class="badges">{tag}</div>' if tag else ""}</div>
</div>'''
    return f'<div class="cb-chefs">{out}</div>'

def cb_nationals():
    facts = [("Venue", "Hofbräuhaus Las Vegas"), ("Dates", "February 10–12"), ("Format", "3-night tournament"), ("Prize", "$5,000 + national title")]
    fh = "".join(f'<div class="stat"><span class="label">{e(k)}</span><span class="v sm">{e(v)}</span></div>' for k, v in facts)
    nights = [("Night One", "Preliminary", "8 chefs. One hour to create their best dish for the judges, then bites for the crowd. Judges score, crowd votes.", "Hosted by Michael Politz, Founder & Editor-in-Chief, Food & Beverage Magazine", "Top 3 advance to the finals", ""),
              ("Night Two", "Preliminary", "7 chefs. Same format, same pressure. A tied score advanced 4 chefs to the finals instead of 3.", "Hosted by Michael Politz, Food & Beverage Magazine", "Top 4 advance (tied score)", ""),
              ("Night Three", "The Finals", "7 finalists. One title. One chef walks away as the Chef Battle National Champion.", "Hosted by Shaun O'Neale, MasterChef Season 7 Winner", "National Champion crowned", "gold")]
    nh = "".join(f'<div class="cb-stage{" cb-stage--gold" if g else ""}"><div class="label">{e(a)}</div><div class="t">{e(b)}</div><p>{e(c)}</p><p class="host">{e(d)}</p><div class="adv">{e(x)}</div></div>' for a, b, c, d, x, g in nights)
    nums = [("15", "Competing chefs"), ("3", "Nights of competition"), ("7", "Championship finalists"), ("500", "Total attendees"), ("$5K", "Cash prize awarded")]
    numh = "".join(f'<div class="cb-stat"><div class="v">{v}</div><div class="label">{e(k)}</div></div>' for v, k in nums)
    body = f'''
<section class="bg-navy cb-hero cb-hero--media">
  <div class="wrap cb-hero-grid">
    <div class="stack-lg">
      <div class="eyebrow">Chef Battle Nationals · Las Vegas</div>
      <h1 class="h-hero">15 Champions.<br>One Title<span class="dot">.</span></h1>
      <p class="cb-sub">Fifteen city champions from the East Coast to Hawaii earned their spot through local and regional battles across 20+ cities. Over three nights at Hofbräuhaus Las Vegas, they competed for national bragging rights, a $5,000 prize and the title of Chef Battle National Champion.</p>
      <div class="stats four">{fh}</div>
    </div>
    <div class="cb-hero-media">{pic("winners.jpg", "Mike Pascua, Chef Battle National Champion, with the winner's check", pos="center 35%")}</div>
  </div>
</section>

<section class="section bg-bone">
  <div class="wrap cb-feature">
    <div class="stack" style="gap:18px">
      <span class="badge badge--award badge--capsule">And the Winner Is…</span>
      <h2 class="h2">Mike Pascua<span class="dot">.</span></h2>
      <div class="label" style="color:var(--navy)">Chef Battle National Champion · Orange County</div>
      <p style="font-size:18px">Mike Pascua battled through local competition in Orange County, earned his spot at Nationals, and outcooked 14 other city champions across three nights in Las Vegas to claim the title and the $5,000 prize.</p>
    </div>
    {pic("chef-mike-pascua.jpg", "Mike Pascua", "cb-feature-pic cb-feature-pic--portrait", "center 30%")}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="roster-head">
      <div class="stack"><div class="eyebrow">The Challenge</div><h2 class="h2">From City Champions to a National Stage<span class="dot">.</span></h2><div class="rule"></div></div>
      <div class="stack" style="gap:14px">
        <p>Chef Battle had spent years building a multi-city competition circuit: local battles across the country, each producing a champion. The question was always what happens next.</p>
        <p>Nationals called for a three-night, tournament-style event that honored what these chefs had accomplished, on a stage worthy of a national championship. Hofbräuhaus Las Vegas, one of the most recognizable dining venues in the city, became the host partner.</p>
        <p>Chefs battled with limited equipment, limited ingredients and limited time, each with one sous chef. Dishes were judged on appearance, creativity and taste, with the crowd casting votes too.</p>
      </div>
    </div>
    <div class="cb-mosaic cb-mosaic--2">{pic("nationals-chef.jpg", "Chef competing at Chef Battle Nationals")}{pic("crowd-night.jpg", "Crowd at Chef Battle Nationals, Hofbräuhaus Las Vegas")}</div>
  </div>
</section>

<section class="section bg-navy">
  <div class="wrap">
    <div class="section-head"><div class="eyebrow">The Format</div><h2 class="h2">Three Nights. One Champion<span class="dot">.</span></h2><div class="rule"></div>
      <p class="measure" style="font-size:18px;color:var(--on-navy)">A tournament built for drama, fairness and spectacle, with a host each night matched to the stakes.</p></div>
    <div class="cb-stages">{nh}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head_block("The Competitors", eyebrow="15 City Champions")}
    <p class="measure" style="font-size:18px;margin:-32px 0 40px">Every chef earned their place through local and regional battles. These weren't contestants. They were already champions.</p>
    <div class="cb-night"><span class="label">Night One · February 10 · Preliminary · 8 Chefs</span></div>
    {chef_cards(NAT_CHEFS["one"])}
    <div class="cb-night" style="margin-top:48px"><span class="label">Night Two · February 11 · Preliminary · 7 Chefs</span></div>
    {chef_cards(NAT_CHEFS["two"])}
  </div>
</section>

<section class="section bg-bone">
  <div class="wrap">
    {head_block("The Hosts", eyebrow="Hosts of the Battle")}
    <div class="cb-hosts">
      <div class="cb-host">{pic("shaun-oneale.jpg", "Shaun O'Neale celebrating with confetti", pos="center 30%")}
        <div class="stack" style="gap:10px"><span class="badge badge--award">Finals Host · Night Three</span><div class="t">Shaun O'Neale</div><div class="label">MasterChef Season 7 Winner</div>
        <p>Shaun O'Neale won MasterChef Season 7 under Gordon Ramsay, beating out tens of thousands of home cooks to claim one of the most coveted titles in culinary television. A DJ-turned-chef, Shaun brought relentless creativity and technical precision to every dish, and the same energy to the Nationals finals stage.</p></div></div>
      <div class="cb-host">{pic("michael-politz.jpg", "Michael Politz", pos="left center")}
        <div class="stack" style="gap:10px"><span class="badge badge--ink">Nights One &amp; Two Host</span><div class="t">Michael Politz</div><div class="label">Founder &amp; Editor-in-Chief, Food &amp; Beverage Magazine</div>
        <p>Michael Politz founded Food &amp; Beverage Magazine, the go-to source for behind-the-scenes news in restaurants and hospitality, read by 12 million people a month. Snarky, sarcastic and always in the know, he brought a seasoned industry lens to the preliminary rounds.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head_block("Beyond the Venue", eyebrow="Marketing & Media")}
    <div class="cb-press">
      <figure>{pic("marquee.jpg", "Chef Battle Nationals on the Hofbräuhaus Las Vegas marquee")}<figcaption><b>Hofbräuhaus marquee.</b> High-visibility signage on a major Las Vegas corridor.</figcaption></figure>
      <figure>{pic("review-journal.jpg", "Las Vegas Review-Journal front page coverage")}<figcaption><b>Las Vegas Review-Journal.</b> Front-page editorial on Night Two.</figcaption></figure>
      <figure>{pic("spokane-coverage.jpg", "Spokane media coverage of Travis Tveit")}<figcaption><b>Spokane.</b> The Inlander followed Iron Goat's Travis Tveit to his third-place finish.</figcaption></figure>
    </div>
    <p class="measure" style="font-size:18px;margin-top:32px">Local media in competing cities followed their chefs to Las Vegas, and Food &amp; Beverage Magazine carried national trade coverage to 12 million monthly readers. Not paid placement. Earned media. Chef Battle was the story.</p>
  </div>
</section>

<section class="section--band bg-navy">
  <div class="wrap"><div class="cb-stats cb-stats--5">{numh}</div></div>
</section>

<section class="section">
  <div class="wrap">
    {head_block("Who Made It Possible", eyebrow="Event Partners")}
    {logo_wall(NATIONALS_PARTNERS, 6)}
  </div>
</section>

<section class="section--band bg-bone">
  <div class="wrap band-grid">
    <div class="stack" style="gap:14px"><h2 class="h2">Ready to Host the Next One?</h2>
      <p style="font-size:18px">Chef Battle Nationals is coming back. If you're interested in sponsoring, hosting, or bringing Chef Battle to your city, let's talk. Chefs: become a League Chef to start your road to the next national stage.</p></div>
    <div class="btn-row">{btn("Get in Touch", cb_mail("Chef Battle Nationals"), "primary", "lg")}{btn("Become a League Chef", "{R}", "secondary", "lg")}</div>
  </div>
</section>'''
    page("chef-battle/nationals/index.html", "Chef Battle Nationals — Las Vegas Recap",
         "Chef Battle Nationals at Hofbräuhaus Las Vegas: 15 city champions, 3 nights, 500 attendees and one National Champion, Mike Pascua.",
         body, active="Nationals")

# ------------------------------------------------------------------
# /chef-battle/operators/
# ------------------------------------------------------------------
def cb_operators():
    how = [("01", "One per market", "One Operator Per City", "We're selecting one approved Chef Battle Local Operator for each market, giving you the exclusive opportunity to lead Chef Battle in your community."),
           ("02", "No event financing", "We Fund Approved Event Expenses", "Hop To It funds the approved event budget so you don't have to finance the event yourself. You focus on execution, not capital."),
           ("03", "Your role", "Follow the Playbook + Execute Locally", "We provide the framework. You use your local relationships to recruit chefs, build sponsor partnerships, promote the event and lead on-the-ground execution."),
           ("04", "Your upside", "Earn 30% of Event Profit", "Hop To It manages event revenue and approved expenses. You receive 30% of the final Event Profit from every Chef Battle event you operate.")]
    T = [("30%", "Of event profit you earn"), ("1", "Operator per city"), ("$149", "Annual operator fee"), ("$0", "Event expenses out of pocket")]
    body = f'''
{cb_hero("Chef Battle · Local Operator Program",
         'Bring Chef Battle<br>to Your City<span class="dot">.</span>',
         "You've seen chef competitions on TV, but there's nothing like experiencing one in person. Chef Battle brings local chefs out from behind the kitchen and puts them center stage, giving communities the chance to discover, celebrate and support the chefs and restaurants in their own backyard.",
         btn("Apply to Become an Operator", OPERATOR_FORM, "primary", "lg", attrs='target="_blank" rel="noopener"') + btn("See How It Works", "#how-it-works", "inverse", "lg"),
         "chef-at-station.jpg", "Chef competing at a Chef Battle station", "center",
         extra='<p class="label" style="color:var(--on-navy-muted)">Lead the experience · Support your community · Share in the success</p>')}
<section class="section--band bg-bone"><div class="wrap">{terms(T)}</div></section>

<section class="section" id="how-it-works" style="scroll-margin-top:76px">
  <div class="wrap">
    {head_block("We've Built the Playbook. You Bring It to Life", eyebrow="How It Works")}
    <p class="measure" style="font-size:18px;margin:-32px 0 48px">You don't need to create an event from scratch or figure out how Chef Battle should work. We've built the brand, competition format and event playbook. You follow the framework and execute it in your local market.</p>
    {numbered(how)}
  </div>
</section>

<div class="wrap"><div class="cb-mosaic cb-mosaic--3">{pic("crowd-night.jpg", "Chef Battle crowd")}{pic("competition-floor.jpg", "Chef Battle competition floor")}{pic("judges.jpg", "Judges tasting at Chef Battle")}</div></div>

<section class="section" id="partnership">
  <div class="wrap">
    {head_block("You're Local. You're Not Alone", eyebrow="The Partnership")}
    <p class="measure" style="font-size:18px;margin:-32px 0 40px">You bring the local knowledge and relationships. We bring everything else.</p>
    <div class="cb-two">
      <div class="cb-col"><div class="eyebrow">What You Bring</div>{ticklist(["Knowledge of your local food and restaurant community", "Relationships with chefs, venues and local businesses", "Ability to recruit local sponsors and partners", "Local marketing and ticket sales support", "Event-day coordination and on-the-ground execution", "The drive to make it happen"])}</div>
      <div class="cb-col cb-col--navy"><div class="eyebrow">What We Provide</div>{ticklist(["The Chef Battle brand and competition format", "Operator onboarding and ongoing support", "Event planning resources and templates", "Brand and creative resources", "Sponsorship materials", "Ticketing infrastructure", "Approved event funding", "Financial reconciliation and profit-sharing"])}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head_block("You Don't Need to Be a Professional Event Producer", eyebrow="Who We're Looking For")}
    <p class="measure" style="font-size:18px;margin:-32px 0 40px">You might work in events, hospitality, food and beverage, sales, marketing or run your own business. Or you may simply know your city, love bringing people together and have the drive to make things happen.</p>
    {traits()}
    <div class="cb-mosaic cb-mosaic--4" style="margin-top:56px">{pic("dishes.jpg", "Plated dishes at Chef Battle")}{pic("salmon.jpg", "Salmon dish at Chef Battle")}{pic("fish.jpg", "Fish dish at Chef Battle")}{pic("cooking.jpg", "Cooking at Chef Battle")}</div>
  </div>
</section>

<section class="section--band bg-bone">
  <div class="wrap">
    <div class="eyebrow" style="margin-bottom:20px">The Terms</div>
    {terms(T)}
  </div>
</section>

<section class="section--band bg-navy">
  <div class="wrap band-grid">
    <div class="stack" style="gap:14px"><h2 class="h2">Ready to Bring Chef Battle to Your Community?</h2>
      <p style="font-size:18px;color:var(--on-navy)">We're reviewing applications for new Chef Battle markets across the country. Tell us about yourself, your community and why you'd be a great person to bring Chef Battle to your city.</p>
      <p class="legal">Outside the United States? See the <a href="{{R}}chef-battle/operators/international/" style="color:#fff">International Operator Program</a>.</p></div>
    {btn("Apply Now", OPERATOR_FORM, "primary", "lg", attrs='target="_blank" rel="noopener"')}
  </div>
</section>'''
    page("chef-battle/operators/index.html", "Become a Chef Battle Local Operator",
         "Bring Chef Battle to your city. One operator per market, $149 annual fee, approved event expenses funded, and 30% of event profit.",
         body, active="Operators")

def cb_operators_intl():
    how = [("01", "One per city", "Exclusive Territory", "We're selecting one approved Chef Battle International Operator per market. You become the person leading Chef Battle in your community."),
           ("02", "Your investment", "You Fund Your Market", "As an International Operator, you fund approved event expenses and manage local event finances. You keep more control, and take more ownership, of your market."),
           ("03", "Your role", "You Lead and Market Locally", "You use your knowledge and relationships to recruit chefs, connect with venues, build sponsorships, promote the event and drive ticket sales."),
           ("04", "Your upside", "You Share in the Profit", "International Operators receive 60% of final Event Profit from the Chef Battle events they operate. Hop To It retains 40%.")]
    T = [("60%", "Of event profit you earn"), ("1", "Approved operator per city"), ("$999 USD", "Annual operator fee*"), ("You fund", "Approved event expenses")]
    body = f'''
{cb_hero("Chef Battle · International Operator Program",
         'Bring Chef Battle<br>to Your City<span class="dot">.</span>',
         "Lead the experience. Build your local food community. Share in the success.",
         btn("Apply Now", INTL_OPERATOR_FORM, "primary", "lg", attrs='target="_blank" rel="noopener"') + btn("See How It Works", "#how-it-works", "inverse", "lg"),
         "outdoor-crowd.jpg", "Chef Battle outdoor evening event", "center")}
<section class="section--band bg-bone"><div class="wrap">{terms(T)}</div></section>

<section class="section" id="how-it-works" style="scroll-margin-top:76px">
  <div class="wrap">
    {head_block("How It Works", eyebrow="The Model")}
    {numbered(how)}
  </div>
</section>

<section class="section bg-bone">
  <div class="wrap">
    <div class="cb-two">
      <div class="cb-col"><div class="eyebrow">Your Role · What You Bring</div>{ticklist(["Local market knowledge and relationships", "Event funding and financial management", "Chef and restaurant recruitment", "Local sponsorship and partnership development", "Local marketing and ticket sales", "Event-day leadership and execution"])}</div>
      <div class="cb-col cb-col--navy"><div class="eyebrow">Our Role · What We Provide</div>{ticklist(["The Chef Battle brand and competition format", "Operator onboarding and support", "Event planning resources and templates", "Brand and creative resources", "Sponsorship materials", "Ticketing infrastructure", "Event standards and operating framework", "Ongoing support from planning through event day"])}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap cb-feature">
    {pic("crowd-night.jpg", "Chef Battle event crowd", "cb-feature-pic")}
    <div class="stack" style="gap:18px">
      <div class="eyebrow">The Experience</div>
      <h2 class="h2">More Than a Local Competition<span class="dot">.</span></h2>
      <p style="font-size:18px">Every Chef Battle celebrates the people behind the local food scene. Guests see chefs outside their restaurants, experience the competition up close, taste their creations and cheer on their favorites. Local winners become City Champions, with the chance to advance through the Chef Battle series and represent their community on a larger stage.</p>
      <p style="font-size:18px">It starts locally. But the competition doesn't have to end there.</p>
    </div>
  </div>
</section>

<section class="section bg-bone">
  <div class="wrap">
    {head_block("Who We're Looking For", eyebrow="The Operator")}
    {traits()}
  </div>
</section>

<section class="section--band">
  <div class="wrap">
    <div class="eyebrow" style="margin-bottom:20px">The Terms</div>
    {terms(T + [("Opportunity", "To grow with Hop To It")], "There are no guaranteed earnings. Your compensation is based on the actual financial performance of your event. *$999 USD annual license fee is per approved market. All market territories, geographic boundaries and regional limits are defined by Chef Battle.")}
  </div>
</section>

<section class="section--band bg-navy">
  <div class="wrap band-grid">
    <div class="stack" style="gap:14px"><h2 class="h2">Ready to Bring Chef Battle to Your City?</h2>
      <p style="font-size:18px;color:var(--on-navy)">We're reviewing applications for new international markets. Tell us about yourself, your community and why Chef Battle belongs where you are.</p>
      <p class="legal">In the United States? See the <a href="{{R}}chef-battle/operators/" style="color:#fff">Local Operator Program</a>.</p></div>
    {btn("Apply to Become an International Operator", INTL_OPERATOR_FORM, "primary", "lg", attrs='target="_blank" rel="noopener"')}
  </div>
</section>'''
    page("chef-battle/operators/international/index.html", "Chef Battle International Operator Program",
         "Bring Chef Battle to your city outside the US. Exclusive territory, 60% of event profit, $999 USD annual operator fee.",
         body, active="Operators")

# ------------------------------------------------------------------
# /chef-battle/team-building/
# ------------------------------------------------------------------
def cb_team():
    data = [("5.3×", "More likely to do their best work when employees feel a sense of belonging", "Salesforce Research"),
            ("23%", "Higher profitability in companies with highly engaged teams", "Gallup, 2024"),
            ("37%", "More productive: the lift from high-engagement team environments", "Harvard Business Review"),
            ("50%", "Lower turnover risk when teams experience genuine workplace belonging", "BetterUp Research")]
    dh = "".join(f'<div class="cb-stat"><div class="v">{v}</div><div class="label">{e(k)}</div><div class="src">{e(s)}</div></div>' for v, k, s in data)
    why = [("01", "Shared stress creates bonds", "Shared Stress Creates Bonds", "PwC research shows that experiences combining meaning and a shared challenge fast-track teams through forming, storming and norming. Bonds that take years to build at a desk happen in a single night."),
           ("02", "Inclusive by design", "Everyone Actually Participates", "Happy hours exclude non-drinkers, parents who can't stay late, and those who don't love bars. A structured culinary experience levels the playing field: every person on the team has a role."),
           ("03", "Culture", "Memories That Last", "Harvard research shows shared experiences increase acceptance, belonging and camaraderie in ways passive social events simply can't. The story of your team cooking under pressure becomes part of your culture.")]
    formats = [
        ("On-Site · Hands-On", "Team Building On-Site", "High-energy. Efficient. Brought to your office.", "Sales kickoffs · Team building · Internal events",
         ["Everyone participates, fully interactive", "All equipment and ingredients provided", "Professional chef host and facilitation"],
         [("Essential", "Up to 20 guests", "$15K"), ("Signature", "Up to 30 guests", "$20K"), ("Premium", "Up to 50 guests", "$30K"), ("Premium Experience", "50+ guests", "$50K+")],
         "Engagement & interaction", ""),
        ("Off-Site · Elevated", "Team Building Off-Site", "Interactive, social, and more immersive.", "Offsites · Leadership retreats · Team celebrations",
         ["Interactive competition format", "Open bar + passed appetizers", "Elevated venue production"],
         [("Essential", "Up to 20 guests", "$25K"), ("Signature", "Up to 30 guests", "$35K"), ("Premium", "Up to 50 guests", "$50K"), ("Premium Experience", "50+ guests", "$75K+")],
         "Team building + atmosphere", ""),
        ("Private · Full Production", "Chef Battle Private Event", "Entertainment-driven. Large-scale. Unforgettable.", "Holiday parties · Annual events · Client entertainment",
         ["Live competition with pro chef teams", "Dedicated MC + stage, AV and lighting", "Open bar, passed apps + chef tastings", "Photography and video included"],
         [("Essential", "Up to 100 guests", "$75K"), ("Signature", "Up to 200 guests", "$100K"), ("Premium", "Up to 300 guests", "$150K"), ("Premium Experience", "300+ guests", "$200K+")],
         "Entertainment + scale", "navy")]
    fh = ""
    for tag, name, line, best, inc, tiers, focus, tone in formats:
        rows = "".join(f'<div class="tier"><span class="n">{e(a)}<small>{e(b)}</small></span><span class="p">{e(c)}</span></div>' for a, b, c in tiers)
        fh += f'''<div class="cb-format{" cb-format--navy" if tone else ""}">
  <span class="badge {"badge--ink-inv" if tone else "badge--ink"}">{e(tag)}</span>
  <div class="t">{e(name)}</div><p class="line">{e(line)}</p>
  <div class="label">Best for</div><p>{e(best)}</p>
  <div class="label">What's included</div>{ticklist(inc)}
  <div class="label">Investment</div><div class="tiers">{rows}</div>
  <div class="focus">Focus: {e(focus)}</div>
</div>'''
    included = [("Challenge Design", "Team-based challenges built around real collaboration dynamics, not just a recipe to follow."),
                ("All Ingredients & Equipment", "Everything your teams need to compete: sourced, prepped and ready to go."),
                ("Setup & Breakdown", "We arrive early and leave clean. Zero logistics burden on your team."),
                ("Professional Host", "An experienced emcee keeps the energy high and the experience moving from start to finish."),
                ("Judging & Awards", "A structured judging process with real scoring, real results and a moment your team won't forget."),
                ("Facilitation", "On-site facilitators make sure every participant is engaged and every team has what they need.")]
    ih = "".join(f'<div class="inc"><div class="num">0{i+1}</div><div class="t">{e(t)}</div><p>{e(b)}</p></div>' for i, (t, b) in enumerate(included))
    body = f'''
{cb_hero("Chef Battle · Corporate Experiences",
         'Your Team Deserves More Than a Happy Hour<span class="dot">.</span>',
         "Chef Battle is a live culinary competition with professional chefs, real pressure and packed crowds. Now we're bringing that same energy directly to your company. The format that fills venues works even better with your team.",
         btn("Request a Proposal", cb_mail("Corporate Team Building Proposal"), "primary", "lg") + btn("See the Formats", "#formats", "inverse", "lg"),
         "cooking.jpg", "Chicken searing in a pan at Chef Battle", "center")}
{strip(["Team Building", "Real Collaboration", "High-Energy Experience", "On-Site & Off-Site", "Fully Managed", "Leadership Offsites", "Sales Kickoffs"])}

<section class="section">
  <div class="wrap">
    <div class="section-head"><div class="eyebrow">Why It Matters · The Data</div><h2 class="h2">The Bonds That Take Years to Build at a Desk Happen in a Single Night<span class="dot">.</span></h2><div class="rule"></div></div>
    <div class="cb-stats cb-stats--light">{dh}</div>
  </div>
</section>

<section class="section bg-bone" id="what-it-is">
  <div class="wrap cb-two">
    <div class="stack" style="gap:16px"><div class="eyebrow">What It Is</div><h2 class="h2 h2--sm">A Team Experience That Actually Works<span class="dot">.</span></h2><div class="rule"></div>
      <p>Chef Battle is more than a cooking competition. It's a structured, high-energy environment where teams collaborate in real time to solve challenges and execute under pressure.</p>
      <p>Participants aren't just following instructions. They're making real decisions, under real constraints, as a real team.</p>
      {ticklist(["Aligning on strategy before time runs out", "Delegating roles based on strengths", "Adapting when things don't go as planned", "Delivering a final outcome as a team"])}</div>
    <div class="stack" style="gap:16px" id="how-it-works"><div class="eyebrow">How It Works</div><h2 class="h2 h2--sm">Built for Collaboration, Not Just Participation<span class="dot">.</span></h2><div class="rule"></div>
      <p>Teams get a shared objective, limited resources and a defined time frame. From there, success depends entirely on how well the team works together.</p>
      <p>Each experience is facilitated end to end, so every team is engaged and every participant plays a meaningful role.</p>
      {ticklist(["Communication under pressure", "Real-time decision-making", "Leadership that emerges organically", "Execution from start to finish"])}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head_block("Designed for Real Team Dynamics", eyebrow="Why Experiences Beat Happy Hours")}
    {numbered(why, 3)}
  </div>
</section>

<section class="section bg-bone" id="formats" style="scroll-margin-top:76px">
  <div class="wrap">
    {head_block("Find Your Format", eyebrow="Three Formats to Fit Any Goal")}
    <p class="measure" style="font-size:18px;margin:-32px 0 40px">Whether your team competes head-to-head or your guests experience a world-class culinary showdown, Chef Battle delivers a fully produced, unforgettable event.</p>
    <div class="cb-formats">{fh}</div>
    <p class="measure" style="margin-top:32px">Goal is team engagement? Choose one of the Team Building experiences. Looking to host and impress at scale? The Private Event is the right fit. Not sure? We'll recommend the best format for your team size, goals and timing.</p>
  </div>
</section>

<section class="section" id="included">
  <div class="wrap">
    {head_block("Fully Managed. End to End", eyebrow="What's Included")}
    <p class="measure" style="font-size:18px;margin:-32px 0 40px">We handle everything, from setup to facilitation, so your team can focus entirely on the experience.</p>
    <div class="grid g-3" style="gap:48px 40px">{ih}</div>
  </div>
</section>

<section class="section bg-navy">
  <div class="wrap cb-two">
    <div class="stack" style="gap:16px"><div class="eyebrow">Customization</div><h2 class="h2 h2--sm">Tailored to Your Team<span class="dot">.</span></h2>
      <p style="color:var(--on-navy)">Each experience can be built to reflect your organization's culture, values and goals, not a generic off-the-shelf package.</p>
      {ticklist(["Branded materials and team stations", "Custom challenge themes tied to company goals", "Integration of company values or messaging", "Optional takeaways and custom awards"]).replace('cb-list"', 'cb-list cb-list--inv"')}</div>
    <div class="stack" style="gap:16px"><div class="eyebrow">Where It Fits Best</div><h2 class="h2 h2--sm">Ideal Use Cases<span class="dot">.</span></h2>
      {ticklist(["Team building days and company retreats", "Sales meetings and annual kickoffs", "Leadership offsites and executive programs", "Departmental alignment sessions", "New hire onboarding and orientation", "Client entertainment and partner events"]).replace('cb-list"', 'cb-list cb-list--inv"')}</div>
  </div>
</section>

<section class="section--band bg-bone">
  <div class="wrap band-grid">
    <div class="stack" style="gap:14px"><div class="eyebrow">Next Steps</div><h2 class="h2">Let's Plate Your Event<span class="dot">.</span></h2>
      <p style="font-size:18px">Tailored to your team, venue and vision. Every proposal starts with a conversation, and we'll recommend the right format for your goals.</p></div>
    {btn("Request a Proposal", cb_mail("Corporate Team Building Proposal Request"), "primary", "lg")}
  </div>
</section>'''
    page("chef-battle/team-building/index.html", "Corporate Team Building — Chef Battle",
         "Chef Battle corporate team building: on-site, off-site and private event formats, fully managed end to end. Request a proposal.",
         body, active="Team Building")

def chef_battle_pages():
    cb_home(); cb_nationals(); cb_operators(); cb_operators_intl(); cb_team()
