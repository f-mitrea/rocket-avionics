SEA_LEVEL_PRESSURE = 101325.0  # p0 [Pa]
TEMPERATURE_LAPSE_RATE = 0.0065  # L [K/m]
GRAVITY = 9.80665  # g [m/s^2]
AIR_GAS_CONSTANT = 287.05  # R [J/(kg K)]
SEA_LEVEL_TEMPERATURE = 288.15  # T0 [K]


def pressure_to_altitude(pressure: float) -> float:
    exponent = AIR_GAS_CONSTANT * TEMPERATURE_LAPSE_RATE / GRAVITY
    return (SEA_LEVEL_TEMPERATURE / TEMPERATURE_LAPSE_RATE) * (
        1.0 - (pressure / SEA_LEVEL_PRESSURE) ** exponent
    )
