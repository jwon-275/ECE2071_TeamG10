import serial
import time
import matplotlib.pyplot as plt

# Change this to your port
# Windows: 'COM3', 'COM4', etc
# Mac: '/dev/tty.usbmodem...'
# Linux: '/dev/ttyACM0'
# On mac also run ls /dev/tty.usb* to check
PORT = '/dev/tty.usbmodem21103'
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # wait for STM32 to reset

samples = []
duration = 3  # seconds to collect

print("Collecting samples...")
start = time.time()

while time.time() - start < duration:
    line = ser.readline().decode(errors='ignore').strip()
    if line.isdigit():
        samples.append(int(line))

ser.close()

print(f"Got {len(samples)} samples in {duration}s")
print(f"Approx sample rate: {len(samples) / duration:.0f} sps")

if samples:
    print(f"Min: {min(samples)}")
    print(f"Max: {max(samples)}")
    print(f"Mean: {sum(samples) / len(samples):.1f}")

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    # First 500 samples
    ax1.plot(samples[:500])
    ax1.set_title("First 500 samples")
    ax1.set_xlabel("Sample")
    ax1.set_ylabel("ADC value")
    ax1.axhline(y=512, color='r', linestyle='--', alpha=0.5, label='midpoint (512)')
    ax1.legend()

    # All samples
    ax2.plot(samples)
    ax2.set_title(f"All {len(samples)} samples")
    ax2.set_xlabel("Sample")
    ax2.set_ylabel("ADC value")
    ax2.axhline(y=512, color='r', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()
else:
    print("No samples received. Check COM port and wiring.")