# Home thermostat program that supports a web interface and controls a
# thermocouple equipped stove by supplying current to the stove's
# gas valve.

import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

# WiFi credentials
ssid = 'TP-Link_E787'
password = '35858164'
# ip = None

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
    connection.settimeout(1.0)
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def web_page(temperature, state):
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
            <p>LED is {state}</p>
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
					<h1 style="font-size: 6em;" align = "center">68&deg</h1>
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

def serve(connection):
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        try:
            client = connection.accept()[0]
        # except:
        except:
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
                state = 'ON'
            elif request == '/lightoff?':
                pico_led.off()
                state = 'OFF'
            temperature = pico_temp_sensor.temp
            html = web_page(temperature, state)
            client.send(html)
            client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
