# GLPwn
 A GLPI hack tool, using Apache directory listing and / or CVE-2020-15175 to dump files and valid sessions.

### Who is vulnerable?
- Any GLPI instance that has Apache directory listing already enabled on the `/files` folder
- All GLPI instances prior to 9.5.1 running on a default Apache2 server.

### What can it do?
GLPwn is able to dump all files inside the GLPI `/files` folder, which includes adminitrator sessions, logs, database dumps, and ticket attachments.

GLPwn is also able to automaticaly detect which session is valid, has the most rights on the platform, and the sessions user's name.

## Disclaimer
**This tool leverages a vulnerability inside GLPI that permanently erases a critical configuration file. Once exploited, the private data inside GLPI will be exposed publicly.**

**This tool shall not be used outside of educationnal purposes and/or penetration tests.**

**Just like with sex, please use with consent of both parties.**

## Installation
### Pre-requisites
- Python 3.9 or later

First clone the repository from the `master` branch, or download one of the releases from the repository.

Use `pip install -r requirements.txt` to install all the required dependencies.

Use `python3 GLPwn.py -h` to run the script and get the help menu.

## Usage
The `--url` parameter is required for the script to work. 

`python3 GLPwn.py --url [GLPI_URL]`, e.g. `http://127.0.0.1/glpi`

Optionnal parameters : 

 - `--check` Performs version check to determine if the GLPI instance is vulnerable or not.
 - `--exploit` Attempts to use a CVE-2020-15175 expoit to enable directory listing on `/files`.
 - `--sessions` Attempts to retrieve valid session tokens.
 - `--dumpfiles` Attempts to dump the whole content of the `/files` folder.

## License
The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.