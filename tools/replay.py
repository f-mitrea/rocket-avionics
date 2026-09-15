import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from avionics.atmosphere import pressure_to_altitude
from avionics.filters import filter_pressure, reset_filter
from avionics.flight_state import apogee_detected, liftoff_detected

csv_path = sys.argv[1]

rows = []
with open(csv_path) as f:
    for row in csv.reader(f):
        if len(row) >= 2:
            rows.append((float(row[0]), float(row[1])))

print("campioni:", len(rows))
print("durata s:", (rows[-1][0] - rows[0][0]) / 1000)

gaps = [rows[i + 1][0] - rows[i][0] for i in range(len(rows) - 1)]
print("dt medio ms: %.1f" % (sum(gaps) / len(gaps)))

raw_alt = [pressure_to_altitude(p) for t, p in rows]
ground = raw_alt[0]

apogee_i = max(range(len(raw_alt)), key=lambda i: raw_alt[i])

print("quota di lancio AMSL m: %.1f" % ground)
print("apogeo vero: t=%.2f s  AGL=%.1f m"
      % (rows[apogee_i][0] / 1000, raw_alt[apogee_i] - ground))

reset_filter()

alts = []
liftoff_i = None
fired_i = None

for i, (t, p) in enumerate(rows):
    alts.append(pressure_to_altitude(filter_pressure(p)))

    if liftoff_i is None:
        if liftoff_detected(alts):
            liftoff_i = i
    elif fired_i is None:
        if apogee_detected(alts):
            fired_i = i
            break


def report(name, i):
    if i is None:
        print(name + ": mai rilevato")
    else:
        print("%s: t=%.2f s  AGL=%.1f m"
              % (name, rows[i][0] / 1000, raw_alt[i] - ground))


report("liftoff rilevato", liftoff_i)
report("apogeo rilevato ", fired_i)

if fired_i is not None:
    err_s = (rows[fired_i][0] - rows[apogee_i][0]) / 1000
    err_m = raw_alt[fired_i] - raw_alt[apogee_i]

    w = 20
    a = max(0, fired_i - w)
    b = min(len(rows) - 1, fired_i + w)
    climb = (raw_alt[b] - raw_alt[a]) / ((rows[b][0] - rows[a][0]) / 1000)

    print("errore sull'apogeo: %+.2f s, %+.1f m" % (err_s, err_m))
    print("velocita' verticale allo sparo: %+.1f m/s" % climb)