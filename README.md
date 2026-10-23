# Community Impact Hub

A responsive Flask website concept for a community / volunteer initiative. Includes a home dashboard with charts, programs and training, events, food support, volunteer registration, profile, about, and feedback pages.

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the website:
   ```bash
   python app.py
   ```
6. Visit http://127.0.0.1:5000

## Included files
- `app.py` — Flask routes and demo dashboard data
- `requirements.txt` — Python dependency
- `templates/base.html` — shared layout/navigation
- `templates/dashboard.html` — home dashboard with graphs
- `templates/profile.html` — profile and volunteer registration
- `templates/style.css` — shared styles (also copied to `static/style.css`)
- `templates/events.html` — upcoming events
- `templates/food.html` — food support program
- `templates/training.html` — programs and training
- `templates/about.html` — about page
- `templates/feedback.html` — feedback form

## Note
This is a demo starter project. Forms display confirmation messages but are not connected to a database, email service, or authentication system. Replace the demo statistics with real data before publishing.
