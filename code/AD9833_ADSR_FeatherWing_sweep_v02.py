# AD9833_ADSR_FeatherWing_sweep_v02.py
# 2019-11-19 Cedar Grove Studios
# Fixed or swept frequency generator example. Update "initial parameters"
# section for required functionality.
#
# uses cedargrove_ad9833 driver
# Tested with Adafruit Feather M4 Express and CircuitPython 4.1.0 rc-1.

import time
import cedargrove_ad5245
digi_pot = cedargrove_ad5245.AD5245(address=0x2C)
digi_pot.shutdown()  # mute the output before instantiating wave_gen

import cedargrove_ad9833
wave_gen = cedargrove_ad9833.AD9833(select='D6')


# *** Helpers ***

# *** Main code area ***
print("AD9833_ADSR_FeatherWing_sweep_v02.py")

# establish initial parameters
begin_freq =  20        # fixed or sweep starting frequency (Hz)
end_freq = 21000        # sweep ending frequency (Hz)
inc_freq = 10           # sweep freqency step size (Hz)
periods_per_step = 3    # number of waveform periods to hold (non-linear mode)
sweep_mode = "non-linear"    # fixed (10ms per step) or non-linear sweep hold timing
freq_mode = "sweep"     # fixed or sweep frequency
wave_type = "sine"      # sine, triangle, or square waveform
amplitude = 1.0         # normalized potentiometer value (0 to 1.0)

debug = True

if debug:
    print("begin:", begin_freq, "  end:", end_freq, "  incr:", inc_freq)
    print("periods per step:", periods_per_step)
    print("sweep mode:", sweep_mode, "  freq mode:", freq_mode, "  wave type:", wave_type)
    time.sleep(1)

while True:
    wave_gen.reset()
    wave_gen.wave_type = wave_type
    wave_gen.start()
    digi_pot.normalized_wiper = amplitude

    if freq_mode == "sweep":
        wave_gen.start()

        for i in range(begin_freq, end_freq, inc_freq):
            if debug: print("sweep: frequency =", i)
            wave_gen.update_freq(i)

            if sweep_mode == "non-linear":
                time.sleep(periods_per_step * (1 / i))  # pause for x periods at the specified frequency
            else:
                time.sleep(0.010)  # 10msec fixed hold time per step
    else:
        # output a fixed frequency for 10 seconds
        if debug: print("fixed: frequency =", begin_freq)
        wave_gen.update_freq(begin_freq)
        wave_gen.start()
        time.sleep(10)  # 10sec fixed hold time

    digi_pot.shutdown()  # mute the output
    wave_gen.stop()  # stop wave generator

    time.sleep(2)  # wait a second then do it all over again
