import lgpio
import time

# GPIO pin definitions (BCM numbering)
TRIG_A_PIN = 23
ECHO_A_PIN = 24
TRIG_B_PIN = 17
ECHO_B_PIN = 27
RELAY_PIN  = 18

# Open the GPIO chip
chip = lgpio.gpiochip_open(0)

# Configure pins
lgpio.gpio_claim_output(chip, TRIG_A_PIN)
lgpio.gpio_claim_input(chip, ECHO_A_PIN)
lgpio.gpio_claim_output(chip, TRIG_B_PIN)
lgpio.gpio_claim_input(chip, ECHO_B_PIN)
lgpio.gpio_claim_output(chip, RELAY_PIN)

# Person counter
person_count = 0

# Variables to track trigger events
time_A = None
time_B = None
TIME_WINDOW = 1.0  # max seconds between A and B to consider one event

def trigger_pulse(pin):
    """Send 10µs pulse on TRIG pin."""
    lgpio.gpio_write(chip, pin, 1)
    time.sleep(0.00001)
    lgpio.gpio_write(chip, pin, 0)

def get_distance(trig, echo, timeout_s=0.02):
    """Measure distance; return cm or large number on timeout."""
    trigger_pulse(trig)
    start = time.time()
    # wait for echo high
    while lgpio.gpio_read(chip, echo) == 0:
        if time.time() - start > timeout_s:
            return float('inf')
    t0 = time.time()
    # wait for echo low
    while lgpio.gpio_read(chip, echo) == 1:
        if time.time() - t0 > timeout_s:
            return float('inf')
    t1 = time.time()
    return round((t1 - t0) * 17150, 2)

def update_relay():
    """Turn relay on if count>0, else off."""
    if person_count > 0:
        lgpio.gpio_write(chip, RELAY_PIN, 1)
    else:
        lgpio.gpio_write(chip, RELAY_PIN, 0)

try:
    while True:
        now = time.time()
        dA = get_distance(TRIG_A_PIN, ECHO_A_PIN)
        dB = get_distance(TRIG_B_PIN, ECHO_B_PIN)
        # Check for A detection
        if dA < 50:
            if time_A is None:
                time_A = now
        # Check for B detection
        if dB < 50:
            if time_B is None:
                time_B = now

        # If both detected within TIME_WINDOW, decide order
        if time_A and time_B and abs(time_A - time_B) <= TIME_WINDOW:
            if time_A < time_B:
                person_count += 1
                print("A→B: increment →", person_count)
            else:
                if person_count > 0:
                    person_count -= 1
                print("B→A: decrement →", person_count)
            # Reset for next cycle
            time_A = None
            time_B = None
            update_relay()

        # If one stuck alone for too long, reset to avoid stale triggers
        if time_A and now - time_A > TIME_WINDOW:
            time_A = None
        if time_B and now - time_B > TIME_WINDOW:
            time_B = None

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    # turn off relay and cleanup
    lgpio.gpio_write(chip, RELAY_PIN, 0)
    lgpio.gpiochip_close(chip)
