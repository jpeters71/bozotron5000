import digitalio


def turn_pin_on(pin):
    out_pin = digitalio.DigitalInOut(pin)
    out_pin.direction = digitalio.Direction.OUTPUT
    out_pin.value = True
