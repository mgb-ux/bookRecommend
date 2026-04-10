# ------------------------------------------
# import dependencies and Flask set up
# ------------------------------------------
import requests
import time
import json
import os
import hashlib

from flask import Flask, render_template, request
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)

# -------------------------
# Sets up file-based caching
# -------------------------
CACHE_DIR = "api_cache"
CACHE_TTL = 60 * 60 * 24  # 24 hours

os.makedirs(CACHE_DIR, exist_ok=True)

def cache_key(url, params):
    raw = url + json.dumps(params or {}, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()

# -------------------------
# Sets up session retries
# -------------------------
def create_session():
    session = requests.Session()

    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session

session = create_session()

# -------------------------
# Cached GET request
# -------------------------
def cached_get(url, params=None, timeout=10):
    key = cache_key(url, params)
    path = os.path.join(CACHE_DIR, key + ".json")

    # Use cache if valid
    if os.path.exists(path):
        age = time.time() - os.path.getmtime(path)
        if age < CACHE_TTL:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    # -----------------
    # Otherwise fetch
    # -----------------
    response = session.get(url, params=params, timeout=timeout)
    response.raise_for_status()

    data = response.json()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    return data

# -----------------------
# Flask route
# ------------------------
@app.route("/", methods=["GET", "POST"])
def search_books():
    # Connects to index.html 
    if request.method == "GET":
        return render_template("index.html")

    user_query = request.form.get("book_title")
    if not user_query:
        return render_template(
            "index.html",
            error="Please enter a book title."
        )

    # -------------------------
    # Searches based on user input and checks for errors
    # -------------------------
    try:
        search_data = cached_get(
            "https://openlibrary.org/search.json",
            {"q": user_query}
        )
    except requests.RequestException:
        return render_template(
            "index.html",
            error="Unable to connect to Open Library right now."
        )

    docs = search_data.get("docs", [])
    if not docs:
        return render_template(
            "index.html",
            error="No books found."
        )
    # ------------------------------
    # Retrieves work key from book
    # ------------------------------
    book = docs[0]
    original_title = book.get("title")
    work_key = book.get("key")

    if not work_key:
        return render_template(
            "index.html",
            error="Could not retrieve book details."
        )

    # -------------------------
    # Fetches work details to get subjects
    # -------------------------
    try:
        work_data = cached_get(
            f"https://openlibrary.org{work_key}.json"
        )
    except requests.RequestException:
        return render_template(
            "index.html",
            error="Failed to load book information."
        )

    subjects = work_data.get("subjects", [])
    if not subjects:
        return render_template(
            "index.html",
            error="This book has no subjects to match on."
        )

    # -------------------------
    # Filters subjects
    # -------------------------
    def is_good_subject(s):
        bad = {"fiction", "novels", "literature", "books"}
        return isinstance(s, str) and len(s) > 10 and s.lower() not in bad

    selected_subjects = [s for s in subjects if is_good_subject(s)]
    if not selected_subjects:
        selected_subjects = subjects

    selected_subjects = selected_subjects[:12]

    # -------------------------
    # Searches by those subjects
    # -------------------------
    candidates = {}

    for subject in selected_subjects:
        try:
            subject_data = cached_get(
                "https://openlibrary.org/search.json",
                {"q": f"subject:{subject}", "limit": 20}
            )
        except requests.RequestException:
            continue

        for item in subject_data.get("docs", []):
            key = item.get("key")
            if not key:
                continue

            if key not in candidates:
                candidates[key] = {
                    "item": item,
                    "hits": 0
                }

            candidates[key]["hits"] += 1

    # -------------------------
    # Compiles information of recommendations
    # -------------------------
    recommendations = []

    for key, entry in candidates.items():
        item = entry["item"]
        title = item.get("title")

        if not title or title == original_title:
            continue

        recommendations.append({
            "title": title,
            "authors": ", ".join(
                item.get("author_name", ["Unknown author"])
            ),
            "score": entry["hits"],
            "cover_id": item.get("cover_i"),
            "url": f"https://openlibrary.org{key}"
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    recommendations = recommendations[:15]

    return render_template(
        "index.html",
        original=original_title,
        recommendations=recommendations
    )

# --------------------------
# Runs the app
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)