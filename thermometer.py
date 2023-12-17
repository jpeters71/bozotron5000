import time
import board
import busio
from utils import turn_pin_on
import adafruit_ahtx0


# Thermometer pins
i2c_scl = board.D22
i2c_sda = board.D21
thermometer_power = board.D27

sensor = None
i2c = None


def init_thermometer():
    global sensor
    global i2c

    turn_pin_on(thermometer_power)
    time.sleep(2.0)
    i2c = busio.I2C(i2c_scl, i2c_sda)
    sensor = adafruit_ahtx0.AHTx0(i2c)
    resp = sensor.calibrate()
    print(f'CALIBRATE RESP: {resp}')


def get_temperture_humidity():
    temp = sensor.temperature * 1.8 + 32
    humidity = sensor.relative_humidity

    return temp, humidity


def calibrate():
    return sensor.calibrate()
