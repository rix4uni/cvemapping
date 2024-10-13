# CVE-2021-36460

NVD CVE-2021-36460:
https://nvd.nist.gov/vuln/detail/CVE-2021-36460

MITRE CVE-2021-36460:
https://cve.mitre.org/cgi-bin/cvename.cgi?name=2021-36460

## [CWE-836: Use of Password Hash Instead of Password for Authentication](https://cwe.mitre.org/data/definitions/836.html)

The VeryFitPro app (Android: [com.veryfit2hr.second](https://play.google.com/store/apps/details?id=com.veryfit2hr.second), [iOS](https://apps.apple.com/us/app/veryfitpro/id1176428281)) <=3.3.7 hashes the account's password locally on the device using SHA-1 and uses the hash to authenticate in all communication with the backend API, including login, registration and changing of passwords.

This allows an attacker in possession of a hash to takeover a user's account without knowing the original password, rendering the security benefits of storing hashed passwords in the database useless.
This is also known as a [Pass the Hash attack](https://attack.mitre.org/techniques/T1550/002/).

As of the 22nd of April 2022, both Android and iOS apps **are affected in their most recent versions** (3.3.7).
The Android app has **over 10,000,000 installs**, the iOS app has 3.4K ratings and is the #198 app in the "Health & Fitness" category.

## Proof of concept

For example, during login, the app hashes the password entered by the user using SHA-1 locally on the device and then makes a `POST` request to the URL `http://veryfitproapi.veryfitplus.com/user/login` with a request body like this:

```
area=Europe&password=5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8&account=foo%40bar.com
```

The backend then parses the request body, comparing the hash value defined by the `password` key with the hash stored in the database in order to verify authentication of the user.

### Attack scenario

1. Attacker obtains the password hash of a user, for example through SQL injection, information exposure or sniffing
2. Attacker performs login on any Android device / emulator or iOS device using the VeryFitPro app
3. Attacker intercepts the `POST` login request and replaces in the request body the hash value of `password` and the email address of `account` with the user's
4. Attacker is now logged in as the user
5. Attacker can now impersonate the user and perform actions like changing the password by using the app

## Mitigation

- In the apps, transmit the original password (unhashed) in the request body via HTTPS to the backend API.
- In the backend, hash the password parsed from the request body before comparing it to the hash in the database.
- In order to mitigate [CWE-327](https://cwe.mitre.org/data/definitions/327.html), the passwords must be hashed using a strong algorithm like [Argon2](https://github.com/P-H-C/phc-winner-argon2)

## Timeline

- **25th of June 2021**: Vulnerability found by [@martinfrancois](https://github.com/martinfrancois), CVE ID requested and vendor contacted
- **28th of June 2021**: No reply from vendor, contacted vendor again
- **6th of April 2022**: [CVE-2021-36460](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-36460) received
- **15th of April 2022**: No reply from vendor, contacted vendor again
- **22nd of April 2022**: No reply from vendor, [advisory](https://github.com/martinfrancois/CVE-2021-36460) published
