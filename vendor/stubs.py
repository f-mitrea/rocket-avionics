__all__ = ( )

try:
    import machine
except ImportError:
    import time
    import sys
    import threading
    import typing
    import ctypes
    from enum import Enum

    __startTime = time.time_ns() // 1000

    # `time` module impl
    time.ticks_ms = lambda: time.time_ns() // 1000000 - __startTime
    time.sleep_ms = lambda ms: time.sleep( ms / 1000 )

    # `machine` module impl
    sys.modules[ "machine" ] = sys.modules[ __name__ ]
        



    class Timer:
        PERIODIC: typing.Final[ bool ] = False
        ONE_SHOT: typing.Final[ bool ] = True

        _periodSec: float
        _oneShot: bool
        _callback: typing.Callable
        _control: threading.Thread
        _timeOut: float


        def __init__( self, mode: bool, period: int, callback: typing.Callable = None ):
            self._periodSec = period / 1000
            self._oneShot = mode
            self._callback = callback
            self._timeOut = time.time() + self._periodSec
            self._control = threading.Thread(target=self._controlThread)
            self._control.start()

        def _controlThread(self):
            while True:
                if time.time() > self._timeOut:
                    self._timeOut += self._periodSec
                    self._callback()
                    if self._oneShot: return