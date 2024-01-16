import audiobusio
import audiocore
import board
from utils import turn_pin_on


# I2S
i2s_bitclock = board.D19
i2s_wordselect = board.D5
i2s_datapin = board.D18
i2s_power = board.D23


def init_audio():
    turn_pin_on(i2s_power)


def play_wave(filename):
    wave_file = open(filename, "rb")
    wave = audiocore.WaveFile(wave_file)
    print(f"playing wave: {wave_file}")
    i2s = audiobusio.I2SOut(i2s_bitclock, i2s_wordselect, i2s_datapin)
    try:
        i2s.play(wave)
        while i2s.playing:
            pass
    finally:
        i2s.stop()
        i2s.deinit()
