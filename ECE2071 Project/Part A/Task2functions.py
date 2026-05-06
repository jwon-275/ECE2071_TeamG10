import numpy as np
import wave
import serial
import matplotlib.pyplot as plt

# Connect to STM32 over UART
print("Connecting to STM32...")
ser = serial.Serial(
    port='/dev/tty.usbmodem21103',
    baudrate=115200,
    timeout=1
)
print(f"Connected on {ser.port}")

# Empty list to store incoming data
data = []

# STM32 timer-triggered ADC at 120us period = ~8333 sps
# UART bottleneck limits effective rate to ~5000 sps
SAMPLE_RATE = 5000
DURATION = 5  # seconds
NUM_SAMPLES = SAMPLE_RATE * DURATION

# Read 1 byte at a time from UART for 5 seconds
print(f"Recording for {DURATION} seconds ({NUM_SAMPLES} samples)...")
for i in range(NUM_SAMPLES):
    byte = ser.read(1)
    if byte:
        data.append(ord(byte))
    else:
        print(f"  Timeout at sample {i} — no data received")
        break
    if i % SAMPLE_RATE == 0 and i > 0:
        print(f"  {i // SAMPLE_RATE}s elapsed...")

ser.close()
print(f"Done recording. Got {len(data)} samples.")

if len(data) == 0:
    print("No data received. Check STM32 is transmitting.")
    exit()

# Convert to numpy array and normalise to uint8 range (0–255)
print("Normalising data...")
data = np.array(data, dtype=np.float32)
denom = data.max() - data.min()
dataNormalised = (((data - data.min()) / denom * 255) if denom > 0 else data).astype(np.uint8)


# Save raw data as a csv file. 6/5/2026 Nisal
np.savetxt("RawAudioData.csv",dataNormalised,delimiter=",")

# Save audio data as a amplitude graph. 6/5/2026 Nisal
timeAxis = np.arange(len(dataNormalised))//SAMPLE_RATE

# Create pyplot graph using audio Data and save it as a png file. 6/5/2026 Nisal
plt.figure()
plt.plot(timeAxis,dataNormalised)
plt.title("Captured Audio")
plt.xlabel("Time(s)")
plt.ylabel("Amplitude(s)")
plt.savefig("AmplitudePlot.png",dpi = 300,bbox_inches = 'tight')


# Write to WAV file
print("Writing WAV file...")
with wave.open('output.wav', 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(1)        # 8-bit samples (matches STM32 ADC resolution)
    wav_file.setframerate(SAMPLE_RATE)
    wav_file.writeframes(dataNormalised.tobytes())

print(f"Saved {len(dataNormalised)} samples to output.wav")