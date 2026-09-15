import io
import sys
from pathlib import Path
try:
    from machine import Pin
    Pin("LED", Pin.OUT).on()
except ImportError:
    pass

dir = Path("./mSD")

if not dir.exists():
    dir.mkdir()

dirPath = str(dir)
"""
absolute path to free-to-use directory as str
"""

def openParachute(channel: bool) -> None:
    """
    fire phyro
    :param channel: 0 or 1, the firing channel
    """
    print(f"P{int(channel)}", end="\0")


class Baro:
    """
    interface to the physical bmp 388
    """
    def __init__(self):
        print("S", end="\0")

    def getPressure(self) -> float:
        """

        :return: latest pressure esteeme
        """
        print("G", end='\0')
        buffer = io.StringIO()
        while (x := sys.stdin.read(1)) != '\0':
            buffer.write(x)

        data: str = buffer.getvalue()
        return float(data) / 10

def changeState() -> None:
    """
    when testing communicate to the simulator that the state has changed
    """
    print("C", end="\0")


def printToLog(arg) -> None:
    """
    when testing send a stringable message to the simulator
    :param arg: stuff to print
    """
    print(f"D{str(arg)}", end="\0")


def endFlight() -> None:
    """
    when testing halt simulator
    """
    print("E", end="\0")
