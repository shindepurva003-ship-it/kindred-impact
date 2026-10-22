# Kindred Impact — Ready-to-run website

## Quick start (Windows)
1. Extract this ZIP into a folder.
2. Open that folder in VS Code.
3. In the VS Code terminal run:
   `py -m pip install -r requirements.txt`
4. Then run:
   `py app.py`
5. Open http://127.0.0.1:5000

If `py` does not work, try `python -m pip install -r requirements.txt` and `python app.py`.

The app has a single `app.py` with embedded HTML templates to avoid missing-template errors. CSS is in `static/style.css`.
Forms are demo-only and do not save data. Dashboard graphs use sample data.
