# AD9833_ADSR_FeatherWing
### _An amplitude-controlled version of the original AD9833 Waveform Generator FeatherWing_

![Image of FeatherWing](https://github.com/CedarGroveStudios/AD9833_ADSR_FeatherWing/blob/master/photos/Waveform_Gen_ADSR_close_wide.png)

## Overview
The AD9833 ADSR FeatherWing project is a software and hardware extension of previous work done on the AD9833 Waveform Generator FeatherWing. The ADSR project adds output amplitude control to simulate the Attack-Decay-Sustain-Release envelope needed to simulate musical instrument sounds.
The AD9833 ADSR FeatherWing is an Adafruit Feather-compatible module. The Waveform Generator portion, controlled by SPI, produces an op-amp buffered sine, triangle, or square wave output with a practical frequency range of 0.5Hz to 100KHz with 0.1Hz resolution. The on-board AD5245 Digital Potentiometer is a 256-step 10K potentiometer controlled by I2C. This PCB version includes enhanced power supply noise reduction and an improved output buffer amplifier with higher gain-bandwidth product.

Example MIDI synthesizer and sweep generator code is provided in the repository (sweep example video: https://youtu.be/O1vMfLoCWzg). 
MIDI synthesizer and sweep generator code was tested with a Feather M4 Express using CircuitPython version 4.1.0 rc-1.

MIDI note input was received by a Classic MIDI Interface FeatherWing from a variety of MIDI sources. See https://github.com/CedarGroveStudios/Classic_MIDI_FeatherWing for details.

OSH Park shared PCB project: https://oshpark.com/shared_projects/nDZsxzWR

## AD5245 Digital Potentiometer for Envelope Control
Unlike using the Feather's internal DAC as a multiplying DAC by applying a waveform to the DAC's reference voltage input, the digital potentiometer doesn't require a reference bias, eliminating the distortion that happens when the DAC's reference voltage is less than about 1v. The digital potentiometer's internal MOSFET switches are biased differently than a DAC, allowing the AD5245 potentiometer to control voltage values between ground and Vcc.

![Digital Potentiometer Circuit](https://github.com/CedarGroveStudios/AD9833_ADSR_FeatherWing/blob/master/photos/ADSR_digipot_concept.png)
![Digital Potentiometer Circuit](https://github.com/CedarGroveStudios/AD9833_ADSR_FeatherWing/blob/master/photos/DS1Z_QuickPrint12.png)

The resulting envelope met the original design expectations for distortionless scaling of the waveform's amplitude. The only issue faced was limited I2C data transfer rates during short-duration envelope segments such as shown during the Sustain segment below.

![Digital Potentiometer Circuit](https://github.com/CedarGroveStudios/AD9833_ADSR_FeatherWing/blob/master/photos/DS1Z_QuickPrint13.png)

The latest version of the envelope segment control algorithm was modified to use a fixed time interval approach rather than a variable time interval based on segment duration. In the newest code, the digital potentiometer updates regularly every 1ms during segment generation, a speed easily accommodated by CircuitPython and the Feather M4 Express.

![FeatherWing Implementation Chart](https://github.com/CedarGroveStudios/AD9833_ADSR_FeatherWing/blob/master/docs/FeatherWing_Impl_Chart.png)

## Primary Project Objectives
1)	Generate a smooth ADSR modulated waveform from the AD9833 across the audio spectrum (1Hz to 20KHz).  
2)	Implement with CircuitPython code.
3)  Develop CircuitPython libraries for the AD9833 and AD5245.
4)  Improve output bandwidth.
5)  Reduce power supply noise bleedthrough.
## Deliverables
1)	CircuitPython test, example, and library code
2)  Updated custom FeatherWing PCB  
  a) FeatherWing Implementation Chart  
  b) KiCAD schematic and board layout with Gerber code  
3)	OSH Park public shared project page
4)	GitHub public repository page
5)	Project description and report
## Concepts Learned
1)  The digital potentiometer approach is very viable and eliminates the multiplying DAC reference input bias distortion issue. 
2)  The digital potentiometer's 256-step resolution appears to be sufficient for artifactless envelope generation.
## Next Steps
  * Create a version of the PCB for the low-power AD9837 device (thanks to @jeffwurz).
  * Design a Eurorack-compatible version that provides MIDI and CV/Gate inputs.
  * Design a desktop test equipment version with display and selector knob.
  *	Incorporate the knowledge and experience gained in this project into the design of an Arbitrary Waveform Generator FeatherWing.

![Digital Potentiometer Circuit](https://github.com/CedarGroveStudios/AD9833_ADSR_FeatherWing/blob/master/photos/Waveform_Gen_ADSR_wide.png)
