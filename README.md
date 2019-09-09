### _ADSR Envelope Extension for the Precision Waveform Generator FeatherWing_
# AD9833_ADSR

![Image of Envelope](https://github.com/CedarGroveStudios/AD9833_ADSR/blob/master/photos/smooth_ADSR_social.png)

## Overview
The AD9833 ADSR project is a software and hardware extension of work done on the AD9833 Precision Waveform Generator FeatherWing. The ADSR project adds output amplitude control to simulate the Attack-Decay-Sustain-Release envelope needed to simulate musical instrument sounds.
The AD9833 Precision Waveform Generator FeatherWing is an Adafruit Feather-compatible module. The Waveform Generator produces an op-amp buffered sine, triangle, or square wave output with a practical frequency range of approximately 0 to 300KHz with 0.1Hz resolution. The AD5245 Digital Potentiometer Breakout is a 256-step 10K potentiometer on a small breadboardable PCB. The breakout has connections for I2C and the potentiometer A, B, and W (wiper) pins.

MIDI note input was received by a Classic MIDI Interface FeatherWing from a variety of MIDI sources.

See https://github.com/CedarGroveStudios/AD9833_FeatherWing, https://github.com/CedarGroveStudios/AD5245_Digital_Pot, and https://github.com/CedarGroveStudios/Classic_MIDI_FeatherWing for details.

A test of signal amplitude control using the AREF pin of the Feather M4 Express' DAC was performed during prototyping. Details of that test can be found here: https://github.com/CedarGroveStudios/AD9833_ADSR/blob/master/M4_DAC_AREF_test.md

ADSR envelope code was tested with a Feather M4 Express using CircuitPython version 4.1.0 rc-1. Example MIDI synthesizer and sweep generator code is provided in the repository (sweep example video: https://youtu.be/O1vMfLoCWzg). 
  
## AD5245 Digital Potentiometer for Envelope Control
Unlike a DAC's reference voltage input, a digital potentiometer typically doesn't require a reference bias, eliminating the distortion that happens when the DAC's reference voltage is less than about 1v. The digital potentiometer's internal MOSFET switches are biased differently than a DAC, allowing the potentiometer to control voltage values between ground and Vcc (as with the AD5245) or up to the value of a separate wiper bias pin (as with the DS3502).

![Digital Potentiometer Circuit](https://github.com/CedarGroveStudios/AD9833_ADSR/blob/master/photos/ADSR_digipot_concept.png)
![Digital Potentiometer Circuit](https://github.com/CedarGroveStudios/AD9833_ADSR/blob/master/photos/DS1Z_QuickPrint12.png)

The resulting envelope met the original design expectations for distortionless scaling the waveform's amplitude. The only issue faced was limited I2C data transfer rates during short-duration envelope segments such as shown during the Sustain segment below.

![Digital Potentiometer Circuit](https://github.com/CedarGroveStudios/AD9833_ADSR/blob/master/photos/DS1Z_QuickPrint13.png)

The latest version of the envelope segment control algorithm was modified to use a fixed time interval approach rather than a variable time interval based on segment duration. In the newest code, the digital potentiometer updates regularly every 1ms during segment generation, a speed easily accommodated by CircuitPython and the Feather M4 Express.

## Primary Project Objectives
1)	Generate a smooth ADSR waveform that modulates the AD9833 output waveform.  
2)	Implement with CircuitPython code and develop an ADSR library.
3)	Update the initial AD9833 FeatherWing design to incorporate ADSR envelope control.
## Deliverables
1)	CircuitPython test, example, and library code
2)  Updated custom FeatherWing PCB, M4 Express pinout  
  a) FeatherWing Implementation Chart  
  b) KiCAD schematic and board layout with Gerber code  
3)	OSH Park public shared project page
4)	GitHub public repository page
5)	Project description and report
## Concepts Learned
1)  A digital potentiometer approach is very viable and eliminates the DAC reference input bias distortion issue. 
7)  The digital potentiometer's 256-step resolution appears to be sufficient for artifactless envelope generation.
## Next Steps
  * Redesign the PCB to include the digital potentiometer.
  * Design a Eurorack-compatible version that provides MIDI and CV/Gate inputs.
  * Design a desktop test equipment version with display and selector knob.
  *	Incorporate the knowledge and experience gained in this project into the design of an Arbitrary Waveform Generator FeatherWing.

