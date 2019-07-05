#!/usr/bin/env python3

import os
import subprocess
import sys
import toml

env_list = ['TRAVIS_PULL_REQUEST_SLUG',
            'TRAVIS_REPO_SLUG',
            'TRAVIS_BRANCH',
            'TRAVIS_COMMIT',
            'TRAVIS_COMMIT_RANGE',
            'TRAVIS_EVENT_TYPE']

for elt in env_list:
    if elt in os.environ:
        print("%s -> '%s'" % (elt, os.environ[elt]))
    else:
        print("%s not defined" % elt)

def check_username(username, toml_data):
    content = toml.loads(toml_data)
    if 'general' not in content:
        return False
    elif 'github_usernames' not in content.get("general"):
        return False
    else:
        return username in content.get("general").get('github_usernames')

def username():
    if 'TRAVIS_PULL_REQUEST_SLUG' in os.environ:
        username, _ = os.environ['TRAVIS_PULL_REQUEST_SLUG'].split('/', 1)
        return username
    else:
        return "_NO_USERNAME_"

def commit_id_or_range():
    if 'TRAVIS_COMMIT_RANGE' in os.environ \
           and len(os.environ['TRAVIS_COMMIT_RANGE']) > 0:
        return os.environ['TRAVIS_COMMIT_RANGE']
    elif 'TRAVIS_COMMIT' in os.environ:
        return os.environ['TRAVIS_COMMIT']
    else:
        return "_NO_COMMIT_ID_"

output = subprocess.check_output(['git', 'show', '--pretty=', '--name-only', commit_id_or_range()])
file_list = output.decode(sys.stdout.encoding).split("\n")
file_list = [i for i in file_list if i]
file_list.sort()
file_list = list(set(file_list))
print("List of files: %s" % str(file_list))

if len(file_list) < 0:
    print("No file modified in this PR???")
    os.sys.exit(1)
elif len(file_list) > 1:
    print("More than one file modified in this PR")
    os.sys.exit(1)
else:
    filename = file_list[0]
    first_commit = commit_id_or_range().split('...', 1)[0]

    try:
        output = subprocess.check_output(['git', 'show', "%s~:%s" % (first_commit, filename)])
        toml_data = output.decode(sys.stdout.encoding)
    except subprocess.CalledProcessError as e:
        print(e.output)
        print("This is a new file")
        with open(filename, 'r', encoding='utf-8') as fp:
            toml_data = fp.read()

    if check_username(username(), toml_data):
        print("PR author owns the file")
        os.sys.exit(0)
    else:
        print("PR author doesn't own the file")
        os.sys.exit(1)

