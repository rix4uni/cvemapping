# CVE-2019-17625

There is a stored XSS vulnerability in rambox 0.6.9 due to unsantized parameters in the name field when a user is adding a service. Since rambox runs on NodeJS this allows for the use of OS commands to be injected into an `<a>` or `<img>` tag.

_Note:_ This code has only been tested on MacOS and may need to be reconfigured for other operating systems

# Exploit code

The exploit code will create a service (using discord as a base), the shell requires that the system has `mkfifo` on it. You can of course swap out the payload for whatever you want.

# PoC

![rce_rambox_poc](https://user-images.githubusercontent.com/14183473/66883875-fb30fa00-ef94-11e9-82a0-589006c453a9.gif)
