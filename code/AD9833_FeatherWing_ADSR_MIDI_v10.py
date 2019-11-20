# AD9833_FeatherWing_ADSR_MIDI_v10.py
# 2019-08-25 Cedar Grove Studios
# Simple MIDI voice module using Cedar Grove AD9833 Precision Waveform
#     Generator FeatherWing, Cedar Grove Classic MIDI FeatherWing, and
#     Cedar Grove AD5245 Digital Potentiometer Breakout
#
#      cedargrove_AD9833_FeatherWing library
#      cedargrove_MIDI_util library
#      cedargrove_AD5245 library
#
# Tested with Adafruit Feather M4 Express and CircuitPython 4.1.0 rc-1.

import cedargrove_ad5245
digi_pot = cedargrove_ad5245.AD5245(address=0x2C)
digi_pot.shutdown()  # mute the output before instantiating wave_gen

# establish class instance with chip_select pin D6
import cedargrove_AD9833_FeatherWing as AD9833
wave_gen = AD9833.WaveGenerator(select="D6")

import board
import busio
import time
from math import sin
import adafruit_midi
import usb_midi

from cedargrove_MIDI_util import *

from adafruit_midi.timing_clock            import TimingClock
from adafruit_midi.channel_pressure        import ChannelPressure
from adafruit_midi.control_change          import ControlChange
from adafruit_midi.note_off                import NoteOff
from adafruit_midi.note_on                 import NoteOn
from adafruit_midi.pitch_bend              import PitchBend
from adafruit_midi.polyphonic_key_pressure import PolyphonicKeyPressure
from adafruit_midi.program_change          import ProgramChange
from adafruit_midi.start                   import Start
from adafruit_midi.stop                    import Stop
from adafruit_midi.system_exclusive        import SystemExclusive
from adafruit_midi.midi_message            import MIDIUnknownEvent

UART = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = adafruit_midi.MIDI(midi_in=UART, midi_out=UART, in_channel=0, out_channel=0)

# *** Helpers ***

def amplitude_stepper(start, end, period, level=1.0, debug=False):  # step from start to end amplitude over time period
    step = 0.001  # step through segment in 1ms steps
    seg_time = 0
    if start < end:
        while seg_time <= period:
            angle = (3 / 2 * 3.14159) + ((3.14159 * (seg_time / period)))
            amplitude = (start + ((end - start) * ((sin(angle) + 1) / 2))) * level
            digi_pot.normalized_wiper = amplitude
            if debug: print((amplitude,))
            time.sleep(step)
            seg_time = seg_time + step
    elif start > end:
         while seg_time <= period:
            angle = (1 / 2 * 3.14159) + ((3.14159 * (seg_time / period)))
            amplitude = (end + ((start - end) * ((sin(angle) + 1) / 2))) * level
            digi_pot.normalized_wiper = amplitude
            if debug: print((amplitude,))
            time.sleep(step)
            seg_time = seg_time + step
    else:  # start = end
        while seg_time <= period:
            digi_pot.normalized_wiper = start * level
            if debug: print((start * level,))
            time.sleep(step)
            seg_time = seg_time + step

def wave_ADSr(a=(1.0,0), d=(1.0,0), s=(1.0,0), level=1.0):
    amplitude_stepper(0, a[0], a[1], level)  # attack
    amplitude_stepper(a[0], d[0], d[1], level)  # decay
    amplitude_stepper(d[0], s[0], s[1], level)  # sustain

def wave_adsR(s=(1.0,0), r=(0.0,0), level=1.0):
    amplitude_stepper(s[0], r[0], r[1], level)  # release

# *** Main code area ***
print("AD9833_FeatherWing_ADSR_MIDI_v10.py")
print("Input channel:", midi.in_channel + 1 )

# establish initial parameters
adsr_A  = (1.0, 0.090)  # attack level, period in seconds
adsr_D  = (0.8, 0.080)  # decay level, period in seconds
adsr_S  = (0.8, 0.002)  # sustain level, period in seconds
adsr_R  = (0.0, 0.080)  # release level, period in seconds

t0 = time.monotonic_ns()
tempo = 0.0  # establish initial tempo value
playing = []  # set up LIFO buffer for notes

wave_type = "sine"  # sine, triangle, or square waveform
wave_gen.reset()  # reset and stop the wave generator; reset all registers
wave_gen.wave_type = wave_type  # load the waveform type value
wave_gen.stop
digi_pot.shutdown()  # squelch output

while True:
    msg = midi.receive()

    if msg is not None:
        # midi.send(msg)  # MIDI thru
        if isinstance(msg, NoteOn):
            print("NoteOn : #%02d %s %5.3fHz" % (msg.note, note_lexo(msg.note), note_freq(msg.note)))
            print("     vel   %03d     chan #%02d" %(msg.velocity, msg.channel + 1))

            if msg.velocity == 0:  # some note wants to stop playing now
                if len(playing) != 0:
                    if msg.note == playing[-1][0]:  # stop playing the current note
                        wave_adsR(adsr_S, adsr_R, playing[-1][1] / 127)
                        digi_pot.shutdown()  # mute output
                        playing.pop()  # remove current note from the list
                    else:  # otherwise just remove it from the list so that it won't replay
                        for i in range(0, len(playing)):
                            if playing[i][0] == msg.note:
                                playing.remove(playing[i])
                                break
            else:
                if len(playing) != 0:
                    if msg.note != playing[-1][0]:  # another note wants to play over the top of current note
                        wave_adsR(adsr_S, adsr_R, playing[-1][1] / 127)  # release current note
                        digi_pot.shutdown()  # mute output
                        playing.pop()  # remove current note from the list

                wave_gen.update_freq(note_freq(msg.note))  # set frequency register and play new note
                wave_gen.start()  # start oscillator
                wave_ADSr(adsr_A, adsr_D, adsr_S, msg.velocity / 127)
                playing.append((msg.note, msg.velocity))  # add new note to the playing list

        elif isinstance(msg, NoteOff):
            print("NoteOff: #%02d %s %5.3fHz" % (msg.note, note_lexo(msg.note), note_freq(msg.note)))
            print("     vel   %03d     chan #%02d" %(msg.velocity, msg.channel + 1))
            if len(playing) != 0:
                if msg.note == playing[-1][0]:  # stop playing the current note
                    wave_adsR(adsr_S, adsr_R, playing[-1][1] / 127)
                    digi_pot.shutdown()  # mute output
                    playing.pop()  # remove current note from the list
                else:  # otherwise just remove it from the list so that it won't replay
                    for i in range(0, len(playing)):
                        if playing[i][0] == msg.note:
                            playing.remove(playing[i])
                            break

        elif isinstance(msg, TimingClock):
            t1 = time.monotonic_ns()
            if (t1-t0) != 0:
                tempo = (tempo + (1 / ((t1 - t0) * 24) * 60 * 1e9)) / 2 # simple running average
                # print("-- Tick: %03.1f BPM" % tempo)  # compared to previous tick
            t0 = time.monotonic_ns()

        elif isinstance(msg, ChannelPressure):
            print("ChannelPressure: ")
            print("     press %03d     chan #%02d" %(msg.pressure, msg.channel + 1))

        elif isinstance(msg, ControlChange):
            print("ControlChange: ctrl #%03d  %s" % (msg.control, cc_decoder(msg.control)))
            print("     value %03d     chan #%02d" %(msg.value, msg.channel + 1))
            if msg.control == 1:  # Modulation
                wave_type = "sine"
                if msg.value > 43: wave_type = "triangle"
                if msg.value > 86: wave_type = "square"
                wave_gen.wave_type = wave_type
                wave_gen.start()

        elif isinstance(msg, PitchBend):
            print("PitchBend: ")
            print("     bend  %05d   chan #%02d" %(msg.pitch_bend, msg.channel + 1))

        elif isinstance(msg, PolyphonicKeyPressure):
            print("PolyphonicKeyPressure:")
            print("          #%02d %s %5.3fHz" % (msg.note, note_lexo(msg.note), note_freq(msg.note)))
            print("     press %03d     chan #%02d" %(msg.pressure, msg.channel + 1))

        elif isinstance(msg, ProgramChange):
            print("ProgramChange:")
            print("     patch %03d     chan #%02d" %(msg.patch, msg.channel + 1))

        elif isinstance(msg, (Start, Stop)): print("-- %s --" % str(type(msg))[8:-2])

        elif isinstance(msg, SystemExclusive):
            print("SystemExclusive:  ID= ", msg.manufacturer_id,
                ", data= ", msg.data)
            print("--------------------")

        elif isinstance(msg, MIDIUnknownEvent):
            # Message are only known if they are imported
            print("Unknown MIDI event status ", msg.status)
