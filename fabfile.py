# -*- coding: utf-8 -*-

from fabric.api import local, prompt, settings, env, roles, cd, run
from fabric.contrib.console import confirm
from fabric.contrib import files
import getpass
from os import path, getcwd
import shutil

import deployutils.utils as utils
import deployutils.config as config

env.roledefs['production'] = [config.PROD_SSH_URI]


def commit():
    with settings(warn_only=True):
        local('git status')
        prompt('Press <Enter> to continue or <Ctrl+C> to cancel.')
        local('git add --all')
        local('git commit')
        local('git push origin master')


def init_project():
    joomla_url = utils.get_latest_joomla_zip_url()
    utils.get_joomla(joomla_url)
    bb_pass = getpass.getpass(prompt='Enter bitbucket pass: ')
    utils.bb_create_repo(config.BB_USER, bb_pass, config.REPO_NAME)
    local('git init')
    local(
        'git remote add origin git@bitbucket.org:{}/{}.git'.format(
            config.BB_USER, config.REPO_NAME))
    gitignore_tmpl = path.join(getcwd(), 'deployutils', 'gitignore.template')
    shutil.copyfile(gitignore_tmpl, path.join(getcwd(), '.gitignore'))
    commit()


def _production_env():
    env.key_filename = config.PROD_SSH_PRIVATE_KEY
    env.user = config.PROD_SSH_USER
    env.project_root = config.PROD_PROJECT_ROOT
    env.shell = '/bin/bash -c'
    env.python = '/usr/bin/python'


@roles('production')
def prod_push():
    _production_env()
    with cd(env.project_root):
        if files.exists(path.join(env.project_root, '.git'),
                        use_sudo=False,
                        verbose=False):
            run('git status')
            prompt('Press <Enter> to continue or <Ctrl+C> to cancel.')
            run('git add --all')
            run('git commit -m "push from prod"')
            run('git push origin master')


@roles('production')
def deploy():
    commit()
    _production_env()
    with cd(env.project_root):
        if files.exists(path.join(env.project_root, '.git'),
                        use_sudo=False,
                        verbose=False):
            run('git pull origin master')
        else:
            repo = 'https://{0}@bitbucket.org/{0}/{1}.git'.format(
                config.BB_USER, config.REPO_NAME)
            print('Project not init on prod server')
            if (confirm('Clone repo {}? '.format(repo))):
                run('git clone {} {}'.format(repo, env.project_root))
