# "86 The Fees" sweepstakes — loaded by build.py (exec'd into its namespace).
# Page: /sweepstakes/   Official Rules: /sweepstakes/rules/ (from content/86-the-fees-rules.md)
#
# SWEEP_FORM: paste the Google Form link here once it's made (the "Send > link" URL).
#   None = the entry section shows a "form opens soon" card instead of the form.
SWEEP_FORM = None
# SWEEP_EMBED: paste the sweepstakes software's embed code here (a """...""" string). Takes priority over SWEEP_FORM.
SWEEP_EMBED = None
SWEEP_SHARE = "assets/img/share/share-86-the-fees.jpg"

def sweepstakes_pages():
    rules = "{R}sweepstakes/rules/"
    enter = "#enter"
    if SWEEP_EMBED:
        form = f'<div class="sw-form sw-form--embed">{SWEEP_EMBED}</div>'
    elif SWEEP_FORM:
        src = SWEEP_FORM.split("?")[0]
        src = src.replace("/viewform", "") + "/viewform?embedded=true"
        form = (f'<div class="sw-form"><iframe src="{e(src)}" title="86 The Fees sweepstakes entry form" loading="lazy">Loading…</iframe></div>'
                f'<p class="legal" style="margin-top:12px">Form not loading? <a href="{e(SWEEP_FORM)}" target="_blank" rel="noopener">Open the entry form in a new tab</a>.</p>')
    else:
        form = ('<div class="sw-form sw-form--soon"><div class="eyebrow">Entry Form</div>'
                '<div class="t">Entries Open November 15<span class="dot">.</span></div>'
                f'<p>The entry form will appear right here. Questions? Email <a href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a>.</p></div>')
    legal = ('No purchase or donation necessary. A purchase or donation will not increase your chances of winning. '
             'Void where prohibited. Open to legal residents of the 50 U.S. and D.C., 18 and older. Sweepstakes runs November 15 to December 14, 2026 (Pacific Time). See <a href="' + rules + '">Official Rules</a> '
             'for entry deadlines, prize details, and winner selection.')
    movement = [("Compete", "Take on fellow chefs in Chef Battle and pursue the World Chef Cup."),
                ("Connect", "Build your professional profile and become part of a global culinary community."),
                ("Get Recognized", "Showcase your talent and discover upcoming culinary awards."),
                ("Discover", "Explore Industry Night specials and hospitality perks as the program expands.")]
    mv = "".join(f'<div class="pillar"><div class="num">0{i+1}</div><h3 class="h3">{e(t)}</h3><p>{e(b)}</p></div>' for i, (t, b) in enumerate(movement))
    body = f'''
<section class="bg-navy sw-hero">
  <div class="wrap sw-hero-grid">
    <div class="stack-lg">
      <span class="badge badge--brand badge--capsule">Sweepstakes · Enter to Win</span>
      <h1 class="sw-title"><span class="sw-86">86</span><span class="sw-fees">The Fees!</span></h1>
      <p class="sw-kicker">86 Winners. Zero Membership Fees.</p>
      <p>Enter the 86 The Fees Sweepstakes, made for chefs. We're giving away 86 FREE Global Chef League memberships, and entering is free!</p>
      <p class="sw-dates">Enter November 15 – December 14, 2026</p>
      <div class="btn-row">{btn("Enter to Win", enter, "primary", "lg")}{btn("Sweepstakes Rules", rules, "inverse", "lg")}</div>
    </div>
    <div class="sw-ticket" aria-label="86 free memberships: 10 lifetime and 76 one-year">
      <div class="top"><span>Free Memberships</span><span class="badge badge--brand">Sweepstakes</span></div>
      <div class="sw-ticket-num">86</div>
      <div class="sw-ticket-split">
        <div><span class="n gold">10</span><span class="l">Lifetime</span></div>
        <div><span class="n">76</span><span class="l">One-Year</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="roster-head">
      <div class="stack"><div class="eyebrow">The Prizes</div><h2 class="h2">86 Chances to Join<span class="dot">.</span></h2><div class="rule"></div></div>
      <p style="font-size:18px">10 lucky winners will score a Lifetime Membership, while 76 additional winners will receive a FREE One-Year Membership. That's 86 chances to join a growing global community of chefs, compete in Chef Battle, showcase your culinary talent, and connect with the industry.</p>
    </div>
    <div class="sw-prizes">
      <div class="sw-prize sw-prize--gold">
        <div class="sw-prize-num">10</div>
        <div><div class="t">Lifetime Memberships</div><p>Never pay annual membership dues again.</p></div>
      </div>
      <div class="sw-prize">
        <div class="sw-prize-num">76</div>
        <div><div class="t">One-Year Memberships</div><p>Enjoy a full year of Global Chef League membership on us.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section bg-bone" id="enter" style="scroll-margin-top:76px">
  <div class="wrap sw-enter">
    <div class="stack" style="gap:18px">
      <div class="eyebrow">Enter to Win</div>
      <h2 class="h2">Your Table Is Waiting<span class="dot">.</span></h2>
      <p class="sw-kicker-dark">Enter the 86 The Fees Sweepstakes</p>
      <div class="rule"></div>
      <p style="font-size:18px">Whether you're a seasoned chef, an emerging culinary talent, or ready to step into the competition, there's a place for you in the League.</p>
      <p style="font-size:18px;color:var(--ink)"><strong>Enter for your chance to win. It only takes a minute.</strong></p>
      <p class="legal">{legal}</p>
    </div>
    <div>{form}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head_block("More Than a Membership. It's a Movement", eyebrow="Why Global Chef League")}
    <p class="measure" style="font-size:18px;margin:-32px 0 48px">Global Chef League is bringing chefs together through culinary competitions, professional recognition, industry connections, and opportunities to grow.</p>
    <div class="grid g-4">{mv}</div>
  </div>
</section>

<section class="section--band bg-navy">
  <div class="wrap band-grid">
    <div class="stack" style="gap:14px">
      <h2 class="h2">The League Is Just Getting Started<span class="dot">.</span></h2>
      <p style="font-size:18px;color:var(--on-navy)">86 winners. Will you be one of them?</p>
      <p class="legal">{legal}</p>
    </div>
    {btn("Enter to Win", enter, "primary", "lg")}
  </div>
</section>'''
    page("sweepstakes/index.html", "86 The Fees Sweepstakes: Win a Free Chef Membership",
         "Enter the 86 The Fees Sweepstakes for a chance to win one of 86 free Global Chef League memberships: 10 Lifetime and 76 One-Year. No purchase necessary.",
         body, image=SWEEP_SHARE, crumbs=[("Home", ""), ("86 The Fees Sweepstakes", "sweepstakes/")])

    src = Path(__file__).parent / "content" / "86-the-fees-rules.md"
    if src.exists():
        content = md_to_html(src.read_text(encoding="utf-8"), subheads=True)
        rb = f'''
<section class="bg-navy page-hero" style="padding:72px 0"><div class="wrap"><div class="eyebrow" style="margin-bottom:14px">Global Chef League Sweepstakes</div><h1 class="h1 h1--sm">Official Rules<span class="dot">.</span></h1></div></section>
<section class="section--md"><div class="wrap legal-body">{content}<p style="margin-top:32px"><a href="{{R}}sweepstakes/">Back to the sweepstakes</a></p></div></section>'''
        page("sweepstakes/rules/index.html", "Global Chef League Sweepstakes: Official Rules",
             "Official Rules for the Global Chef League Sweepstakes: 86 free memberships, November 15 to December 14, 2026. No purchase necessary.", rb, image=SWEEP_SHARE,
             crumbs=[("Home", ""), ("86 The Fees Sweepstakes", "sweepstakes/"), ("Official Rules", "sweepstakes/rules/")])
