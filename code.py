# Bozotron 5000
import os
import audiocore
import board
import audiobusio
import socketpool
import wifi
import mdns
from adafruit_httpserver import Server, Request, Response, FileResponse


# Now, HTTP server
ssid = os.getenv(
    "CIRCUITPY_WIFI_SSID"
)  # Gets set automatically for circuitpython/esp32
password = os.getenv(
    "CIRCUITPY_WIFI_PASSWORD"
)  # Gets set automatically for circuitpython/esp32

print("Connecting to", ssid)
wifi.radio.connect(ssid, password)
print("Connected to", ssid)

pool = socketpool.SocketPool(wifi.radio)
mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = "bozotron5000"
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=80)

server = Server(pool, "/static", debug=True)
# server.headers = {
#     "X-Server": "Adafruit CircuitPython HTTP Server",
#     "Access-Control-Allow-Origin": "*",
# }


@server.route("/")
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    return FileResponse(request, "index.html")


@server.route("/audio/<file_name>", "POST")
def handle_audio(request: Request, file_name):
    _play_wave(f"/static/{file_name}")
    return Response(request, '{"status": "success"}')


@server.route("/audio/<file_name>", "OPTIONS")
def handle_audio(request: Request, file_name):
    return Response(
        request,
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
            "Access-Control-Allow-Methods": "POST",
        },
    )


def _play_wave(filename):
    wave_file = open(filename, "rb")
    wave = audiocore.WaveFile(wave_file)
    print(f"playing wave file: {wave}")
    i2s = audiobusio.I2SOut(board.D19, board.D13, board.D12)
    i2s.play(wave)
    while i2s.playing:
        pass
    i2s.stop()


server.serve_forever(str(wifi.radio.ipv4_address))
