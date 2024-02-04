# Home thermostat program that supports a web interface and controls a
# thermocouple equipped stove by supplying current to the stove's
# gas valve.

import network
import socket
from time import sleep
import machine
from sht30 import SHT30

# WiFi credentials
ssid = 'TP-Link_E787'
password = '35858164'
# ip = None

pico_led = machine.Pin("LED", machine.Pin.OUT)
sensor = SHT30()

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Connecting to network...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def round(x):
    return int(x + 0.5)


#            <meta http-equiv="refresh" content="5"/>
#            <meta http-equiv='cache-control' content='no-cache'>
#            <meta http-equiv='expires' content='0'>
#            <meta http-equiv='pragma' content='no-cache'>

def web_page(temperature, humidity, setting):

    # template HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Thermostat</title>
        </head>
        <body>
            <table width = "100% border = "0">
			<tr>
				<td colspan = "3" bgcolor = "#b5dcb3">
				       <h1 style="font-size: 4em;" align = "center">Thermostat</h1>
			       </td>
			</tr>
			<tr>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" align = "right"></h1>
				</td>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" align = "center">{temperature}&deg</h1>
					<h1 style="font-size: 3em;" align = "center">Temperature</h1>
				</td>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" ></h1>
				</td>
			</tr>
			<tr>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
                    <form action="./decrease">
                        <input style="font-size: 6em;" type="submit" value="&lt">
                    </form>
				</td>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" align = "center">{setting}&deg</h1>
					<h1 style="font-size: 3em;" align = "center">Setting</h1>
				</td>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
                    <form action="./increase">
                        <input style="font-size: 6em;" type="submit" value="&gt">
                    </form>
				</td>
			</tr>
			<tr>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" ></h1>
				</td>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" align = "center">{humidity}&#37</h1>
					<h1 style="font-size: 3em;" align = "center">Humidity</h1>
				</td>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" ></h1>
				</td>
			</tr>
            </table>
            <div align="center">
                <form action="./refresh">
                    <input style="font-size: 6em;" type="submit" value="Refresh">
                </form>
            </div>
        </body>
    </html>
    """
    return str(html)

# Serve web page. This function does not return. If there is an unhandled
# exception, the program will reset.
def serve(connection):
    setting = 60
    led_state = 'OFF'
    pico_led.off()
    while True:
        client = connection.accept()[0]
        print('client:', client)
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
            print('request:', request)
        except IndexError:
            pass
        if request == '/decrease?':
            setting -= 1
            if setting < 50:
                setting = 50
        elif request == '/increase?':
            setting += 1
            if setting > 80:
                setting = 80
        temperature, humidity = sensor.measure()
        print('Temperature:', temperature, 'ºC, RH:', humidity, '%')
        html = web_page(round((temperature * 1.8) + 32.0), round(humidity), setting)
        client.send(html)
        client.close()

# Connect to WiFi and serve web page.
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
