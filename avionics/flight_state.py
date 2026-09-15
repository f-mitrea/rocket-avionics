
LIFTOFF_THRESHOLD_M = 3
APOGEE_THRESHOLD_M = 0.1

PRE_LAUNCH = 3
IN_FLIGHT = 2

PARACHUTE_STOWED = 0
PARACHUTE_DEPLOYED = 1


def liftoff_detected(altitudes: list[float]) -> bool:

    if len(altitudes) < 2:
        return False
    altitude_change = altitudes[-1] - altitudes[-2]
    return abs(altitude_change) > LIFTOFF_THRESHOLD_M


def apogee_detected(altitudes: list[float]) -> bool:

    if len(altitudes) < 2:
        return False
    altitude_changes = altitudes[-1] - altitudes[-2]
    return abs(altitude_changes) < APOGEE_THRESHOLD_M