from flask import Flask, render_template_string, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "demo-change-this-key")

BASE = r"""
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title or 'Kindred Impact' }}</title><link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script></head><body>
<header class="topbar"><a class="brand" href="/">✿ Kindred<span>Impact</span></a><nav>
<a href="/">Home</a><a href="/programs">Programs & training</a><a href="/events">Events</a><a href="/food">Food support</a><a href="/about">About</a><a href="/feedback">Feedback</a><a class="nav-cta" href="/volunteer">Volunteer ↗</a></nav></header>
{% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}<div class="flash-wrap">{% for cat,msg in messages %}<div class="flash {{cat}}">{{msg}}</div>{% endfor %}</div>{% endif %}{% endwith %}
<main>{{ content|safe }}</main><footer><b>✿ Kindred Impact</b><p>Small acts. Stronger communities.</p><small>Community impact demo website</small></footer></body></html>
"""

HOME = r"""
<section class="hero"><div><div class="eyebrow">● COMMUNITY, IN ACTION</div><h1>A little kindness<br>goes <em>a long way.</em></h1><p class="lead">Bring your time, your skills, or simply your heart. Together, we can turn small acts into lasting change.</p><div class="actions"><a class="button" href="/volunteer">Become a volunteer ↗</a><a class="textlink" href="/programs">Explore programs →</a></div><div class="proof">☺　✿　♡　<strong>128 changemakers</strong> and counting</div></div>
<div class="art"><div class="sun"></div><div class="flower">✿</div><h3>GOOD THINGS<br>GROW HERE</h3><span class="sticker one">🌱 Grow together</span><span class="sticker two">♡ Give with heart</span></div></section>
<section class="stats"><article><small>Active volunteers</small><strong>128</strong><span>People showing up 💜</span></article><article><small>Programs running</small><strong>12</strong><span>More ways to make change</span></article><article><small>Community events</small><strong>8</strong><span>Meet, help, connect</span></article><article><small>Meals supported</small><strong>2,450</strong><span>Care served with dignity</span></article></section>
<section class="section"><div class="heading"><div><div class="eyebrow">THE BIGGER PICTURE</div><h2>Impact, at a glance.</h2></div><span class="pill">● Demo dashboard</span></div><div class="charts"><div class="panel"><h3>Volunteer momentum</h3><p>Monthly volunteer sign-ups</p><canvas id="vChart"></canvas></div><div class="panel"><h3>Where we make a difference</h3><p>Program participation share</p><canvas id="pChart"></canvas></div></div></section>
<section class="section"><div class="heading"><div><div class="eyebrow">FIND YOUR WAY IN</div><h2>Good work, many ways.</h2></div><a class="textlink" href="/programs">All programs →</a></div><div class="cards">
<a class="feature lavender" href="/programs"><span>📚</span><small>LEARN & SHARE</small><h3>Skills for tomorrow</h3><p>Help learners build confidence, skills, and brighter possibilities.</p><b>Explore training ↗</b></a>
<a class="feature butter" href="/food"><span>🥣</span><small>CARE & NOURISH</small><h3>Food with dignity</h3><p>Support community meals and make sure no one feels forgotten.</p><b>See food support ↗</b></a>
<a class="feature mint" href="/events"><span>🌿</span><small>MEET & DO</small><h3>Show up together</h3><p>Join friendly events where every helping hand matters.</p><b>Find an event ↗</b></a></div></section>
<section class="cta"><div><div class="eyebrow">YOUR NEXT CHAPTER STARTS HERE</div><h2>Have an hour? You have an impact.</h2><p>Bring what you can. We’ll find a way to make it count.</p></div><a class="button dark" href="/volunteer">Join the community ↗</a></section>
<script>
if(window.Chart){
new Chart(document.getElementById('vChart'),{type:'line',data:{labels:['May','Jun','Jul','Aug','Sep','Oct'],datasets:[{data:[14,19,24,21,28,22],label:'New volunteers',borderColor:'#7356d8',backgroundColor:'rgba(115,86,216,.12)',fill:true,tension:.35,borderWidth:3}]},options:{plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:'#eeeaf4'}},x:{grid:{display:false}}}}});
new Chart(document.getElementById('pChart'),{type:'doughnut',data:{labels:['Education','Food Support','Environment','Health'],datasets:[{data:[42,28,18,12],backgroundColor:['#7356d8','#f2a56f','#80c7ae','#f0cc65'],borderWidth:0}]},options:{cutout:'68%',plugins:{legend:{position:'bottom'}}}});
}</script>
"""

def page(title, intro, cards):
    parts = [f'<section class="pagehero"><div class="eyebrow">KINDRED IMPACT · COMMUNITY</div><h1>{title}</h1><p>{intro}</p></section><section class="cards">']
    for emoji, heading, desc, tag in cards:
        parts.append(f'<article class="contentcard"><span>{emoji}</span><h3>{heading}</h3><p>{desc}</p><small class="tag">{tag}</small></article>')
    parts.append('</section><section class="cta"><div><div class="eyebrow">MAKE IT MEAN SOMETHING</div><h2>There’s a place for you here.</h2><p>Join in with your time, your ideas, or your willingness to learn.</p></div><a class="button dark" href="/volunteer">Volunteer ↗</a></section>')
    return ''.join(parts)

PAGES = {
    "/programs": ("Programs & training", "Build confidence, practical skills, and community connections.", [
        ("💻","Digital basics","Practise computer basics, online safety, and everyday digital tools.","BEGINNER"),
        ("🗣️","Communication & confidence","Friendly sessions for speaking, collaboration, and interview preparation.","ALL LEVELS"),
        ("🌱","Volunteer orientation","Learn to contribute respectfully and support community activities.","START HERE")]),
    "/events": ("Events that bring us together", "Good people, good energy, and practical ways to help. Come as you are.", [
        ("🌿","Community clean-up","Help care for a shared public space with a local team.","COMING SOON"),
        ("📚","Learning circle","Support a friendly peer-learning session for learners.","WEEKEND"),
        ("🥫","Community pantry day","Sort essentials and help prepare food-support packs.","VOLUNTEER")]),
    "/food": ("Nourishment is a community effort", "Support access to food with dignity and care.", [
        ("🥣","Community meals","Coordinate meal distribution with trusted community partners.","CARE"),
        ("🧺","Pantry essentials","Help organise staple food items and useful essentials.","SUPPORT"),
        ("🤝","Partner with us","Connect a community group or organisation with this initiative.","CONNECT")]),
    "/about": ("A kinder community starts with us", "Kindred Impact is a community initiative concept to discover programs, join events, volunteer, and track collective progress.", [
        ("💜","People first","Everyone deserves to feel seen, respected, and included.","VALUES"),
        ("🌼","Small steps count","Consistent, practical acts can build meaningful change over time.","PURPOSE"),
        ("🔎","Open and accountable","We aim to make activities and progress easy to understand.","TRANSPARENCY")])
}

def render(content, title="Kindred Impact"):
    return render_template_string(BASE, content=content, title=title)

@app.route("/")
def home():
    return render(HOME, "Home · Kindred Impact")

@app.route("/programs")
def programs():
    title, intro, cards = PAGES["/programs"]
    return render(page(title, intro, cards), title)

@app.route("/events")
def events():
    title, intro, cards = PAGES["/events"]
    return render(page(title, intro, cards), title)

@app.route("/food")
def food():
    title, intro, cards = PAGES["/food"]
    return render(page(title, intro, cards), title)

@app.route("/about")
def about():
    title, intro, cards = PAGES["/about"]
    return render(page(title, intro, cards), title)

@app.route("/profile")
def profile():
    return redirect(url_for("volunteer"))

@app.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        interest = request.form.get("interest", "").strip()
        if name and email and interest:
            flash(f"Thanks, {name}! Your registration was submitted in this demo.", "success")
            return redirect(url_for("volunteer"))
        flash("Please complete all required fields.", "error")
    content = r"""
    <section class="pagehero"><div class="eyebrow">YOUR COMMUNITY PROFILE</div><h1>Show up as you are.</h1><p>Every volunteer brings something different. Tell us what you’re interested in and find a way to contribute.</p></section>
    <div class="two-col"><aside class="panel profile"><div class="bigicon">✿</div><span class="tag">COMMUNITY MEMBER</span><h2>Your profile starts here</h2><p>This demo profile is ready to personalise. Registration information is not saved to an account or database.</p><div class="line">Interests <span>Choose in the form →</span></div><div class="line">Availability <span>Flexible</span></div><div class="line">Experience <span>All levels welcome</span></div></aside>
    <section class="panel"><h2>Volunteer registration</h2><p>Share a few details to register your interest. Demo only — no data is stored.</p><form method="post">
    <label for="name">Your name</label><input id="name" name="name" required placeholder="Your name">
    <label for="email">Email address</label><input id="email" name="email" type="email" required placeholder="you@example.com">
    <label for="interest">What would you like to help with?</label><select id="interest" name="interest" required><option value="">Choose an area</option><option>Education & training</option><option>Food support</option><option>Community events</option><option>Environment</option><option>Anything that helps</option></select>
    <label for="availability">Availability</label><select id="availability" name="availability"><option>Weekends</option><option>Weekday mornings</option><option>Weekday afternoons</option><option>Flexible</option></select>
    <label for="note">Anything else? (optional)</label><textarea id="note" name="note" rows="3" placeholder="Skills, questions, or ideas..."></textarea>
    <button class="button submit" type="submit">Send my interest ↗</button></form></section></div>"""
    return render(content, "Volunteer registration")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()
        if name and message:
            flash(f"Thank you, {name}! Your feedback was received in this demo.", "success")
            return redirect(url_for("feedback"))
        flash("Please add your name and feedback.", "error")
    content = r"""
    <section class="pagehero"><div class="eyebrow">HELP US GROW</div><h1>Your voice matters.</h1><p>Tell us what feels useful, what could be better, or what you’d love to see next.</p></section>
    <div class="two-col"><section class="panel"><h2>Share your feedback</h2><p>This is a demo form; messages are not stored permanently.</p><form method="post">
    <label for="name">Your name</label><input id="name" name="name" required placeholder="Your name">
    <label for="rating">How was your experience?</label><select id="rating" name="rating"><option>Loved it — 5/5</option><option>Really good — 4/5</option><option>It's okay — 3/5</option><option>Needs work — 2/5</option><option>Not great — 1/5</option></select>
    <label for="message">Your thoughts</label><textarea id="message" name="message" rows="5" required placeholder="I'd love to see..."></textarea>
    <button class="button submit" type="submit">Submit feedback ↗</button></form></section><aside class="panel"><div class="bigicon">♡</div><h2>Good feedback makes good work better.</h2><p>Have an idea for a new program, a more accessible event, or a smoother volunteer experience? We’re listening.</p><div class="notice">Be kind, be honest, and share only information you’re comfortable providing.</div></aside></div>"""
    return render(content, "Feedback")

if __name__ == "__main__":
    # Run with: python app.py
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
