import serial
import numpy as np
import wave
import matplotlib.pyplot as plt
import csv
import time


TEAM_ID = "G10" 
PORT = "COM4"
BAUD_RATE = 460800
SAMPLE_RATE = 22050

def save_all_formats(data, team_id, rate):
    # convert to numpy 
    data = np.array(data, dtype=float)
    if len(data) == 0:
        print("No data")
        return

    if data.max() != data.min(): # small edge case div0
        data = (data - data.min()) / (data.max() - data.min())
        data = (data * 255).astype(np.uint8)
    else:
        data = data.astype(np.uint8)
        
    times = int(time.time())
    filename = f"{team_id}_{rate}Hz_{times}" # for easy testing (format)
    
    # save wav file
    with wave.open(f"{filename}.wav", 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(1)
        wf.setframerate(rate)
        wf.writeframes(data.tobytes())
    
    # save .csv 
    with open(f"{filename}.csv", 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow([rate]) # first row sample rate 
        for val in data:
            write.writerow([val])
            
    # save .png
    plt.figure(figsize=(10, 4))
    plt.plot(data)
    plt.title(f"Audio Amplitude vs Time - {team_id}")
    plt.xlabel("Index") 
    plt.ylabel("Amplitude") 
    plt.grid(True)
    plt.savefig(f"{filename}.png")
    plt.close()
    
    print(f"saved as: {filename}.wav, .csv, and .png")

def record(ser, num_samples=None):
    print("Recording")
    data = []
    
    if num_samples:
        # manual 
        for _ in range(num_samples):
            byte = ser.read(1)
            if byte:
                data.append(byte[0])
    else:
        # distance 
        while True:
            byte = ser.read(1)
            if not byte: # timeout
                break
            data.append(byte[0])
            
    return np.array(data, dtype=np.uint8)



# maybe not needed
ser = serial.Serial(PORT, BAUD_RATE, timeout=1.0) 

try:
    while True:
        print("\n=== ECE2071 PROJECT (G10) ===")
        print("1. Manual Mode")
        print("2. Distance Mode")
        print("3. Stop")
        choice = input("Select: ")

        if choice == '1':
            duration = float(input("recording length (secs): "))
            num_samples = int(duration * SAMPLE_RATE)
            
            ser.write(b'M') #  set STM to enter manual
            time.sleep(0.1) # small delay
            ser.reset_input_buffer() # clear (idk if helps)
            
            audio_data = record(ser, num_samples=num_samples)
            save_all_formats(audio_data, TEAM_ID, SAMPLE_RATE)
            
            ser.write(b'I') # unused now no need 

        elif choice == '2':
            print("Distance Mode active")
            ser.write(b'D') # set stm to distance
            time.sleep(0.1) # small delay
            ser.reset_input_buffer() # clear
            
            audio_data = record(ser, num_samples=None)
            
            if len(audio_data) > 0:
                save_all_formats(audio_data, TEAM_ID, SAMPLE_RATE)
            else:
                print("No data")
                
            ser.write(b'I') # not needed,
        elif choice == '3':
            break
finally:
    ser.close()



# Task 1

# import numpy as np
# import wave
# import serial

# PORT = "COM4"  # Make sure this matches your Processing STM32
# BAUD_RATE = 115200
# SAMPLE_RATE = 8296 
# RECORD_SECONDS = 5 

# TOTAL_SAMPLES = SAMPLE_RATE * RECORD_SECONDS

# ser = serial.Serial(PORT, BAUD_RATE)
# data = []

# print("Recording audio...")

# # Loop exactly 25,000 times
# for i in range(TOTAL_SAMPLES):
#     byte_read = ser.read(1)
#     data.append(byte_read[0])
#     if i % 1000 == 0:
#         print(f"Received {i} bytes...")

# print("Recording complete.")
# ser.close()

# print(f"First 50 samples: {data[:50]}")

# # Convert to numpy array and normalize to 0-255 [cite: 394, 396, 399, 401]
# data = np.array(data)

# data = (data - data.min()) / data.max() # scale to 0-1
# data = data * 255                       # scale to 0-255
# data = data.astype(np.uint8)            # convert to uint8 type

# filename = "output_task1.wav"

# # Write to the .wav file [cite: 411, 412, 413, 414, 419]
# with wave.open(filename, 'wb') as wf:
#     wf.setnchannels(1)           # mono audio (single channel)
#     wf.setsampwidth(1)           # 8 bits (1 byte) per sample
#     wf.setframerate(SAMPLE_RATE) # set the sample rate
#     wf.writeframes(data.tobytes())

# print(f"File saved as {filename}")

# # import numpy as np
# # import wave
# # import serial

# # PORT = "COM4"  # Make sure this matches your Processing STM32
# # BAUD_RATE = 115200
# # SAMPLE_RATE = 5000 
# # RECORD_SECONDS = 5 

# # TOTAL_SAMPLES = SAMPLE_RATE * RECORD_SECONDS

# # ser = serial.Serial(PORT, BAUD_RATE)
# # data = []

# # print("Recording audio...")

# # # Loop exactly 25,000 times
# # for _ in range(TOTAL_SAMPLES):
# #     byte_read = ser.read(1)
# #     data.append(byte_read[0])

# # print("Recording complete.")
# # ser.close()

# # # Convert to numpy array and normalize to 0-255 [cite: 394, 396, 399, 401]
# # data = np.array(data)

# # data = (data - data.min()) / data.max() # scale to 0-1
# # data = data * 255                       # scale to 0-255
# # data = data.astype(np.uint8)            # convert to uint8 type

# # filename = "output_task1.wav"

# # # Write to the .wav file [cite: 411, 412, 413, 414, 419]
# # with wave.open(filename, 'wb') as wf:
# #     wf.setnchannels(1)           # mono audio (single channel)
# #     wf.setsampwidth(1)           # 8 bits (1 byte) per sample
# #     wf.setframerate(SAMPLE_RATE) # set the sample rate
# #     wf.writeframes(data.tobytes())

# # print(f"File saved as {filename}")