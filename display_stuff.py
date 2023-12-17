import board
import busio
import displayio
import digitalio
import terminalio
import fourwire
import time
from adafruit_st7735r import ST7735R 
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import adafruit_ahtx0

# Display
tft_clk = board.D14
tft_mosi= board.D13
tft_rst = board.D25
tft_dc  = board.D2
tft_cs  = board.D15
display_power = board.D33

# Thermometer
i2c_scl = board.D22
i2c_sda = board.D21
thermometer_power = board.D27

# I2S
i2s_bitclock = board.D3
i2s_wordselect = board.D19
i2s_datapin = board.D18
i2s_power = board.D23

# Turn the power on
turn_pin_on(display_power)
turn_pin_on(thermometer_power)
turn_pin_on(i2s_power)

# 
time.sleep(.25)

displayio.release_displays()

spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
display_bus = fourwire.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7735R(display_bus, width=128, height=128, rotation=90)

i2c = busio.I2C(i2c_scl, i2c_sda)

# Make the main display context
main = displayio.Group()
display.root_group = main

main.append(Rect(width=128, height=128, x=0, y=0, fill=0xFF00FF))
main.append(Rect(width=30, height=70, x=0, y=0, fill=0x0000FF))
main.append(Rect(width=20, height=20, x=100, y=100, fill=0x00FF00))
updating_label = label.Label(terminalio.FONT, text='Bozo', anchor_point=(0,0), anchored_position=(20,20))
main.append(updating_label)

sensor = adafruit_ahtx0.AHTx0(i2c)

while True:
    # update text property to change the text showing on the display
    temp = sensor.temperature * 1.8 + 32
    humidity = sensor.relative_humidity
    updating_label.text = f'Time: {time.monotonic()}\n' \
                            + f'Temp: {temp} F\n' \
                            + f'Hum: {humidity}%'

    time.sleep(1)


def turn_pin_on(pin):
    out_pin = digitalio.DigitalInOut(pin)
    out_pin.direction = digitalio.Direction.OUTPUT
    out_pin.value = True
