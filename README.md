# Thermostat

## Description

This project builds a thermostat that controls a gas heater with a thermocouple
powered gas valve and has a web interface. It uses a Raspberry Pi Pico W
board. The tempurature and humidity are sensed by a SHT30 device. The gas
valve is controlled by a relay.

## Setup
See https://projects.raspberrypi.org/en/projects/get-started-pico-w/1

1. Download micro-python run-time.
2. Use BOOTSEL button to mount board at /media/<user-name>.
3. copy run-time file to board. Board will un-mount automatically.
4. Install thonny.
5. Install rshell and test REPL with the following code:
     `from machine import Pin`
     `led = Pin("LED", Pin.OUT)`
     `led.toggle`
 Use ctrl-x to exit rshell.
5. Install ampy (pip3 install adafruit-ampy).
6. Find the name of the Pico serial port. Board I am using is at
 /dev/ttyACM0.

I prefer to use nvim for editing and rshell/ampy to run. The thonny IDE does
all this.

Ampy key commands: ampy --port <port-path> put <python-file-path>
                   ampy --port <port-path> run -n <python-file-name>
The '-n' causes ampy to disconnect after starting the program. This is
required otherwise ampy times-out waiting for program to end. Use the
following screen command to get program output:

screen /dev/ttyACM0 115200


## Code
Started out with gettingStarted.py. This is code from Raspberry Pi
Foundation "Getting Started with your Raspberry Pi Pico W".
