 ampy -p /dev/ttyACM0 put sht30.py
 ampy -p /dev/ttyACM0 put thermostat.py
 ampy -p /dev/ttyACM0 run -n thermostat.py
 screen /dev/ttyACM0 115200
