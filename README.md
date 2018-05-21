# Room-Lights-Networked
A solution to sync traditional RGB LED strips with Phillips Hue bulbs. 


## The Problem 
In my dorm room, I have two sources of light: Phillips hue bulbs, and RGB LED strips. Phillips makes an LED strip, however they are VERY expensive and I'd rather make my own. 


## Dependencies

`phue`, a python skin for the phillips API 

`rgbxy`, a small library for converting between the RGB and phillips color spaces 

`pigpio`, a library for controlling Raspberry Pi GPIO pins

All of these can be installed with pip. 

Runs on Python 3, not Python 2.

## Installation

Download the repository, make whichever script you're using executable, and set it to run at boot. 

`rpLights` is the script for controlling the led strips, while `interface` is for controlling an on/off switch 



