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
import json
import base64
from rtmbot.core import Plugin

from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                     value_serializer=lambda v: json.dumps(v).encode('utf-8'))



class BitbucketPlugin(Plugin):
    """Plugin to act as a git command line interface"""

    def adduser(self, data, namespace):
        if namespace.user and namespace.email and namespace.desc:
            dict={'user':namespace.user,'email':namespace.email,'description':namespace.desc}

            print(dict)
            for key,value in dict.items():

                encoded_key = key.encode('UTF-8', 'strict')
                encoded_value=value.encode('UTF-8','strict')
                print(encoded_key)
                print(encoded_value)
                producer.send('add_user_topic', key=encoded_key,value=encoded_value)
            return True
        else:
            print('in adduser else condition')
            msg = '[user & email & desc] options are necessary for this command'
            msg += '\r\n Usage:git <command> [options]'
            self.outputs.append([data['channel'], msg])
            return False

    def addrepo(self, data, namespace):
        if namespace.project and namespace.repo:
            dict = {'project': namespace.project, 'repo': namespace.repo, }

            for key, value in dict.items():
                encoded_key = key.encode('UTF-8', 'strict')
                encoded_value = value.encode('UTF-8', 'strict')
                print(encoded_key)
                print(encoded_value)
                producer.send('add_user_topic', key=encoded_key, value=encoded_value)
            return True
        else:
            msg = '[project & repo] options are necessary for this command'
            msg += '\r\n Usage:git <command> [options]'
            self.outputs.append([data['channel'], msg])
            return False

    def addproject(self, data, namespace):
        if namespace.project:

            dict = {'project': namespace.project}

            for key, value in dict.items():
                encoded_key = key.encode('UTF-8', 'strict')
                encoded_value = value.encode('UTF-8', 'strict')
                print(encoded_key)
                print(encoded_value)
                producer.send('add_user_topic', key=encoded_key, value=encoded_value)
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
                dict = {'user': namespace.user, 'permission': namespace.permission, 'repo': namespace.repo,
                        'project': namespace.project}
                for key, value in dict.items():
                    encoded_key = key.encode('UTF-8', 'strict')
                    encoded_value = value.encode('UTF-8', 'strict')
                    print(encoded_key)
                    print(encoded_value)
                    producer.send('add_user_topic', key=encoded_key, value=encoded_value)

                return True
            elif namespace.project:
                # project level permission
                dict = {'user': namespace.user, 'permission': namespace.permission, 'project': namespace.project}

                for key, value in dict.items():
                    encoded_key = key.encode('UTF-8', 'strict')
                    encoded_value = value.encode('UTF-8', 'strict')
                    print(encoded_key)
                    print(encoded_value)
                    producer.send('add_user_topic', key=encoded_key, value=encoded_value)

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
        if command not in ['adduser', 'addrepo', 'addproject', 'addpermission','help']:
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
