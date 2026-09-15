# rocket-avionics

Parachute recovery avionics for **HORNET X**, a sounding rocket built by the
Sapienza Rocket Team.

The flight computer reads pressure from a BMP388 barometer, filters it,
converts it to altitude, and fires the two parachute pyro channels at apogee.

Written during my first year with the team (Training Academy 2024/2025) and
rebuilt here with a proper project layout and tests.

> HORNET X flew, but not with this code on board: on launch day the team used
> their own flight computer. This software was validated in simulation only.

## How it works

Two-state machine:

| State | Condition to leave it | Action |
|-------|----------------------|--------|
| `PRE_LAUNCH` | altitude change > 3 m per sample | go to `IN_FLIGHT` |
| `IN_FLIGHT` | altitude change < 0.1 m per sample | fire drogue, wait 1 s, fire main |

Each reading is median-filtered over 25 samples, then averaged over the last
3 medians, then converted to altitude with the International Standard
Atmosphere formula. Every sample is written to a CSV log.

Design target for HORNET X: apogee 543 m, max velocity 113 m/s.

## Project layout

```
avionics/
  atmosphere.py     pressure -> altitude (ISA)
  filters.py        median + moving average
  flight_state.py   liftoff / apogee detection
  recorder.py       CSV flight log
  main.py           the flight loop
flight.py           entry point
tests/              pytest suite
```

## Install

```bash
pip install -r requirements.txt
```

## Run the tests

```bash
python -m pytest
```

Self-contained: no hardware or simulator needed.

## Run a simulated flight

Needs the Rocket Team files, which are not in this repo:

- **FEMU**, the team's flight simulator, in a folder next to this one
- **`stubs.py`** and **`testDriver.py`** in `vendor/`
- a flight CSV (`time_ms,pressure_Pa`), kept with FEMU rather than in this repo
  (`femu/data/`)

`stubs.py` provides the MicroPython APIs (`time.sleep_ms`, `machine`) that this
code needs and CPython does not have. `testDriver.py` talks to the simulator;
on the real board it is replaced by `driver.py`, same interface.

From the folder containing `femu`:

```bash
PYTHONUNBUFFERED=1 python -m femu /abs/path/femu/data/flight.csv /abs/path/flight.py
```

Both are required:

- `PYTHONUNBUFFERED=1` — without it Python buffers stdout and the two processes
  deadlock silently
- absolute paths — the simulator changes working directory before starting the
  script

## Flight log

`logs/flight_log.csv`, no header, one row per sample:

```
timestamp, filtered_pressure_Pa, raw_pressure_Pa, state, parachute
```

`state` is `3` pre-launch or `2` in flight. `parachute` is `0` stowed or
`1` deployed. Opened in append mode, so delete it between runs.

## Known limitations

- Thresholds are per sample, not per second: they shift if the loop rate changes
- The filter lags, and apogee is detected about 2 s early on the reference flight
- Altitude is above sea level, not above ground

## Author

Fabio Alexandru Mitrea
