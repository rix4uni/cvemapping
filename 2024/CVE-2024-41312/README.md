# CVE-2024-41312.
InstantCMS - Stored Cross Site Scripting (XSS)
Affected Version: InstantCMS 2.16.3

Steps to Reproduce:
1. Log in to https://demo.instantcms.io as an demo user.
2. Visit https://demo.instantcms.io/photos/upload.
3. Upload the image with the embedded payload test `<img src="asd" onerror="alert(1)">` in the Camera Model Name meta data filed.
4. Visit the https://demo.instantcms.io/photos/camera-{payload}
5. Example: https://demo.instantcms.io/photos/camera-Amal_Test%3Cimg+src=%22asd%22+onerror=%22alert(1)%22%3E
6. you will observe the immediate execution of the XSS payload.

POC:

<a href=https://d.pr/v/DT8Gve> Video POV</a>
