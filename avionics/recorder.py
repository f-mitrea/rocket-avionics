LOG_PATH = "logs/flight_log.csv"

log_file = None


def open_log(path: str = LOG_PATH) -> None:

    global log_file
    log_file = open(path, "a")


def write_row(
    timestamp: float,
    filtered_pressure: float,
    raw_pressure: float,
    state: int,
    parachute: int,
) -> None:

    log_file.write(
        f"\n{timestamp},{filtered_pressure},{raw_pressure},{state},{parachute}"
    )


def close_log() -> None:

    global log_file
    log_file.close()
    log_file = None
