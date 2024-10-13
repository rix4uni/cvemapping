# CVE-2019-14745
weaponized radare2 vulnerability (CVE-2019-14745 assigned) found by @CaptnBanana and blenk92

For details about vulnerability, read https://bananamafia.dev/post/r2-pwndebian/

# Usage
First of all, you need Python bindings of LIEF (https://lief.quarkslab.com/)
Then, run script as:

`python nukeradare2.py <binary_name> <one of the symbols of that binary> <shell command>`

This will create a binary with nuked_ as prefix. Run it with:

`radare2 -c "ood" <nuked_binary>`

or give "ood" as a command in radare2. Note that radare2 will run your command twice.
