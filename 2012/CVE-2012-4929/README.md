# CRIME-poc

CRIME attack : a compression oracle attacks [CVE-2012-4929](https://cve.mitre.org/cgi-bin/cvename.cgi?name=cve-2012-4929) discovered by Juliano Rizzo and Thai Duong;

> In a compression oracle attack the use of adaptive data compression on a mixture of chosen plaintext and unknown plaintext can result in content-sensitive changes in the length of the compressed text that can be detected even though the content of the compressed text itself is then encrypted. This can be used in protocol attacks to detect when the injected known plaintext is even partially similar to the unknown content of a secret part of the message, greatly reducing the complexity of a search for a match for the secret text. The CRIME and BREACH attacks are examples of protocol attacks using this phenomenon.

The CRIME attack allows you to retrieve encrypted data send by a client to a server using the length of the encrypted data. It does not allow you to retrieve the private key used to encrypt the message or the HTTP request.

## Table of Contents

1. [Explanation](#explanation)
2. [Proof Of Concept](#proof-Of-Concept)
   1. [RC4 stream cipher](#rc4-stream-cipher)
   2. [CBC cipher mode](#cbc-cipher-mode)
3. [Exploit](#exploit)

## Explanation

Many articles explain how the CRIME attack works, but this is the best explanations I found on the internet :

1. [this answer: Crime how to beat the beast successor](https://security.stackexchange.com/questions/19911/crime-how-to-beat-the-beast-successor/19914#19914)
2. [SSL Attacks Survey from NCC Group](https://www.nccgroup.trust/globalassets/our-research/us/whitepapers/ssl_attacks_survey.pdf)

This attack is really not complex, the really interesting part is the implementation that is a bit different from the 'theory'.

Let's check the naive method as described in the article, it's a good way to understand how it works : 

The attacker can control request send by the client (using javascript for example). The goal is to retrieve secret cookie. The attacker sends multiple requests like this and check the length of the encrypted data :

| Reques | length
|---|---|
| GET /cookie=  DATA cookie=quokkalight | **80** |
| GET /cookie=a DATA cookie=quokkalight | 81 |
| GET /cookie=b DATA cookie=quokkalight | 81 |
| GET /cookie=. DATA cookie=quokkalight | 81 |
| GET /cookie=**q** DATA cookie=quokkalight | **80** |

Since `cookie=q` match `cookie=quokkalight` from the secret cookie, the length of the encrypted data will be the same and the attacker know he found a byte.

But this method failed some times and cannot be trusted so instead we will use another method.
First we send a request with the char we want to find followed by multiple caracters that cannot be found in the initial request like some specials chars :`chr(i) + "#:/[@/&"`. Then we send a second request but we invert the payload like this: `"#:/[@/&" + chr(i)` and we compare the two length. If `len(enc(req1)) < len(enc(req2))` then we found a byte. This method is called: `two_tries` and it's a lot more reliable :

| Request to retrieve  byte q | length
|---|---|
| GET /cookie=a~#:/[@/& DATA cookie=quokkalight | 81 |
| GET /cookie=~#:/[@/&a DATA cookie=quokkalight | 81 |
| GET /cookie=b~#:/[@/& DATA cookie=quokkalight | 81 |
| GET /cookie=~#:/[@/&b DATA cookie=quokkalight | 81 |
| GET /cookie=q~#:/[@/& DATA cookie=quokkalight | **80** |
| GET /cookie=~#:/[@/&q DATA cookie=quokkalight | **81** |

The attacker found a byte !

```python
if len(enc(request1)) < len(enc(request2)):
    print("found byte")
```

The method `two_tries` I implemented is fully recursive but why ? some time, more than one byte can be found because the compression match with multiple patterns.

Lets take the secret : `cookie=quokkalight`, if we run the algorithm `two_tries` we will found the following result:

```python
result 1: cookie=quokie=quokie=quokie=quokie=quokie=
result 2: cookie=quokkalight
```

The algorithm needs to take all the paths in the tree in order to find all the possible solutions.
We can see the all the results as a tree that can be respresented like this:

![img](https://user-images.githubusercontent.com/5891788/39074732-e73d07bc-44f2-11e8-952e-849e56e8f95a.png)

## Proof Of Concept

### RC4 stream cipher

The proof of concept of CRIME attack against the stream cipher mode can be found in the file : `CRIME-RC4-poc.py`. This is an implementation in python of the previous explanation.

```bash
python3 CRIME-RC4-poc.py
```

Full demo and result:

[![asciicast](https://asciinema.org/a/igA5aaqc5Mf0RMklxuPu6aPyw.png)](https://asciinema.org/a/igA5aaqc5Mf0RMklxuPu6aPyw)

### CBC cipher mode

When CBC cipher mode is used with AES or DES the attack is not as simple as RC4. Since everything is divided in block the attacks is a bit more tricky (not too much).

![cbc](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/CBC_encryption.svg/601px-CBC_encryption.svg.png)

For example let say we use AES with CBC cipher mode, the block will be devided with a length of 16 and a padding will be added to the end if `len(data)%16 != 0`.
In the mode CBC, it's important to note that the payload `payload=rand` will produce a length of 16 and not 12 since a padding will be add at the end of the data **before** encryption. So our previous attack cannot works.

Example :

| block1 | block2 | block3 | length
|---|---|---|---|
| GET /cookie=  DA | TA cookie=quokka | light + PAD(11) | **48** |
| GET /cookie=a DA | TA cookie=quokka | light + PAD(10) | **48** |
| GET /cookie=b DA | TA cookie=quokka | light + PAD(10) | **48** |
| GET /cookie=. DA | TA cookie=quokka | light + PAD(10) | **48** |
| GET /cookie=**q** DA | TA cookie=quokka | light + PAD(11) | **48** |

In this example, the length will be always the same because if we add or remove a byte, the length will always be the same, **only the padding will change**. The attacker only see the encrypted data and he has no way to know the padding using the encrypted data.

Solution: play with the specification of the CBC mode, so the padding length will be 1 by adding random value in the **GARB** variable (in the GET parameter since the attacker control the GET and POST data)

| block1 | block2 | block3 | block4 | length
|---|---|---|---|---|
| GET /GARBc | ookie=  DATA coo | kie=quokkalight + PAD(1) | | **48** |
| GET /GARBc | ookie=a DATA coo | kie=quokkalight | PAD(16) | 64 |
| GET /GARBc | ookie=b DATA coo | kie=quokkalight | PAD(16) | 64 |
| GET /GARBc | ookie=. DATA coo | kie=quokkalight | PAD(16) | 64 |
| GET /GARBc | ookie=**q** DATA coo | kie=quokkalight + PAD(1) | | **48** |

If the byte match a pattern, the length will be the same, if it doesn't match, the length will be different.

Next, we just have to use the same method explain in the RC4 part, we just add a step before.

1. we call the function `adjust_padding()` so we can have a padding of length 1
2. we call the function `two_tries_recursive()` and we can find the secret FLAG !

```bash
python3 CRIME-cbc-poc.py
```

[![asciicast](https://user-images.githubusercontent.com/5891788/39086213-b604a438-458e-11e8-8626-f1a78c37f410.png)](https://asciinema.org/a/6XrXwP4B4pwTxHrCdwtvz1tfX)

## Exploit

<del>coming really soon...</del>

```
                \     /
                 \ _ /
              ----/_\----
  x--------------( . )--------------x
       x|x   | |_|\_/|_| |   x|x
        x    x           x    x     
```

## References

https://www.nccgroup.trust/globalassets/our-research/us/whitepapers/ssl_attacks_survey.pdf
https://github.com/cloudflare/cf-nocompress
https://www.ekoparty.org/archive/2012/CRIME_ekoparty2012.pdf
https://security.stackexchange.com/questions/19911/crime-how-to-beat-the-beast-successor/19914#19914
