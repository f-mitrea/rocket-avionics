"""Plot a recorded flight replayed through the detection logic.

Usage: python tools/plot_replay.py /abs/path/flight.csv [figures/replay.png]
"""
import csv
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from avionics.atmosphere import pressure_to_altitude
from avionics.filters import filter_pressure, reset_filter
from avionics.flight_state import apogee_detected, liftoff_detected

csv_path = sys.argv[1]
out_path = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "figures" / "replay.png"

rows = []
with open(csv_path) as f:
    for row in csv.reader(f):
        if len(row) >= 2:
            rows.append((float(row[0]) / 1000, float(row[1])))

ground = pressure_to_altitude(rows[0][1])
t = [r[0] for r in rows]
raw = [pressure_to_altitude(p) - ground for _, p in rows]

reset_filter()
alts = []
filt = []
liftoff_i = fired_i = None
for i, (_, p) in enumerate(rows):
    alts.append(pressure_to_altitude(filter_pressure(p)))
    filt.append(alts[-1] - ground)
    if liftoff_i is None:
        if liftoff_detected(alts):
            liftoff_i = i
    elif fired_i is None and apogee_detected(alts):
        fired_i = i

apogee_i = max(range(len(raw)), key=lambda i: raw[i])
end = min(len(rows), apogee_i + int(10 / ((t[-1] - t[0]) / len(t))))

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
ax.plot(t[:end], raw[:end], color="#9aa0a6", linewidth=1, label="raw pressure -> altitude")
ax.plot(t[:end], filt[:end], color="#1f6feb", linewidth=2, label="filtered (median 25 + average 3)")

marks = [(apogee_i, raw, "highest raw sample", "#202124", (12, -34)),
         (fired_i, raw, "apogee detected (drogue)", "#d93025", (-135, -40)),
         (liftoff_i, raw, "liftoff detected", "#d93025", (12, -24))]
for i, series, name, color, offset in marks:
    if i is None:
        continue
    ax.plot(t[i], series[i], "o", markersize=8, color=color,
            markeredgecolor="white", markeredgewidth=2, zorder=3)
    ax.annotate("%s\n%.2f s, %.0f m" % (name, t[i], series[i]), (t[i], series[i]),
                textcoords="offset points", xytext=offset, fontsize=8, color="#202124")

ax.set_xlabel("time since log start [s]")
ax.set_ylabel("altitude above pad [m]")
ax.grid(color="#e0e0e0", linewidth=0.8)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.legend(frameon=False, loc="upper left", fontsize=8)
ax.set_title("Recorded flight replayed through flight_state.py", fontsize=10, loc="left")
fig.tight_layout()
out_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out_path)
print("saved", out_path)
