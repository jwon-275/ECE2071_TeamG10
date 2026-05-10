import numpy as np
import wave
import serial

PORT = "COM4"  
BAUD_RATE = 115200
SAMPLE_RATE = 5000 
RECORD_SECONDS = 5 

TOTAL_SAMPLES = SAMPLE_RATE * RECORD_SECONDS

ser = serial.Serial(PORT, BAUD_RATE)
data = []

print("Recording ")

# loop 250000 times
for _ in range(TOTAL_SAMPLES):
    byte_read = ser.read(1)
    data.append(byte_read[0])

print("Recording complete.")
ser.close()


data = np.array(data)

data = (data - data.min()) / data.max() # scale to 0-1
data = data * 255                       # scale to 0-255
data = data.astype(np.uint8)            

filename = "output_task1.wav"


with wave.open(filename, 'wb') as wf:
    wf.setnchannels(1)           # mono audio (single channel)
    wf.setsampwidth(1)           # 8 bits (1 byte) per sample
    wf.setframerate(SAMPLE_RATE) # set the sample rate
    wf.writeframes(data.tobytes())

print(f"File saved as {filename}")
