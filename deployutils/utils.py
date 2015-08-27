# -*- coding: utf-8 -*-

import os
import json
import zipfile
import urllib
import base64
from urllib2 import urlopen, Request
import config


def config_test():
    try:
        config.BB_USER
    except Exception as e:
        print("BB_USER is not defined in config")
        return 0

    try:
        config.PROD_SSH_URI
    except Exception as e:
        print("PROD_SSH_URI is not defined in config")
        return 0

    try:
        config.REPO_NAME
    except Exception as e:
        print("REPO_NAME is not defined in config")
        return 0

    try:
        config.PROD_SSH_PRIVATE_KEY
    except Exception as e:
        print("PROD_SSH_PRIVATE_KEY is not defined in config")
        return 0

    try:
        config.PROD_SSH_USER
    except Exception as e:
        print("PROD_SSH_USER is not defined in config")
        return 0

    try:
        config.PROD_PROJECT_ROOT
    except Exception as e:
        print("PROD_PROJECT_ROOT is not defined in config")
        return 0

def bb_create_repo(user, password, repo_name=None):
    if (repo_name is None):
        print('enter repo name')
        return
    url = 'https://api.bitbucket.org/2.0/repositories/{}/{}'.format(user,
                                                                    repo_name)
    values = {'scm': 'git', 'is_private': 'true', 'language': 'php'}
    data = urllib.urlencode(values)
    req = Request(url, data)
    base64string = base64.encodestring('%s:%s' %
                                       (user, password)).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string)
    response = urlopen(req)
    result = response.read()
    return result


def get_latest_joomla_zip_url():
    url = 'https://api.github.com/repos/joomla/joomla-cms/releases/latest'
    response = urlopen(url)
    data = json.load(response)
    return data['assets'][2]['browser_download_url']


def get_joomla(url):
    f = urlopen(url)
    print("downloading {} ...".format(url))
    file_path = os.path.basename(url)
    with open(file_path, "wb") as local_file:
        local_file.write(f.read())
    with zipfile.ZipFile(file_path) as zf:
        zf.extractall(os.getcwd())
    os.remove(file_path)
