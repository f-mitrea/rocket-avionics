from collections import deque

MEDIAN_WINDOW = 25
AVERAGE_WINDOW = 3

pressure_samples = deque(maxlen=MEDIAN_WINDOW)
past_medians = deque(maxlen=AVERAGE_WINDOW)


def filter_pressure(pressure: float, debug_hook=None) -> float:

    global pressure_samples, past_medians

    pressure_samples.append(pressure)
    ordered = sorted(pressure_samples)
    if debug_hook is not None:
        debug_hook(ordered)

    middle = len(ordered) // 2
    if len(ordered) % 2 == 0:
        median = (ordered[middle - 1] + ordered[middle]) / 2
    else:
        median = ordered[middle]

    past_medians.append(median)
    return sum(past_medians) / len(past_medians)


def reset_filter() -> None:

    pressure_samples.clear()
    past_medians.clear()
