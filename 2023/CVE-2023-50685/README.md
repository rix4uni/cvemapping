# Hipcam RealServer/V1.0 RTSP Format Validation Vulnerability Proof-of-Concept | CVE-2023-50685

**Proof-of-Concept for RTSP Service Format Validation Vulnerability in Hipcam RealServer/V1.0.**

## Description
This POC exploits a format validation vulnerability in the Real Time Streaming Protocol (RTSP) service of the Hipcam RealServer/V1.0, stemming from inadequate input validation and handling of the 'client_port' parameter in the RTSP SETUP request.

## Vulnerability Details
The 'client_port' parameter in the RTSP SETUP request is manipulated, inducing a vulnerability in the RTSP server's format validation. Unlike conventional exploits with a specific overflow value, this vulnerability is triggered by improper formatting, particularly when the 'client_port' is not in the expected format (e.g., client_port=[custom_port]-[custom_port+1]). Format validation vulnerabilities occur when an application fails to properly validate or handle input, potentially leading to unexpected behavior. In this case, the goal is to disrupt the service.

```python
cam_address = "rtsp://120.75.111.XX:554/11" #The RTSP port is normaly 554 with the path /11 which is also normaly used in Hipcam Cameras
random_data_value = 8712429 #It can be anything except the correct format of [custom_port]-[custom_port+1]
rtsp_request = f"SETUP {cam_address}/trackID=1 RTSP/1.0\r\nCSeq: 3\r\nTransport: RTP/AVP;unicast;client_port={random_data_value}\r\n\r\n"
```

## Exploitation
### Steps
1. Formulate an RTSP URL for the target camera.
2. Craft an RTSP SETUP request with a manipulated 'client_port' parameter (ensure it is not in the expected format).
3. Establish a connection to the RTSP service on the target camera.
4. Send the crafted RTSP request to the camera, attempting to trigger the format validation vulnerability.

### Script Usage
```cli
python3 poc.py 120.75.111.XX 554
python3 poc.py -h
```

## Impact
Upon successful exploitation, the RTSP stream is offline for approximately 45 seconds. This disruption could be leveraged in physical attack scenarios where temporary unavailability of surveillance footage may provide an opportunity for unauthorized access or other malicious activities.

### Shodan Trends
**Timeline**
![Shodan Trend of Hipcam RealServer/V1.0 Devices](/assets_images/shodan_trend_timeline.png)

**Countries**
![Top Ranked Countries with Hipcam RealServer/V1.0 Devices](/assets_images/shodan_trend_countries.png)

For more information on the Shodan trend of Hipcam RealServer, check [Shodan Trends](https://trends.shodan.io/search?query=has_screenshot%3Atrue+port%3A554+%22Hipcam+RealServer%2FV1.0%22#facet/overview).

Search query used: `has_screenshot:true port:554 "Hipcam RealServer/V1.0"`.

## Disclaimer
This script is intended for educational and responsible disclosure purposes only. Unauthorized use of this script on systems without proper authorization is illegal and unethical. The user is responsible for ensuring compliance with legal and ethical standards.
