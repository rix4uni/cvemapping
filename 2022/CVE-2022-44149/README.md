# CVE-2022-44149
This tool helps identify the CVE-2022-44149 vulnerability in routers, allowing researchers and security professionals to test their systems. It includes authentication header generation, payload delivery, and detailed logging for analysis.

# EN
This tool is designed to test the vulnerability CVE-2022-44149 in routers, which may allow unauthorized users to execute arbitrary commands via the router's web interface. The tool aims to assist security professionals and researchers in identifying and mitigating this security issue in their networks.

## Features
- **Authentication Header Generation**: Uses basic authentication with Base64 encoding.
- **Payload Delivery**: Sends payloads to the router's web interface for testing.
- **Logging and Error Handling**: Detailed logging and error handling to facilitate debugging and analysis.

## Requirements
- Python 3.x
- `requests` library (`pip install requests`)

## Usage
1. **Setup Environment Variables**: Before running the script, set the necessary environment variables to ensure secure operation:
```bash
export ROUTER_URL="http://192.168.1.1"
export ROUTER_USERNAME="admin"
export ROUTER_PASSWORD="admin"
```
2. **Running the Script**: Execute the script to start testing:
```bash
python GenVuln_CVE2022_44149.py
```
3. **Output**: The script will log the process and output the results, indicating if the payload was successfully delivered.

## Security Notice
**Disclaimer**: This tool is intended for use in testing environments and should not be used against devices or networks without explicit permission. Unauthorized use of this tool can be illegal and unethical.

# RU
Этот инструмент предназначен для тестирования уязвимости CVE-2022-44149 в маршрутизаторах, которая может позволить неавторизованным пользователям выполнять произвольные команды через веб-интерфейс маршрутизатора. Инструмент помогает специалистам по безопасности и исследователям выявлять и устранять эту проблему в своих сетях.

## Особенности
- **Генерация заголовка аутентификации**: Использует базовую аутентификацию с кодированием Base64.
- **Отправка полезной нагрузки**: Отправляет полезные нагрузки на веб-интерфейс маршрутизатора для тестирования.
- **Логирование и обработка ошибок**: Подробное логирование и обработка ошибок для облегчения отладки и анализа.

## Требования
- Python 3.x
- Библиотека `requests` (`pip install requests`)

## Использование
**Настройка переменных окружения**: Перед запуском скрипта установите необходимые переменные окружения для обеспечения безопасной работы:
```bash
export ROUTER_URL="http://192.168.1.1"
export ROUTER_USERNAME="admin"
export ROUTER_PASSWORD="admin"
```
2. **Запуск скрипта**: Выполните скрипт для начала тестирования:
```bash
python GenVuln_CVE2022_44149.py
```
3. **Результаты**: Скрипт будет логировать процесс и выводить результаты, указывая, была ли полезная нагрузка успешно отправлена.

## Уведомление о безопасности
**Отказ от ответственности**: Этот инструмент предназначен для использования в тестовых средах и не должен использоваться против устройств или сетей без явного разрешения. Несанкционированное использование этого инструмента может быть незаконным и неэтичным.
