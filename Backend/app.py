from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, timezone
from database import get_db
from astro_calc import julian_date, lst_hours, ra_dec_to_alt_az

app = Flask(__name__, static_folder="../frontend", static_url_path="/")

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/stars")
def stars():
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))
    time_utc = datetime.fromisoformat(request.args.get("time").replace("Z","")).replace(tzinfo=timezone.utc)

    jd = julian_date(time_utc)
    lst_h = lst_hours(jd, lon)

    db = get_db()
    cur = db.execute("SELECT name, ra_hours, dec_deg, mag FROM stars")
    stars = []
    for row in cur.fetchall():
        alt, az = ra_dec_to_alt_az(row["ra_hours"], row["dec_deg"], lat, lst_h)
        if alt > 0:  # above horizon
            stars.append({
                "name": row["name"],
                "alt": alt,
                "az": az,
                "mag": row["mag"]
            })
    return jsonify(stars)

if __name__ == "__main__":
    app.run(debug=True)
