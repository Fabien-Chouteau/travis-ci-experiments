#!/usr/bin/env python3

import os

list = ['TRAVIS_PULL_REQUEST_SLUG',
        'TRAVIS_REPO_SLUG',
        'TRAVIS_BRANCH',
        'TRAVIS_COMMIT',
        'TRAVIS_EVENT_TYPE']

for elt in list:
    if elt in os.environ:
        print("%s -> '%s'" % (elt, os.environ[elt]))
    else:
        print("%s not defined" % elt)
