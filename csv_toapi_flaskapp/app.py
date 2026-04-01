from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "flask_frontend_secret"

API_BASE = "http://localhost:8000"


def api_get(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI. Make sure it is running on port 8000."
    except Exception as e:
        return None, str(e)


def api_post(path):
    try:
        r = requests.post(f"{API_BASE}{path}", timeout=10)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI. Make sure it is running on port 8000."
    except Exception as e:
        return None, str(e)


# ── HOME / DASHBOARD ─────────────────────────────────────────────────────────
@app.route("/")
def dashboard():
    # students, err = api_get("/db/students")
    # if err:
    #     return render_template("error.html", message=err)

    # total = len(students)
    # avg_age = round(sum(s["age"] for s in students if s["age"]) / total, 1) if total else 0
    # avg_gpa = round(sum(s["gpa"] for s in students if s["gpa"]) / total, 2) if total else 0
    # paid    = sum(1 for s in students if s.get("status") == "Paid")
    # pending = total - paid

    # majors = {}
    # for s in students:
    #     m = s.get("major") or "Unknown"
    #     majors[m] = majors.get(m, 0) + 1
    # top_majors = sorted(majors.items(), key=lambda x: x[1], reverse=True)[:5]

    # cities = {}
    # for s in students:
    #     c = s.get("city") or "Unknown"
    #     cities[c] = cities.get(c, 0) + 1
    # top_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)[:5]

    # return render_template("dashboard.html",
    #     total=total, avg_age=avg_age, avg_gpa=avg_gpa,
    #     paid=paid, pending=pending,
    #     top_majors=top_majors, top_cities=top_cities
    # )
    return render_template("base.html")

# ── VIEW ALL STUDENTS ─────────────────────────────────────────────────────────
@app.route("/students")
def students():
    data, err = api_get("/db/students")
    if err:
        return render_template("error.html", message=err)
    return render_template("students.html", students=data, total=len(data))


# ── FILTER / SEARCH ───────────────────────────────────────────────────────────
@app.route("/filter", methods=["GET", "POST"])
def filter_students():
    results = None
    count   = None
    form    = {}

    if request.method == "POST":
        form = request.form.to_dict()
        params = {}
        for key in ["age_gt", "age_lt", "gpa_gt", "gpa_lt", "min_scholarship"]:
            if form.get(key, "").strip():
                params[key] = form[key].strip()
        for key in ["major", "status", "city"]:
            if form.get(key, "").strip():
                params[key] = form[key].strip()

        results, err = api_get("/db/students", params=params)
        if err:
            return render_template("error.html", message=err)
        count = len(results)

    return render_template("filter.html", results=results, count=count, form=form)


# ── SEED PAGE ─────────────────────────────────────────────────────────────────
@app.route("/seed", methods=["GET", "POST"])
def seed():
    result = None
    db_status = None

    # Always check DB first
    status_data, err = api_get("/check_db")
    if err:
        return render_template("error.html", message=err)
    db_status = status_data.get("status")

    if request.method == "POST":
        result, err = api_post("/db/seed")
        if err:
            flash(f"Error: {err}", "danger")
        else:
            flash(f"Done! Inserted {result['inserted']} rows, skipped {result['skipped']} existing.", "success")

    return render_template("seed.html", db_status=db_status, result=result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
