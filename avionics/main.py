import time

import stubs  # noqa: F401  - installs MicroPython APIs on CPython
import testDriver

from avionics.atmosphere import pressure_to_altitude
from avionics.filters import filter_pressure
from avionics.flight_state import (
    IN_FLIGHT,
    PARACHUTE_DEPLOYED,
    PARACHUTE_STOWED,
    PRE_LAUNCH,
    apogee_detected,
    liftoff_detected,
)
from avionics.recorder import close_log, open_log, write_row

SAMPLE_PERIOD_MS = 20
PYRO_DELAY_MS = 1000
DROGUE_CHANNEL = 0
MAIN_CHANNEL = 1


def main() -> None:

    altitudes: list[float] = []
    parachute_deployed = False
    barometer = testDriver.Baro()
    state = PRE_LAUNCH
    parachute = PARACHUTE_STOWED

    open_log()

    while state == PRE_LAUNCH:
        raw = barometer.getPressure()
        filtered = filter_pressure(raw)
        altitudes.append(pressure_to_altitude(filtered))
        write_row(time.monotonic(), filtered, raw, state, parachute)
        if liftoff_detected(altitudes):
            state = IN_FLIGHT
        time.sleep_ms(SAMPLE_PERIOD_MS)

    while not parachute_deployed:
        raw = barometer.getPressure()
        filtered = filter_pressure(raw)
        altitudes.append(pressure_to_altitude(filtered))
        write_row(time.monotonic(), filtered, raw, state, parachute)

        if apogee_detected(altitudes):
            parachute_deployed = True
            parachute = PARACHUTE_DEPLOYED
            write_row(time.monotonic(), filtered, raw, state, parachute)
            testDriver.openParachute(DROGUE_CHANNEL)
            time.sleep_ms(PYRO_DELAY_MS)
            testDriver.openParachute(MAIN_CHANNEL)

        time.sleep_ms(SAMPLE_PERIOD_MS)

    close_log()


