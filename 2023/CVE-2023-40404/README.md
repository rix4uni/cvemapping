
# EN
`GenEtherExploit` is a Proof-of-Concept (PoC) exploit for the macOS vulnerability `CVE-2023-40404`. This PoC leverages IOKit APIs to interact with the `IOUserEthernetResource` network service, manipulating the system's network interfaces. The purpose of this exploit is to demonstrate a potential kernel panic in vulnerable macOS systems by creating and interacting with Ethernet controllers.

## Disclaimer
This code is for educational and research purposes only. The author is not responsible for any misuse or damage caused by the usage of this code. Please ensure you have proper authorization before testing on any system.

## Features
- Interacts with macOS `IOKit` services.
- Creates a new Ethernet controller and interacts with network interfaces.
- Demonstrates exploitation of a vulnerability in the macOS network stack.

## Requirements
- macOS system vulnerable to CVE-2023-40404.
- Xcode or `clang` installed for compilation.
- Root access for running the exploit.

## Compilation & Usage
### Compilation
Use the following command to compile the exploit:

```bash
clang GenEtherExploit.m -o GenEtherExploit -framework IOKit -framework Foundation
```

### Running the Exploit
You need to run the compiled binary as a superuser:

```bash
sudo ./GenEtherExploit
```

## How It Works
1. **Connects to the Ethernet Service**: Uses `IOServiceGetMatchingService` to locate the `IOUserEthernetResource` service.
2. **Creates Controller Parameters**: Sets up the minimum and maximum packet size, hardware address (MAC), and name prefix for the Ethernet controller.
3. **Creates the Ethernet Controller**: Serializes the parameters and calls the method to create a new controller.
4. **Obtains Network Interface**: Finds and connects to the `IOUserEthernetInterface` service.
5. **Collects Network Stats**: Gathers network statistics through IOKit calls to demonstrate the exploitation potential.
6. **Cleans Up Connections**: Closes all opened connections and services.

## Output Example
```less
[Информация] Подключение к сервису Ethernet выполнено, user_client_port: 56
[Информация] Контроллер создан успешно, статус: 0x0
[Информация] Интерфейс Ethernet подключен, network_client: 72
[Информация] Сетевая статистика собрана, статус: 0x0, данные: 123456
[Завершено] Операции завершены, проверьте состояние системы.

```

# RU
`GenEtherExploit` — это Proof-of-Concept (PoC) эксплойт для уязвимости macOS `CVE-2023-40404`. Этот PoC использует API IOKit для взаимодействия с сетевым сервисом `IOUserEthernetResource` и манипуляции сетевыми интерфейсами системы. Цель этого эксплойта — продемонстрировать возможность паники ядра в уязвимых системах macOS путем создания и взаимодействия с Ethernet-контроллерами.

## Дисклеймер
Этот код предназначен только для образовательных и исследовательских целей. Автор не несет ответственности за любое неправильное использование или ущерб, причиненный использованием данного кода. Пожалуйста, убедитесь, что у вас есть соответствующие права для тестирования на любой системе.


## Возможности
- Взаимодействие с сервисами `IOKit` в macOS.
- Создание нового контроллера Ethernet и взаимодействие с сетевыми интерфейсами.
- Демонстрация эксплуатации уязвимости в сетевом стеке macOS.

## Требования
- Система macOS, уязвимая для CVE-2023-40404.
- Установленный Xcode или `clang` для компиляции.
- Права root для запуска эксплойта.

## Компиляция и использование
### Компиляция
Используйте следующую команду для компиляции эксплойта:

```bash
clang GenEtherExploit.m -o GenEtherExploit -framework IOKit -framework Foundation
```

### Запуск эксплойта
Вам необходимо запустить скомпилированный бинарный файл от имени суперпользователя:

```bash
sudo ./GenEtherExploit
```

## Как это работает
1. **Подключение к сервису Ethernet**: Использует `IOServiceGetMatchingService` для поиска сервиса `IOUserEthernetResource`.
2. **Создание параметров контроллера**: Настраивает минимальный и максимальный размер пакета, аппаратный адрес (MAC) и префикс имени для Ethernet-контроллера.
3. **Создание контроллера Ethernet**: Сериализует параметры и вызывает метод для создания нового контроллера.
4. **Получение сетевого интерфейса**: Находит и подключается к сервису `IOUserEthernetInterface`.
5. **Сбор статистики сети**: С помощью вызовов IOKit собирает статистику сети для демонстрации потенциала эксплуатации.
6. **Закрытие соединений**: Закрывает все открытые соединения и сервисы.

## Пример вывода
```less
[Информация] Подключение к сервису Ethernet выполнено, user_client_port: 56
[Информация] Контроллер создан успешно, статус: 0x0
[Информация] Интерфейс Ethernet подключен, network_client: 72
[Информация] Сетевая статистика собрана, статус: 0x0, данные: 123456
[Завершено] Операции завершены, проверьте состояние системы.

```
