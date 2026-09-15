# rocket-avionics

Parachute recovery code for HORNET X, a solid-propellant sounding rocket built
by the Sapienza Rocket Team.

The flight computer reads pressure off a BMP388, filters it, turns it into
altitude and fires the two pyro channels once it decides the rocket has stopped
going up.

I wrote the first version during my first year with the team, in the Sapienza
Rocket Team Training Academy 2024/2025, as part of team 7. What's in here is
that same logic, tidied up and with tests around it. HORNET X did fly, but not
with this on board: on launch day we used the team's own flight computer, so
everything below was only ever checked in simulation.

## The rocket

A 75 mm airframe about 66 cm long: a 3D-printed PLA ogive nose over a Kraft
phenolic body tube, trapezoidal fins, ballast up front to move the centre of
gravity forward. Recovery was sized for a 1 kg vehicle coming down at 3 m/s
under a cruciform chute of 0.73 m side, which is where the ejection charge and
shock cord loads came from.

Worth saying, because it sets the scale the thresholds below were chosen for:
the flight I replay in `tools/replay.py` is a different and much larger team
vehicle, reaching 1418 m about 18 s after leaving the pad, against the few
hundred metres and roughly 10 s HORNET X was built for. The detection logic is
the same either way, but the numbers it has to work with are not.

## What it does

Two states. On the pad it keeps sampling until the altitude moves more than 3 m
between two consecutive samples, and calls that liftoff. From then on it looks
for two samples less than 10 cm apart, calls that apogee, fires the drogue,
waits a second and fires the main.

Each reading goes through a median filter over the last 25 samples, then a
3-point moving average, and only then becomes an altitude with the standard ISA
formula. Everything gets written to a CSV while the loop runs.

The team's OpenRocket model puts apogee in the mid-500s, but its motor and its
mass don't agree with the 1 kg the recovery was sized around, so I read that as
a design target rather than a prediction.

## Layout

```
avionics/
  atmosphere.py     pressure -> altitude (ISA)
  filters.py        median + moving average
  flight_state.py   liftoff / apogee detection
  recorder.py       CSV flight log
  main.py           the flight loop
flight.py           entry point
tests/              pytest suite
tools/replay.py     replay a recorded flight through the detection logic
vendor/             team-supplied stubs and simulator driver
```

## Tests

```bash
pip install -r requirements.txt
python -m pytest
```

Eleven of them, covering the atmosphere math, the filter and the state machine.
No hardware or simulator involved. The flight code itself needs nothing outside
the standard library; pytest is the only dependency and it's there just to run
the tests.

## Running a simulated flight

`vendor/stubs.py` and `vendor/testDriver.py` are in the repo. `stubs.py` fakes
the MicroPython pieces that CPython doesn't have (`time.sleep_ms`, `machine`).
`testDriver.py` talks to the simulator over stdin/stdout; on the real board it
gets swapped for `driver.py`, same interface. Neither of them is mine, they come
from the team.

What you need from outside is FEMU, the team's simulator, in a folder next to
this one, and a recorded flight to replay: a CSV of `time_ms,pressure_Pa` rows,
which I keep in `femu/data/` rather than in here. The team's flight logs are not
part of this repo.

From the folder that contains `femu`:

```bash
PYTHONUNBUFFERED=1 python -m femu /abs/path/femu/data/flight.csv /abs/path/flight.py
```

Both bits matter. Without `PYTHONUNBUFFERED=1` the two processes end up waiting
on each other's buffered output and nothing happens, with no error to tell you
why. The paths have to be absolute because femu changes working directory before
it starts the script.

## The log

`logs/flight_log.csv`, no header, one row per sample:

```
timestamp, filtered_pressure_Pa, raw_pressure_Pa, state, parachute
```

`state` is 3 on the pad and 2 in flight, `parachute` is 0 or 1. The file opens
in append mode, so delete it between runs or you'll get two flights in one.

## What's still wrong with it

`tools/replay.py` feeds a recorded flight through the same filter and state
machine the flight loop uses, and prints where the thresholds actually fire
against the apogee computed from the unfiltered pressure:

```bash
python tools/replay.py /abs/path/femu/data/flight.csv
```

On the flight I replayed, apogee comes out 3.1 s early and 15 m low, with the
rocket still climbing at 13 m/s, and liftoff isn't flagged until 142 m, about a
second after it actually left the pad. Both have the same cause: the two checks
look at a single pair of samples and compare absolute differences, so they can't
tell a climb from a descent, and one quiet pair is enough to trigger a
deployment.

The thresholds are per sample rather than per second, so they only mean what I
think they mean at the loop rate I picked (20 ms). The flight I replayed was
recorded at 12.5 ms.

Altitude is above sea level. Nothing zeroes it on the pad.

The loop exits right after the main charge, so none of the descent is logged and
there's no landing detection.

`time.monotonic()` works only because of the CPython stubs. On the board it
would need `time.ticks_ms()`.

## Author

Fabio Alexandru Mitrea
