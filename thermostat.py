# Home thermostat program that supports a web interface and controls a
# thermocouple equipped stove by supplying current to the stove's
# gas valve.

import network
import socket
from time import sleep
import machine

# WiFi credentials
ssid = 'TP-Link_E787'
password = '35858164'
# ip = None

pico_led = machine.Pin("LED", machine.Pin.OUT)

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
    connection.settimeout(0.1)
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def web_page(temperature, led_state):
    # template HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Thermostat</title>
        </head>
        <body>
            <form action="./lighton">
                <input type="submit" value="Light On">
            </form>
            <form action="./lightoff">
                <input type="submit" value="Light Off" />
            </form>
            <p>LED is {led_state}</p>
            <p>Temperature is {temperature}</p>
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
					<h1 style="font-size: 6em;" align = "right">&lt</h1>
				</td>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" align = "center">70&deg</h1>
					<h1 style="font-size: 3em;" align = "center">Setting</h1>
				</td>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" >&gt</h1>
				</td>
			</tr>
			<tr>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" ></h1>
				</td>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" align = "center">50&#37</h1>
					<h1 style="font-size: 3em;" align = "center">Humidity</h1>
				</td>
				<td bgcolor = "#eeeeee" valign = "top" width = "33%">
					<h1 style="font-size: 6em;" ></h1>
				</td>
			</tr>
            </table>
        </body>
    </html>
    """
    return str(html)

# Serve web page. This function does not return. If there is an unhandled
# exception, the program will reset.
def serve(connection):
    led_state = 'OFF'
    pico_led.off()
    temperature = 60
    while True:
        try:
            client = connection.accept()[0]
        except:
            # The socket timed out in this implementation does not appear
            # to be working. This is the only exception expected at this
            # point.
            pass
        else:
            print(client)
            request = client.recv(1024)
            request = str(request)
            try:
                request = request.split()[1]
                print(request)
            except IndexError:
                pass
            if request == '/lighton?':
                pico_led.on()
                led_state = 'ON'
            elif request == '/lightoff?':
                pico_led.off()
                led_state = 'OFF'
            html = web_page(int((temperature * 1.8) + 32.0), led_state)
            client.send(html)
            client.close()

# Connect to WiFi and serve web page.
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
