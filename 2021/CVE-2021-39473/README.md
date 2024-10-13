# CVE-2021-39473

## Affected Product Code Base
HotelManager - v1.2

## Affected Component
Kernel.php; Middleware

## Attack Type
Remote

## Attack Vectors
To exploit this vulnerability the user needs to create "rooms" or "guests" or "reservations" or "users" and in the "comment" or "contact" field can execute a xss payload without even doing any bypass.

This is a stored XSS since I was able to store payloads on endpoints (rooms, guests, ...) and trigger them using different accounts.

## Link to the issue
https://github.com/Saibamen/HotelManager/issues/49
https://github.com/Saibamen/HotelManager/issues/49
