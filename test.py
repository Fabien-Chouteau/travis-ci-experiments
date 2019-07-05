#!/usr/bin/env python3

import os
import subprocess
import sys

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

if 'TRAVIS_PULL_REQUEST_SLUG' in os.environ:
    username, _ = os.environ['TRAVIS_PULL_REQUEST_SLUG'].split('/', 1)
    print("PR username: %s" % str(username))

if 'TRAVIS_COMMIT_RANGE' in os.environ:
    output = subprocess.check_output(['git', 'show', '--pretty=', '--name-only', os.environ['TRAVIS_COMMIT_RANGE']])
    file_list = output.decode(sys.stdout.encoding).split("\n")
    file_list = [i for i in file_list if i]
    file_list.sort()
    file_list = list(set(file_list))
    print("List of files: %s" % str(file_list))

    if len(file_list) < 0:
        print("No file modified in this PR???")
    elif len(file_list) > 0:
        print("More than one file modified in this PR")
