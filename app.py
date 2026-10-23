from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Demo data for the dashboard. Replace with database queries for production.
STATS = {"volunteers": 128, "programs": 12, "events": 8, "meals_served": 2450}
MONTHS = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]
VOLUNTEERS_BY_MONTH = [14, 19, 24, 21, 28, 22]
PROGRAM_PARTICIPATION = {"Education": 42, "Food Support": 28, "Environment": 18, "Health": 12}

@app.route("/")
def home():
    return render_template("dashboard.html", stats=STATS,
                           months=MONTHS, volunteer_data=VOLUNTEERS_BY_MONTH,
                           program_labels=list(PROGRAM_PARTICIPATION.keys()),
                           program_data=list(PROGRAM_PARTICIPATION.values()))

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/programs")
def programs():
    return render_template("training.html")

@app.route("/events")
def events():
    return render_template("events.html")

@app.route("/food")
def food():
    return render_template("food.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()
        rating = request.form.get("rating", "5")
        if not name or not message:
            flash("Please add your name and feedback before submitting.", "error")
        else:
            # Demo only: no database/email is connected.
            flash(f"Thank you, {name}! Your feedback was received in this demo.", "success")
            return redirect(url_for("feedback"))
    return render_template("feedback.html")

@app.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        interest = request.form.get("interest", "").strip()
        if name and email and interest:
            flash(f"Thanks, {name}! Your volunteer registration was submitted in this demo.", "success")
            return redirect(url_for("volunteer"))
        flash("Please complete all fields.", "error")
    return render_template("profile.html", registration=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)