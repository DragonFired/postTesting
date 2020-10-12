# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import uos, machine
# uos.dupterm(None, 1) # disable REPL on UART(0)
import webrepl

webrepl.start()
import gc

gc.collect()
print("Free RAM: {0}".format(gc.mem_free()))

from uos import stat

try:
    if stat("/plantMonitor.py")[6] > 0:
        exec(open("/plantMonitor.py").read())
except OSError:
    print("plantMonitor.py code file not found")
