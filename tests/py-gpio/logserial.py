import serial


def read_and_write_serial_ascii(device="/dev/serial0", baudrate=9600):
    try:
        with serial.Serial(device, baudrate, timeout=1) as ser:
            print(f"Connection opened on {device} (read/write)... (Ctrl+C to stop)")
            while True:
                if ser.in_waiting:
                    line = ser.readline().decode('ascii', errors='replace').strip()
                    print(line)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nManual stop.")


if __name__ == "__main__":
    read_and_write_serial_ascii()
