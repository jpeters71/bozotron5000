
import board
import busio
import displayio
import fourwire
from utils import turn_pin_on
from adafruit_st7735r import ST7735R
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import terminalio


# Display Pins
tft_clk = board.D14 # SCK
tft_mosi= board.D13 # SDA
tft_rst = board.D25
tft_dc  = board.D2  # A0
tft_cs  = board.D15
display_power = board.D32 # LED

main_group: displayio.Group = None
display = None
updating_label: label.Label = None


def init_display():
    global main_group
    global display
    global updating_label

    turn_pin_on(display_power)

    displayio.release_displays()

    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
    display_bus = fourwire.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
    display = ST7735R(display_bus, width=128, height=128, rotation=90)

    # Make the main display context
    main_group = displayio.Group()
    display.root_group = main_group
    updating_label = label.Label(terminalio.FONT, text='Bozo', anchor_point=(0,0), anchored_position=(20,20))


def update_text(text: str):
    updating_label.text = text