# -*- coding: utf-8 -*-

import os
import json
import zipfile
import urllib
import base64
from urllib2 import urlopen, Request
from StringIO import StringIO


def bb_create_repo(user, password, repo_name=None):
    if (repo_name is None):
        print('enter repo name')
        return 0
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
    print "downloading " + url
    file_path = os.path.basename(url)
    with open(file_path, "wb") as local_file:
        local_file.write(f.read())
    with zipfile.ZipFile(file_path) as zf:
        zf.extractall(os.getcwd())
    os.remove(file_path)
