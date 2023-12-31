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
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def web_page(temperature, state):
    # template HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <body>
        <form action="./lighton">
            <input type="submit" value="Light On">
        </form>
        <form action="./lightoff">
            <input type="submit" value="Light Off" />
        </form>
        <p>LED is {state}</p>
        <p>Temperature is {temperature}</p>
    </body>
    </html>
    """
    return str(html)

def serve(connection):
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
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

