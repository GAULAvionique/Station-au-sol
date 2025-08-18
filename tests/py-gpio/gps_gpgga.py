def parse_gpgga(nmea_sentence):
    parts = nmea_sentence.strip().split(',')
    if len(parts) < 15:
        return None  # Incomplete frame

    try:
        time_str = parts[1]
        lat_str = parts[2]
        lat_dir = parts[3]
        lon_str = parts[4]
        lon_dir = parts[5]
        fix_quality = parts[6]
        num_satellites = parts[7]

        # Latitude conversion
        lat_deg = float(lat_str[:2])
        lat_min = float(lat_str[2:])
        latitude = lat_deg + lat_min / 60
        if lat_dir == 'S':
            latitude *= -1

        # Longitude conversion
        lon_deg = float(lon_str[:3])
        lon_min = float(lon_str[3:])
        longitude = lon_deg + lon_min / 60
        if lon_dir == 'W':
            longitude *= -1

        return {
            "time": time_str,
            "latitude": latitude,
            "longitude": longitude,
            "fix_quality": fix_quality,
            "satellites": num_satellites
        }
    except (ValueError, IndexError):
        return None


def test_gps(device="/dev/serial0"):
    try:
        with open(device, 'r') as serial:
            print(f"Reading GPS on {device}...")
            while True:
                line = serial.readline()
                if line.startswith('$GPGGA'):
                    data = parse_gpgga(line)
                    if data:
                        print("=== GPS Data ===")
                        print(f"Time (UTC)    : {data['time']}")
                        print(f"Latitude      : {data['latitude']}")
                        print(f"Longitude     : {data['longitude']}")
                        print(f"Fix Quality   : {data['fix_quality']}")
                        print(f"Satellites    : {data['satellites']}")
                        print("====================")
    except FileNotFoundError:
        print(f"The device {device} was not found.")
    except PermissionError:
        print(f"Permission denied to read {device}. Use sudo?")
    except KeyboardInterrupt:
        print("Manual stop.")


if __name__ == "__main__":
    test_gps()
