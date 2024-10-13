# cve-2019-12735
Docker image that lets me study the exploitation of the VIM exploit [here](https://www.exploit-db.com/exploits/46973)

# Affected Software
- Vim 8.1.1365 (up to and excluding)
- NeoVim 0.3.6 (up to and excluding)

# Install
```bash
# on Host
$ make build
$ make run
$ make attach   # This brings you into the container with the vulnerable Vim

# In docker container
$ vim exploit/poc.txt
```

# Fix
The commit that [fixes it](https://github.com/vim/vim/commit/53575521406739cf20bbe4e384d88e7dca11f040).
![image](https://user-images.githubusercontent.com/12999836/119934249-1446bd00-bfb8-11eb-9037-36e2477adaa0.png)



# Credits
Environment setup inspired by LiveOverflow's [pwnedit](https://github.com/LiveOverflow/pwnedit)
