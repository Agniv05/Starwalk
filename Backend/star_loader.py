import sqlite3
import csv

conn = sqlite3.connect("stars.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS stars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    ra_hours REAL,
    dec_deg REAL,
    mag REAL
);
""")

# Example: load minimal dataset (you can replace with Hipparcos subset)
with open("bright_stars.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute("INSERT INTO stars (name, ra_hours, dec_deg, mag) VALUES (?, ?, ?, ?)",
                    (row["name"], float(row["ra_hours"]), float(row["dec_deg"]), float(row["mag"])))

conn.commit()
conn.close()
