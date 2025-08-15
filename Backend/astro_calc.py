import math
from datetime import datetime, timezone

def julian_date(dt):
    """Convert datetime to Julian Date."""
    year = dt.year
    month = dt.month
    day = dt.day + (dt.hour + dt.minute/60 + dt.second/3600) / 24
    if month <= 2:
        year -= 1
        month += 12
    A = year // 100
    B = 2 - A + (A // 4)
    JD = int(365.25*(year + 4716)) + int(30.6001*(month + 1)) + day + B - 1524.5
    return JD

def lst_hours(jd, lon_deg):
    """Local Sidereal Time in hours."""
    T = (jd - 2451545.0) / 36525
    GST = 6.697374558 + 2400.051336*T + 0.000025862*T*T
    GST = GST % 24
    LST = GST + lon_deg / 15
    return LST % 24

def ra_dec_to_alt_az(ra_hours, dec_deg, lat_deg, lst_h):
    """Convert RA/Dec to Alt/Az."""
    H = (lst_h - ra_hours) * 15
    lat = math.radians(lat_deg)
    dec = math.radians(dec_deg)
    H = math.radians(H)
    sin_alt = math.sin(dec)*math.sin(lat) + math.cos(dec)*math.cos(lat)*math.cos(H)
    alt = math.asin(sin_alt)
    cos_az = (math.sin(dec) - math.sin(alt)*math.sin(lat)) / (math.cos(alt)*math.cos(lat))
    cos_az = max(-1, min(1, cos_az))
    az = math.acos(cos_az)
    if math.sin(H) > 0:
        az = 2*math.pi - az
    return math.degrees(alt), math.degrees(az)
