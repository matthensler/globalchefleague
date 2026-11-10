# Chef Relief page — loaded by build.py (exec'd into its namespace).
# Brand: Chef Relief uses core red, ink and white (no navy). It leads fundraising
# and chef-assistance communications, endorsed as part of the Global Chef League family.
#
# Edit the copy below; DONATE_LINK can be swapped for a real donation page later.

CR_IMG = "assets/img/chef-relief/"
DONATE_LINK = None          # e.g. a Stripe donation link. None = "Donate" emails us instead.
ASSIST_LINK = None          # e.g. a Google Form for assistance requests. None = email.

def chef_relief_page():
    from urllib.parse import quote
    def mail(subject):
        return f"mailto:{CONTACT_EMAIL}?subject={quote(subject)}"
    donate = DONATE_LINK or mail("Chef Relief donation")
    assist = ASSIST_LINK or mail("Chef Relief assistance request")
    helps = [("Emergency financial assistance", "Direct support for chefs hit by an unexpected hardship, when they need it most."),
             ("Essential expenses covered", "Help with the essential costs that can't wait while a chef gets back on their feet."),
             ("Back to the kitchen", "The goal is stability, so chefs can keep cooking and continue the careers they've built.")]
    hh = "".join(f'<div class="cr-help"><div class="num">0{i+1}</div><div class="t">{e(t)}</div><p>{e(b)}</p></div>' for i, (t, b) in enumerate(helps))
    steps = [("Reach out", "Email us with a short note about your situation and how to reach you."),
             ("We follow up", "Our team gets in touch to learn more about what you need."),
             ("Review and support", "Requests are reviewed, and assistance is provided based on available funds.")]
    sh = "".join(f'<div class="cr-step"><span class="num">{i+1}</span><div><div class="t">{e(t)}</div><p>{e(b)}</p></div></div>' for i, (t, b) in enumerate(steps))
    body = f'''<div class="cr-page">
<section class="cr-hero">
  <div class="wrap cr-hero-grid">
    <div class="stack-lg">
      <div class="eyebrow">Part of the Global Chef League family</div>
      <h1 class="h-hero">Chefs Take Care of Everyone<span class="dot">.</span><br><span class="cr-red">Chef Relief Takes Care of Chefs.</span></h1>
      <p class="cr-sub">Chef Relief provides emergency financial assistance to chefs facing unexpected hardship, helping cover essential expenses so they can regain stability and continue their careers.</p>
      <div class="btn-row">{btn("Support Chef Relief", "#support", "primary", "lg")}{btn("Request Assistance", "#assistance", "inverse", "lg")}</div>
    </div>
    <div class="cr-logo"><img src="{{R}}{CR_IMG}chef-relief-logo-white.png" alt="Chef Relief" width="600" height="438"></div>
  </div>
</section>

<section class="section">
  <div class="wrap roster-head">
    <div class="stack"><div class="eyebrow">Our Mission</div><h2 class="h2">Care, Built Into the League<span class="dot">.</span></h2><div class="rule"></div></div>
    <div class="stack" style="gap:14px">
      <p style="font-size:19px;color:var(--ink)">Chefs spend their careers feeding their communities, often in an industry with thin margins and little safety net. One unexpected setback can put everything they've built at risk.</p>
      <p>Chef Relief is Global Chef League's charitable program. It exists so that when a chef hits a hard moment, the culinary community can step in and help them get through it.</p>
    </div>
  </div>
</section>

<section class="section bg-bone">
  <div class="wrap">
    {head_block("How Chef Relief Helps", eyebrow="What We Do")}
    <div class="cr-helps">{hh}</div>
  </div>
</section>

<section class="section cr-ink" id="assistance" style="scroll-margin-top:76px">
  <div class="wrap cr-two">
    <div class="stack" style="gap:18px">
      <div class="eyebrow">For Chefs</div>
      <h2 class="h2">Need Help<span class="dot">?</span></h2>
      <p class="cr-sub" style="font-size:18px">If you're a chef facing an unexpected hardship, such as an illness or injury, a sudden loss of work, or a family emergency, we want to hear from you.</p>
      {btn("Request Assistance", assist, "primary", "lg")}
      <p class="legal cr-legal">Assistance is subject to review and available funds and is not guaranteed.</p>
    </div>
    <div class="cr-steps">{sh}</div>
  </div>
</section>

<section class="section" id="support" style="scroll-margin-top:76px">
  <div class="wrap">
    {head_block("Support Chef Relief", eyebrow="How You Can Help")}
    <div class="cr-ways">
      <div class="cr-way cr-way--red">
        <div class="t">Give</div>
        <p>Every contribution goes toward helping a chef cover essential expenses during a hard moment.</p>
        {btn("Donate to Chef Relief", donate, "inverse", "lg")}
      </div>
      <div class="cr-way">
        <div class="t">Partner</div>
        <p>Brands and organizations can support chefs by partnering with Chef Relief on fundraising and campaigns.</p>
        {btn("Partner With Us", mail("Chef Relief partnership"), "secondary", "lg")}
      </div>
      <div class="cr-way">
        <div class="t">Spread the Word</div>
        <p>Know a chef who's going through something? Share this page so they know help is out there.</p>
        {btn("Contact Chef Relief", mail("Chef Relief"), "secondary", "lg")}
      </div>
    </div>
  </div>
</section>

<section class="section--band bg-bone">
  <div class="wrap band-grid">
    <div class="stack" style="gap:12px">
      <img src="{{R}}{CR_IMG}chef-relief-logo.png" alt="Chef Relief" width="160" height="117" style="width:160px;height:auto">
      <p style="font-size:18px">Chef Relief is part of the Global Chef League family, alongside Chef Battle and the World Chef Cup.</p>
    </div>
    <div class="btn-row">{btn("Become a League Chef", "{R}", "primary", "lg")}{btn("Explore Chef Battle", "{R}chef-battle/", "secondary", "lg")}</div>
  </div>
</section>
</div>'''
    page("chef-relief/index.html", "Chef Relief — Emergency Assistance for Chefs",
         "Chef Relief provides emergency financial assistance to chefs facing unexpected hardship, helping cover essential expenses so they can regain stability and continue their careers.",
         body, active="Chef Relief")
