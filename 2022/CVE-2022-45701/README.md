# EN
This project provides a Python script to exploit a remote code execution (RCE) vulnerability (CVE-2022-45701) in certain Arris routers. The vulnerability allows authenticated users to execute arbitrary commands on the device by manipulating SNMP settings via the web interface.

**Disclaimer**:\
 This tool is for educational purposes and ethical security testing only. Unauthorized use of this script is illegal and unethical.

## Features
- Exploits CVE-2022-45701 for remote code execution.
- Bypasses router security through SNMP manipulation.
- Supports testing on Arris models TG2482A, TG2492, SBG10.

## Requirements
- Python 3.x
- `requests` library (`pip install requests`)

## Usage
1. Clone the repository:
```bash
git clone https://github.com/geniuszlyy/CVE-2022-45701.git
cd CVE-2022-45701
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Edit the script with your target router's IP, username, password, and your local host and port for reverse shell.
4. Run the exploit:
```bash
python GenVuln_CVE_2022_45701.py
```

## Configuration
- **Router URL**: Default is `http://192.168.0.1`, update if necessary.
- **Credentials**: Default username and password are `admin` and `password`. Update these with the actual credentials.
- **Local Host & Port**: Set your local IP and port for the reverse shell.

## IMPORTANT
This tool is intended for legal and ethical purposes only. It is the user's responsibility to ensure that they have permission to test any devices they use this script on. Unauthorized access to devices and networks is illegal and punishable under law.

# RU
Этот проект предоставляет скрипт на Python для использования уязвимости удаленного выполнения кода (RCE) (CVE-2022-45701) в некоторых маршрутизаторах Arris. Уязвимость позволяет аутентифицированным пользователям выполнять произвольные команды на устройстве путем манипуляций с настройками SNMP через веб-интерфейс.

**Отказ от ответственности**:\
Этот инструмент предназначен только для образовательных целей и этического тестирования безопасности. Несанкционированное использование этого скрипта является незаконным и неэтичным.

## Особенности
- Использует уязвимость CVE-2022-45701 для удаленного выполнения кода.
- Обходит безопасность маршрутизатора через манипуляции с SNMP.
- Поддержка тестирования на моделях Arris TG2482A, TG2492, SBG10.

## Требования
- Python 3.x
- Библиотека `requests` (`pip install requests`)

## Использование
1. Клонируйте репозиторий:
```bash
git clone https://github.com/geniuszlyy/CVE-2022-45701.git
cd CVE-2022-45701
```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Отредактируйте скрипт, указав IP-адрес маршрутизатора, имя пользователя, пароль и ваш локальный хост и порт для обратного shell.
4. Запустите эксплоит:
```bash
python GenVuln_CVE_2022_45701.py
```

## Конфигурация
- **URL маршрутизатора**: По умолчанию `http://192.168.0.1`, измените при необходимости.
- **Учетные данные**: Имя пользователя и пароль по умолчанию — `admin` и `password`. Обновите их на актуальные учетные данные.
- **Локальный хост и порт**: Установите ваш локальный IP и порт для обратного shell.

## ВАЖНО
Этот инструмент предназначен только для законного и этичного использования. Ответственность за обеспечение наличия разрешения на тестирование устройств, на которых используется этот скрипт, лежит на пользователе. Несанкционированный доступ к устройствам и сетям является незаконным и преследуется по закону.
