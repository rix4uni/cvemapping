# CVE-2024-46310
POC for CVE-2024-46310 For FXServer version's v9601 and prior <br>

Incorrect Access Control in FXServer version's v9601 and prior, for CFX.re FiveM, allows unauthenticated users to modify and read userdata via exposed api endpoint

## How to use the script

navigate to [servers.fivem.net](https://servers.fivem.net) <br>
pick a server <br>
copy the join code <br>
and enter it into the script provided in this repository <br>

using this exposed api endpoint we can get the ip address associated with server and user data however when this endpoint is closed it will not fix the issue of every server running FXServer version's v9601 and prior having an exposed /players.json file that unauthenticated users can view and push changes to

## Example of data unauthenticated users can obtain

    {
    "endpoint": "127.0.0.1", (always 127.0.0.1)
    "id": 328, [ingame session ID]
    "identifiers": [
      "steam:", [Steam ID of the user]
      "license:", [FiveM Licence Key]
      "xbl:", [Xbox Live ID]
      "live:", [Xbox Live ID]
      "discord:", [Discord User ID]
      "fivem:", [FiveM User ID]
      "license2:" [FiveM Licence Key]
    ],
    "name": "Example", [FiveM Username of player]
    "ping": 96 [Current Ping of The Player]
    }

## Official public responce from CFX.re after issue was disclosed to them

"To improve player safety, we are also going to deprecate player identifiers from being publicly accessible on servers’ `players.json` endpoint as well as from our server list backend in the coming weeks.<br>
Server owners who want to retain identifiers on their `players.json` for backward-compatibility will be able to use the `sv_exposePlayerIdentifiersInHttpEndpoint` ConVar, but we will implement a safer alternative later this year, allowing for a security string to be passed when querying `players.json`." - CFX.re <br><br>
https://forum.cfx.re/t/celebrating-one-year-with-rockstar-games/
