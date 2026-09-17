from avionics.atmosphere import SEA_LEVEL_PRESSURE, pressure_to_altitude


def test_sea_level_gives_zero_altitude():
    assert abs(pressure_to_altitude(SEA_LEVEL_PRESSURE)) < 1e-9


def test_altitude_increase_as_pressure_drops():
    assert pressure_to_altitude(90000.0) > pressure_to_altitude(100000.0)


def test_launch_site_altitude_matches_flight_data():
    assert round(pressure_to_altitude(86181.7), 1) == 1344.5
