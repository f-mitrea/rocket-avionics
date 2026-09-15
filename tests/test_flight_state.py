from avionics.flight_state import apogee_detected, liftoff_detected


def test_no_decision_without_two_samples():
    assert liftoff_detected([]) is False
    assert liftoff_detected([100.0]) is False
    assert apogee_detected([100.0]) is False


def test_liftoff_detected_above_threshold():
    assert liftoff_detected([100.0, 105.0]) is True


def test_no_liftoff_on_sensor_noise():
    assert liftoff_detected([100.0, 101.00]) is False


def test_apogee_detected_when_altitude_flattens():
    assert apogee_detected([100.0, 100.05]) is True


def test_no_apogee_while_still_climbing():
    assert apogee_detected([100.0, 105.0]) is False