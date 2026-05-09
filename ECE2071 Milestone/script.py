import serial
import time


stm_port = 'COM4' 
rate = 115200 

def main():
    port = serial.Serial(stm_port, rate, timeout=5) 
    time.sleep(2) # https://edstem.org/au/courses/32321/discussion/3241320 
 

    while True:
        
        
        message = input("Message: ")
        edit_message = message + '\n'

        
        port.write(edit_message.encode('utf-8')) 

        
        bytes = port.readline()
        
 
        text = bytes.decode('utf-8').strip()
        print(f"Result: {text}\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting script.")