#!/usr/bin/env python

"""
!git <command> [options] is a command line interface to bitbucket

Commands:
* `adduser`: add a user
    ex: `!git adduser -u <user>`
* `addrepo`: create a repository in a project
    ex: `!git addrepo -p <project> <reponame>`
* `addproject`: create a project
    ex: `!git addproject <project>`
"""
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re

from rtmbot.core import Plugin


class BitbucketPlugin(Plugin):
    """Plugin to act as a git command line interface"""

    def adduser(self, data, namespace):
        if namespace.user and namespace.email and namespace.desc:
            return True
        else:
            print('in adduser else condition')
            msg = '[user & email & desc] options are necessary for this command'
            msg += '\r\n Usage:git <command> [options]'
            self.outputs.append([data['channel'], msg])
            return False

    def addrepo(self, data, namespace):
        if namespace.project and namespace.repo:
            return True
        else:
            msg = '[project & repo] options are necessary for this command'
            msg += '\r\n Usage:git <command> [options]'
            self.outputs.append([data['channel'], msg])
            return False

    def addproject(self, data, namespace):
        if namespace.project:
            return True
        else:
            msg = '[project] options are necessary for this command'
            msg += '\r\n Usage:git <command> [options]'
            self.outputs.append([data['channel'], msg])
            return False

    def addpermission(self, data, namespace):
        if namespace.user and namespace.permission:

            if namespace.repo and namespace.project:
                #repo level permission
                return True
            elif namespace.project:
                # project level permission
                return True
            else:
                msg = '[project | project & repo] options are necessary for this command'
                msg += '\r\n Usage:git <command> [options]'
                self.outputs.append([data['channel'], msg])
                return False
        else:
            msg = '[user & permission] options are necessary for this command'
            msg += '\r\n Usage:git <command> [options]'
            self.outputs.append([data['channel'], msg])
            return False

    def process_message(self, data):
        text = data['text']
        match = re.findall(r"!git\s*(.*)", text)
        if not match:
            return

        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--repo', required=False)
        parser.add_argument('-u', '--user', required=False)
        parser.add_argument('-p', '--project', required=False)
        parser.add_argument('-a', '--permission', required=False)
        parser.add_argument('-e', '--email', required=False)
        parser.add_argument('-d', '--desc', required=False)
        parser.add_argument('command', nargs=1)

        try:
            ns = parser.parse_args(match[0].split(' '))
        except SystemExit:
            return __doc__

        command = ns.command[0]
        if command not in ['adduser', 'addrepo', 'addproject', 'addpermission']:
            self.outputs.append([data['channel'], 'Usage:git <command> [options]'])
            return
        else:
            try:
                done = getattr(self, command)(data, ns)
                if done:
                    reply = 'Thank You!'
                    reply += '\r\nYour command is being executed.\r\n'
                    reply += '\r\nWe will let you know as soon as the execution is over'
                    self.outputs.append([data['channel'], reply])

            except AttributeError:
                raise Exception('Command [{}] interface method is not defined'.format(command))
