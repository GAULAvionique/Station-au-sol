import os
import time
import fcntl

I2C_SLAVE = 0x0703
LCD_ADDR = 0x27  # 0x26 For the other LCD
I2C_DEV = "/dev/i2c-1"

# LCD Commands
LCD_CHR = 1  # Character mode
LCD_CMD = 0  # Command mode

# Flags
LCD_BACKLIGHT = 0x08  # On
ENABLE = 0b00000100   # Enable bit

# LCD Instructions
LCD_LINE = [0x80, 0xC0, 0x94, 0xD4]  # Addresses for lines 1-4


class I2CLcd:
    def __init__(self, i2c_addr=LCD_ADDR):
        self.fd = os.open(I2C_DEV, os.O_RDWR)
        fcntl.ioctl(self.fd, I2C_SLAVE, i2c_addr)
        self.init_lcd()

    def write_byte(self, data):
        os.write(self.fd, bytes([data]))

    def toggle_enable(self, bits):
        self.write_byte(bits | ENABLE)
        time.sleep(0.0005)
        self.write_byte(bits & ~ENABLE)
        time.sleep(0.0001)

    def send_byte(self, bits, mode):
        high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT
        self.write_byte(high)
        self.toggle_enable(high)
        self.write_byte(low)
        self.toggle_enable(low)

    def command(self, cmd):
        self.send_byte(cmd, LCD_CMD)

    def write_char(self, char):
        self.send_byte(ord(char), LCD_CHR)

    def init_lcd(self):
        self.command(0x33)
        self.command(0x32)
        self.command(0x28)  # 4 bits, 2 lines, 5x8 dots
        self.command(0x0C)  # Display on, cursor off
        self.command(0x06)  # Auto-increment
        self.command(0x01)  # Clear screen
        time.sleep(0.005)

    def write_line(self, text, line):
        if 0 <= line < 4:
            self.command(LCD_LINE[line])
            for char in text.ljust(20):  # LCD2004 = 20 columns
                self.write_char(char)

    def clear(self):
        self.command(0x01)
        time.sleep(0.002)

    def close(self):
        os.close(self.fd)


if __name__ == "__main__":
    lcd = I2CLcd()
    try:
        lcd.write_line("A_LAT:  00.00000", 0)
        lcd.write_line("A_LON: 000.00000", 1)
        lcd.write_line("B_LAT:  00.00000", 2)
        lcd.write_line("B_LON: 000.00000", 3)
        # lcd.write_line("A_ALT", 0)
        # lcd.write_line("A_SPD", 1)
        # lcd.write_line("B_ALT", 2)
        # lcd.write_line("B_SPD", 3)

    finally:
        # time.sleep(10)
        # lcd.clear()
        lcd.close()
