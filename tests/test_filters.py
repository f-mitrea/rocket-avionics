from avionics.filters import filter_pressure, reset_filter

def test_first_sample_returns_itself():
    reset_filter()
    assert filter_pressure(101325.0) == 101325.0


def test_second_sample_is_averaged():
    reset_filter()
    filter_pressure(100.0)
    assert filter_pressure(200.0) == 125.0


def test_spike_is_rejected():
    reset_filter()
    for _ in range(25):
        filter_pressure(100000.0)
    assert filter_pressure(500000.0) == 100000.0