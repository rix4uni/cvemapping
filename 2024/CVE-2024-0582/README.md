
# RU
**GenIoURingExploit** is a PoC exploit targeting a specific vulnerability in the Linux kernel (CVE-2024-0582). The PoC leverages the `io_uring` mechanism to gain unintended access and potentially escalate privileges by manipulating socket buffers and triggering certain kernel behaviors.


## Features

- Utilizes `io_uring` for efficient buffer manipulation.
- Demonstrates the KASLR (Kernel Address Space Layout Randomization) leak.
- Exploits a vulnerability related to socket buffer management.
- Triggers the exploit using controlled IOCTL calls.
- Provides a pathway to execute arbitrary shell commands through kernel manipulation.


## Prerequisites

- A Linux-based system (tested on recent distributions).
- Root or administrative privileges for accessing the required resources.
- Development tools (e.g., `gcc`, `make`) for compiling the C code.
- The `liburing` library installed on your system.


## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/geniuszly/CVE-2024-0582
    cd CVE-2024-0582
    ```

2. **Compile the exploit:**

    Ensure you have the necessary build tools and `liburing` installed:

    ```bash
    gcc -o CVE-2024-0582 GenIoURingExploit.c -luring
    ```

3. **Run the exploit:**

    **Warning**: This PoC is for educational purposes only. Running this on a production system may cause unpredictable behavior and should only be done in a controlled environment.

    ```bash
    sudo ./CVE-2024-0582
    ```


## How It Works

The exploit works by:
1. Setting up `io_uring` buffer rings to interact with kernel socket buffers.
2. Searching for a specific marker in the memory to identify vulnerable socket structures.
3. Manipulating these structures to gain access to sensitive kernel memory.
4. Overwriting certain kernel function pointers to trigger the execution of arbitrary commands (`/bin/sh`).

## Disclaimer

This project is intended for educational purposes only. The authors are not responsible for any misuse of this code. The use of this PoC should be limited to testing within controlled, ethical hacking environments.


# RU
**GenIoURingExploit** — это PoC эксплойт, нацеленный на конкретную уязвимость в ядре Linux (CVE-2024-0582). Данный PoC использует механизм `io_uring` для несанкционированного доступа и потенциального повышения привилегий путем манипулирования буферами сокетов и вызова определенных функций ядра.

## Особенности

- Использует `io_uring` для эффективной работы с буферами.
- Демонстрирует утечку KASLR (Kernel Address Space Layout Randomization).
- Эксплуатирует уязвимость, связанную с управлением буфером сокетов.
- Запускает эксплойт с помощью управляемых вызовов IOCTL.
- Предоставляет возможность выполнения произвольных команд через манипуляции в ядре.

## Предварительные требования

- Система на базе Linux (проверено на последних дистрибутивах).
- Права root или администратора для доступа к необходимым ресурсам.
- Инструменты разработки (`gcc`, `make`) для компиляции кода на C.
- Установленная библиотека `liburing`.


## Установка

1. **Клонирование репозитория:**

    ```bash
    git clone https://github.com/geniuszly/CVE-2024-0582
    cd CVE-2024-0582
    ```

2. **Компиляция эксплойта:**

    Убедитесь, что у вас установлены необходимые инструменты сборки и библиотека `liburing`:

    ```bash
    gcc -o CVE-2024-0582 GenIoURingExploit.c -luring
    ```

3. **Запуск эксплойта:**

    **Внимание**: Этот PoC предназначен только для образовательных целей. Запуск на рабочей системе может привести к непредсказуемому поведению и должен выполняться только в контролируемой среде.

    ```bash
    sudo ./CVE-2024-0582
    ```


## Как это работает

Эксплойт работает следующим образом:
1. Настраивает буферные кольца `io_uring` для взаимодействия с буферами сокетов ядра.
2. Ищет определенный маркер в памяти для выявления уязвимых структур сокетов.
3. Манипулирует этими структурами для получения доступа к чувствительной памяти ядра.
4. Перезаписывает определенные указатели функций ядра для выполнения произвольных команд (`/bin/sh`).

---

## Отказ от ответственности

Этот проект предназначен только для образовательных целей. Авторы не несут ответственности за любое неправомерное использование этого кода. Использование данного PoC должно быть ограничено тестированием в контролируемых, этических условиях.
