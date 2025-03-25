import time
import threading
import logging
import random

class PeripheralDetector:
    def __init__(self, callback=None):
        self.callback = callback  # Callback function when an event is detected
        self.event_log = []       # List to store peripheral events
        self.running = False
        self.risk_score = 0       # Cumulative risk score for peripheral detection
        self.last_monitor_count = 1  # Assume 1 monitor initially
        self.logger = logging.getLogger("PeripheralDetector")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s: %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def simulate_pnp(self):
        # Simulate a peripheral event randomly every 10 seconds.
        while self.running:
            # 20% chance to simulate a peripheral event
            if random.random() < 0.2:
                risk_inc = 35
                self.risk_score += risk_inc
                log_entry = {
                    "timestamp": time.time(),
                    "device": f"Simulated Peripheral {random.randint(1, 100)}",
                    "risk": risk_inc
                }
                self.event_log.append(log_entry)
                self.logger.info("Simulated peripheral detected: %s; risk increased by %d", log_entry["device"], risk_inc)
                if self.callback:
                    self.callback(log_entry)
            time.sleep(10)

    def simulate_monitors(self):
        # Simulate a change in monitor count every 15 seconds.
        while self.running:
            # Randomly choose a monitor count between 1 and 3
            new_count = random.randint(1, 3)
            if new_count != self.last_monitor_count:
                if new_count > 1:
                    risk_inc = 35
                    self.risk_score += risk_inc
                    log_entry = {
                        "timestamp": time.time(),
                        "device": f"Multiple monitors detected: {new_count}",
                        "risk": risk_inc
                    }
                    self.event_log.append(log_entry)
                    self.logger.info("Simulated monitor change: %d monitors detected; risk increased by %d", new_count, risk_inc)
                    if self.callback:
                        self.callback(log_entry)
                self.last_monitor_count = new_count
            time.sleep(15)

    def start(self):
        self.running = True
        self.thread_pnp = threading.Thread(target=self.simulate_pnp, daemon=True)
        self.thread_monitors = threading.Thread(target=self.simulate_monitors, daemon=True)
        self.thread_pnp.start()
        self.thread_monitors.start()
        self.logger.info("PeripheralDetector (simulated) started.")

    def stop(self):
        self.running = False
        self.thread_pnp.join()
        self.thread_monitors.join()
        self.logger.info("PeripheralDetector (simulated) stopped.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    detector = PeripheralDetector(callback=lambda event: print("Detected:", event))
    detector.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        detector.stop()
