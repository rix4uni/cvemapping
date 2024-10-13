import os
import re
import argparse

input_1 = '''
line1
          echo ::set-env name=FOO_BAR::$FOO_BAR
          echo ::set-env name=FOO_BAR::${FOO_BAR}
          echo "::set-env name=FOO_BAR::${FOO_BAR}"
          echo "::set-env name=FOO_BAR::$FOO_BAR"
line3
'''

should_1 = '''
line1
          echo "FOO_BAR=$FOO_BAR" >> $GITHUB_ENV
          echo "FOO_BAR=${FOO_BAR}" >> $GITHUB_ENV
          echo "FOO_BAR=${FOO_BAR}" >> $GITHUB_ENV
          echo "FOO_BAR=$FOO_BAR" >> $GITHUB_ENV
line3
'''

input_2 = 'run: echo ::set-env name=FOO_BAR::"${GITHUB_SHA::8},dev-${GITHUB_SHA::8}"'
should_2 = 'run: echo "FOO_BAR=${GITHUB_SHA::8},dev-${GITHUB_SHA::8}" >> $GITHUB_ENV'

input_3 = 'echo ::set-env name=FOO_TOKEN::"${{ secrets.FOO_STAGE_TOKEN }}"'
should_3 = 'echo "FOO_TOKEN=${{ secrets.FOO_STAGE_TOKEN }}" >> $GITHUB_ENV'

def do_file(filename):
    extension = os.path.splitext(filename)[1]
    if not extension in ['.sh', '.yml']:
        return
    old = open(filename, 'rt').read()
    new = fix_set_env(old)
    if new == old:
        return
    with open(filename, 'wt') as fd:
        fd.write(new)
    print('Updated %s' % filename)


def fix_set_env(input):
    def updater(match):
        match1, match2 = match.groups()
        var_name = match1.strip('"')
        var_value = match2.strip('"')
        #if match1 != name:
        #    print(f'### unsure, {match1} != {name}')
        #    return match.group(0)
        ret = '"%s=%s" >> $GITHUB_ENV' % (var_name, var_value)
        print('### Update: %s --> %s' % (match.group(0), ret))
        return ret

    return re.sub(r'"?::set-env\s+name="?(\S+?)::"?(.+)', updater, input)


def test():
    result = fix_set_env(input_3)
    assert result == should_3, result

    result = fix_set_env(input_2)
    assert result == should_2, result

    result = fix_set_env(input_1)
    assert result == should_1, result

    print('OK')


def do_dir_or_file(arg):
    if os.path.isfile(arg):
        do_file(arg)
        return
    if not os.path.isdir(arg):
        return
    for root, dirs, files in os.walk(arg):
        dirs.sort()
        for file in files:
            file = os.path.join(root, file)
            do_dir_or_file(file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    for arg in args.files:
        if not os.path.exists(arg):
            print('%s does not exist' % arg)
            continue
        do_dir_or_file(arg)


if __name__ == '__main__':
    main()