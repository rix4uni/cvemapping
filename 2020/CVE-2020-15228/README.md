# Fix CVE-2020-15228 (set-env, add-path in Github-Actions)

This script changes lines in your github action file.

You give it a directory name, and it searches for all files with the ".sh" or ".yml" extension.

It recognizes these lines:

```
echo ::set-env name=FOO_BAR::$FOO_BAR
echo ::set-env name=FOO_BAR::${FOO_BAR}
echo "::set-env name=FOO_BAR::$FOO_BAR"
echo "::set-env name=FOO_BAR::${FOO_BAR}"
```

All lines get rewrites to 
```
echo "FOO_BAR=$FOO_BAR" >> $GITHUB_ENV
```

And
```
run: echo ::set-env name=FOO_BAR::"${GITHUB_SHA::8},dev-${GITHUB_SHA::8}"
```
becomes
```
run: echo "FOO_BAR=${GITHUB_SHA::8},dev-${GITHUB_SHA::8}" >> $GITHUB_ENV
```
# Run

You can apply this script directly like this. All ".sh" and ".yml" files in "your_repo/.github/workflows" get updated.

```
curl -sSL https://raw.githubusercontent.com/guettli/fix-CVE-2020-15228/main/fix_CVE_2020_15228.py | python3 - your_repo/.github/workflows
```

Please give this project a "star" if it was useful to you.

# TODO: add-path

I don't have any working example of `add-path`. Up to now this does not get updated. 

If you tell me the desired transformation, then I can add it. Thank you.
