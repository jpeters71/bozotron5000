# Bozotron 5000
import os
from audio import init_audio, play_wave
from display import init_display, update_text
import socketpool
from thermometer import calibrate, get_temperture_humidity, init_thermometer
import json
import wifi
import mdns
from adafruit_httpserver import Server, Request, Response, FileResponse


PORT = 9080

# Setup
init_display()
init_audio()
init_thermometer()


# Now, HTTP server
# Wifi params are stored as env vars for circuitpython/esp32
ssid = os.getenv('CIRCUITPY_WIFI_SSID')
password = os.getenv('CIRCUITPY_WIFI_PASSWORD')

print('Connecting to', ssid)
wifi.radio.connect(ssid, password)
print('Connected to', ssid)

pool = socketpool.SocketPool(wifi.radio)
# mdns_server = mdns.Server(wifi.radio)
# mdns_server.hostname = 'bozotron5000'
# mdns_server.advertise_service(service_type='_http', protocol='_tcp', port=PORT)

server = Server(pool, '/static', debug=True)


@server.route('/')
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    return FileResponse(request, 'index.html')


@server.route('/audio/<file_name>', 'POST')
def handle_audio(request: Request, file_name):
    try:
        play_wave(f'/static/{file_name}')
    except Exception as e:
        print(f'EXCEPTION in handle_audio: {e}')
    return Response(request, '{"status": "success"}')


@server.route('/audio/<file_name>', 'OPTIONS')
def handle_audio(request: Request, file_name):
    return Response(
        request,
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Authorization, Content-Type',
            'Access-Control-Allow-Methods': 'POST',
        },
    )


@server.route('/temperature', 'GET')
def handle_temperature(request: Request):
    try:
        temp, humid = get_temperture_humidity()
    except Exception as e:
        print(f'EXCEPTION in handle_temperature: {e}')

    resp = {
        'temperature': temp,
        'humidity': humid,
    }

    return Response(request, json.dumps(resp))


@server.route('/temperature', 'POST')
def handle_temperature_post(request: Request):
    try:
        calibrateStatus = calibrate()
    except Exception as e:
        print(f'EXCEPTION in handle_temperature_post: {e}')

    resp = {'calibrateStatus': calibrateStatus}

    return Response(request, json.dumps(resp))


update_text('Hello!')
server.serve_forever(str(wifi.radio.ipv4_address), port=PORT)
