# Welcome to ds-cve-plugin
A plugin for DataSurgeon that Extracts CVE Numbers From Text (e.g: CVE-2021-56789)

## Jump Right In To Managing Plugins
- [Adding a new Plugin](#adding-a-new-plugin)
- [Removing a Plugin](#removing-a-plugin)
- [Listing All Plugins](#listing-all-plugins)

## Jump Right In To Creating
- [Find Your Plugin File](#find-your-plugin-file)
- [Creating Your Own Plugin](#creating-your-own-plugin)
- [How to Use Your New Plugin](#how-to-use-your-new-plugin)

## Creating Plugins
### Find Your Plugin File
If you're a Windows user, you'll find the plugin file in the  `C:\ds\` directory. If you're on Linux, look for the plugin file here: `~/.DataSurgeon/plugins.json`. And if by chance the plugin file isn't found in either of these directories, we'll automatically check the current working directory.

### Creating Your Own Plugin
Every field in the json object is important. To ensure your plugin works seamlessly with the DataSurgeon options `--add` and `--remove`, remember to upload your `plugins.json` file to a GitHub repository. Please make sure the filename remains as `plugins.json` and only include the plugin options you wish to upload. Here's a quick guide to the fields:

| Field          | Description                                                                                           |
|----------------|-------------------------------------------------------------------------------------------------------|
| content_type   | This should be a one-word description of the content you're searching for (no spaces). This is the word that gets printed alongside the matched content.                            |
| arg_long_name  | This is the unique argument name for the command-line interface. It must be unique across all plugins.             |
| help_message   | This is a short and sweet description of what your plugin does. It'll appear in the help message of the tool. |
| version        | This is the version number of your plugin (e.g: 1.0.0) |
| regex          | This is the regular expression that's used to match the content. To ensure compatibility with the `--clean` option, your regex should be designed such that the entire match `($0)` contains the exact content you're interested in. This allows the `--clean` option to extract only the relevant matched content. For testing your regex patterns, we recommend using https://regexr.com/|
| source_url | This is the URL to the GitHub repository hosting your plugin | 

Here's an example:

```json
[
    {
        "content_type": "windows_registry",
        "arg_long_name": "winregistry",
        "version": "1.0.0",
        "help_message": "Extracts windows registry paths",
        "regex": "^(HKEY_(?:LOCAL_MACHINE|CURRENT_USER|CLASSES_ROOT|CURRENT_CONFIG|USERS)\\\\[\\w\\-\\.\\\\]*)",
        "source_url": "https://github.com/DataSurgeon-ds/ds-cve-plugin/"
    }
]
```
### How to Use Your New Plugin
Once your plugin file is loaded, the option will be added as an additional argument. As you can see the name of the argument is the ```arg_long_name```. 
```
drew@DESKTOP-A5AO3TO$ ds -h

Options:
   ......
  -a, --aws                    Extract AWS keys
      --cve                    Extracts CVE Identifiers
  -V, --version                Print version
```
And here's how you can run it:
```
┌──(drew㉿IT-DREW)-[~]
└─$ ds --cve -f cves.txt
cve: The first one is CVE-2023-1234. This is a hypothetical vulnerability that was supposedly discovered in 2023.
cve: Here's another one: CVE-2021-56789. This one was supposedly discovered in 2021.
cve: And here's a third one: CVE-2020-1234567. This one was supposedly discovered in 2020.
cve: But not all strings that look like CVE identifiers are actual CVE identifiers. For example, CVE-23-1234 is not a valid identifier because the year part only has two digits. Similarly, CVE-2023-123 is not valid because the identifier part only has three digits. And CVE-2023-12345678 is not valid because the identifier part has eight digits, which is too many.
cve: Finally, note that not all CVE identifiers are associated with actual vulnerabilities. For example, CVE-2023-9999 might not be associated with any known vulnerability. To check if a CVE identifier is real, you would need to look it up in a CVE database.

┌──(drew㉿IT-DREW)-[~]
└─$ ds --cve -f cves.txt --clean
cve: CVE-2023-1234
cve: CVE-2021-56789
cve: CVE-2020-1234567
cve: CVE-2023-1234567
cve: CVE-2023-9999
```

## Managing Plugins
### Adding a New Plugin
To add a new plugin you need to use the ```--add <URL>``` option. The URL needs to be a remote github repository hosting a ```plugins.json``` file. [How to use your new plugin](https://github.com/DataSurgeon-ds/ds-cve-plugin/blob/main/README.md#how-to-use-your-new-plugin).
```
drew@DESKTOP-A5AO3TO:~$ ds --add https://github.com/DataSurgeon-ds/ds-cve-plugin/
[*] Download and added plugin: https://github.com/DataSurgeon-ds/ds-cve-plugin/
```
### Listing All Plugins
To list all plugins you can use the ```--list``` option.
```
drew@DESKTOP-A5AO3TO$ ds --list

Plugin File: /home/drew/.DataSurgeon/plugins.json

Source URL                                                     | Argument Long Name
https://raw.githubusercontent.com/DataSurgeon-ds/ds-cve-plugin | cve
```
### Removing a Plugin
To remove a plugin you don't want anymore you can use the ```--remove``` option.
```
drew@DESKTOP-A5AO3TO:~$ ds --remove https://github.com/DataSurgeon-ds/ds-cve-plugin//
[*] Removed plugin: https://github.com/DataSurgeon-ds/ds-cve-plugin//
```
