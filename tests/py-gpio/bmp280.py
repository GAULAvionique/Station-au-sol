import sys
import time
import smbus2

# I2C address of BMP280 (0x76 or 0x77 depending on wiring)
BMP280_I2C_ADDR = 0x77

# Registers
REG_ID = 0xD0
REG_RESET = 0xE0
REG_CTRL_MEAS = 0xF4
REG_CONFIG = 0xF5
REG_PRESS_MSB = 0xF7

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Read sensor ID for verification
chip_id = bus.read_byte_data(BMP280_I2C_ADDR, REG_ID)
if chip_id != 0x58:
    print("Error: BMP280 sensor not detected.")
    sys.exit()

# Configure sensor: normal mode, oversampling x1 for T and P
bus.write_byte_data(BMP280_I2C_ADDR, REG_CTRL_MEAS, 0x27)
bus.write_byte_data(BMP280_I2C_ADDR, REG_CONFIG, 0xA0)


# Read calibration coefficients
def read_calibration_params():
    calib = []
    for i in range(0x88, 0x88+24):
        calib.append(bus.read_byte_data(BMP280_I2C_ADDR, i))
    # Data conversion (little endian)
    dig_T1 = calib[1] << 8 | calib[0]
    dig_T2 = (calib[3] << 8 | calib[2])
    dig_T3 = (calib[5] << 8 | calib[4])
    dig_P1 = calib[7] << 8 | calib[6]
    dig_P2 = (calib[9] << 8 | calib[8])
    dig_P3 = (calib[11] << 8 | calib[10])
    dig_P4 = (calib[13] << 8 | calib[12])
    dig_P5 = (calib[15] << 8 | calib[14])
    dig_P6 = (calib[17] << 8 | calib[16])
    dig_P7 = (calib[19] << 8 | calib[18])
    dig_P8 = (calib[21] << 8 | calib[20])
    dig_P9 = (calib[23] << 8 | calib[22])

    def signed(val):  # helper for signed short
        return val - 65536 if val > 32767 else val

    return {
        "T1": dig_T1,
        "T2": signed(dig_T2),
        "T3": signed(dig_T3),
        "P1": dig_P1,
        "P2": signed(dig_P2),
        "P3": signed(dig_P3),
        "P4": signed(dig_P4),
        "P5": signed(dig_P5),
        "P6": signed(dig_P6),
        "P7": signed(dig_P7),
        "P8": signed(dig_P8),
        "P9": signed(dig_P9),
    }


# Compensation algorithm according to datasheet
def compensate_temp_press(adc_T, adc_P, calib):
    # Temperature
    var1 = (((adc_T >> 3) - (calib["T1"] << 1)) * calib["T2"]) >> 11
    var2 = (((((adc_T >> 4) - calib["T1"]) *
            ((adc_T >> 4) - calib["T1"])) >> 12) * calib["T3"]) >> 14
    t_fine = var1 + var2
    T = (t_fine * 5 + 128) >> 8

    # Pressure
    var1 = t_fine - 128000
    var2 = var1 * var1 * calib["P6"]
    var2 = var2 + ((var1 * calib["P5"]) << 17)
    var2 = var2 + (calib["P4"] << 35)
    var1 = ((var1 * var1 * calib["P3"]) >> 8) + ((var1 * calib["P2"]) << 12)
    var1 = (((1 << 47) + var1) * calib["P1"]) >> 33

    if var1 == 0:
        return T / 100.0, 0  # Avoid division by zero

    p = 1048576 - adc_P
    p = (((p << 31) - var2) * 3125) // var1
    var1 = (calib["P9"] * (p >> 13) * (p >> 13)) >> 25
    var2 = (calib["P8"] * p) >> 19
    p = ((p + var1 + var2) >> 8) + (calib["P7"] << 4)

    return T / 100.0, p / 256.0


if __name__ == "__main__":
    calib = read_calibration_params()

    # Reading loop
    while True:
        data = bus.read_i2c_block_data(BMP280_I2C_ADDR, REG_PRESS_MSB, 6)
        adc_P = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_T = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)

        temp, press = compensate_temp_press(adc_T, adc_P, calib)

        print(f"Temperature : {temp:.2f} °C")
        print(f"Pressure : {press:.2f} Pa")
        print("-----------------------------")

        time.sleep(1)
