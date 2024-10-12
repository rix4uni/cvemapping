# EN
This project provides a proof-of-concept exploit for a remote code execution (RCE) vulnerability in Nexxt routers, specifically targeting the version 15.03.06.60. This vulnerability allows an attacker to enable the Telnet service on the router without authentication, potentially gaining unauthorized access.

## CVE Reference
 - **CVE-2022-46080** (Nexxt Router RCE Exploit)

## Features
- **Unauthenticated Remote Code Execution**: Exploit the vulnerability to execute arbitrary code.
- **Telnet Service Activation**: Enables Telnet service on the router with a specified password and port.

## Usage
### Prerequisites
- Python 3.x
- `requests` library

## Installation
```bash
pip install requests
```
## Running the Exploit
To execute the exploit, use the following command format:
```bash
python GenVuln_CVE2022_46080.py [ROUTER_URL] [TELNET_PORT] [TELNET_PASSWORD]
```
## Example
```bash
python GenVuln_CVE2022_46080.py http://192.168.0.1 23 mysecurepassword
```
### Arguments
- **ROUTER_URL**: The URL of the target router (e.g., `http://192.168.0.1`).
- **TELNET_PORT**: The port on which the Telnet service will be enabled.
- **TELNET_PASSWORD**: The password to be set for the Telnet service.

## Help
For usage instructions, run:
```bash
python GenVuln_CVE2022_46080.py -h
```
## Disclaimer
This code is provided for educational purposes only. Unauthorized access to computer systems is illegal. The author of the project is not responsible for any misuse of this code.

# RU
Этот проект предоставляет доказательство концепции эксплойта для уязвимости удаленного выполнения кода (RCE) в роутерах Nexxt, особенно для версии 15.03.06.60. Эта уязвимость позволяет атакующему включить службу Telnet на роутере без аутентификации, что потенциально предоставляет несанкционированный доступ.

## CVE Ссылка
- **CVE-2022-46080** (Nexxt Router RCE Exploit)

## Особенности
- **Удаленное выполнение кода без аутентификации**: Использование уязвимости для выполнения произвольного кода.
- **Активация службы Telnet**: Включает службу Telnet на роутере с указанным паролем и портом.

## Использование
### Требования
- Python 3.x
- Библиотека `requests`

## Установка
```bash
pip install requests
```
## Запуск эксплойта
Для выполнения эксплойта используйте следующую команду:
```bash
python GenVuln_CVE2022_46080.py [ROUTER_URL] [TELNET_PORT] [TELNET_PASSWORD]
```
## Пример
```bash
python GenVuln_CVE2022_46080.py http://192.168.0.1 23 mysecurepassword
```
### Аргументы
- **ROUTER_URL**: URL целевого роутера (например, `http://192.168.0.1`).
- **TELNET_PORT**: Порт, на котором будет включена служба Telnet.
- **TELNET_PASSWORD**: Пароль, который будет установлен для службы Telnet. 

## Справка
Для получения инструкций по использованию выполните:
```bash
python GenVuln_CVE2022_46080.py -h
```

## Отказ от ответственности
Этот код предоставляется исключительно в образовательных целях. Несанкционированный доступ к компьютерным системам является незаконным. Автор проекта не несет ответственности за любое неправильное использование этого кода.
