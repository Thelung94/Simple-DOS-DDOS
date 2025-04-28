import eel
import signal
import sys
import time
from backend import main

def shutdown(signal_received, frame):
    print("\n[+] Ctrl+C detected! Shutting down the app...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

eel.init('frontend')
main.start_backend()

# Non-blocking start
eel.start('index.html', size=(1200, 1000), port=3033, block=False)

print("[*] App started at http://localhost:3033")
while True:
    eel.sleep(1.0)
