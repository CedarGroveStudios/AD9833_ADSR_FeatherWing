# AD9833_FeatherWing_REF_volume_v01.py
# 2019-07-31 Cedar Grove Studios
# At test of controlling volume using the M4 DAC AREF pin
#     using Cedar Grove AD9833 Precision Waveform
#     Generator FeatherWing as the volume control
#
#      cedargrove_AD9833_FeatherWing library
#
# Tested with Adafruit Feather M4 Express and CircuitPython 4.1.0 rc-1.

import board
import busio
import time
import audioio

# establish class instance with chip_select pin D6
import cedargrove_AD9833_FeatherWing as AD9833
wave_gen = AD9833.WaveGenerator(select="D6")

wave_gen.reset()  # reset and stop the wave generator; reset all registers
wave_gen.wave_type = "sine"
wave_gen.update_freq(0.1)  # 1Hz
wave_gen.start()  # start wave generator to run a 1Hz triangle wave

# use one of M4's DACs to output a wave file
# connect output of AD9833 wing to Feather AREF (after removing AREF to 3.3v trace)
audio = audioio.AudioOut(board.A0)
f = open("1kHz_tone.wav", "rb")
wave = audioio.WaveFile(f)

# *** Helpers ***

# *** Main code area ***
print("AD9833_FeatherWing_AREF_volume_v01.py")

while True:
    print("playing")
    audio.play(wave, loop=True)
    while audio.playing:
      pass
    print("stopped")
