from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import re

class HelpPlugin(Plugin):

 def process_message(self, data):
     text=data['text'].split(' ')
     regex1=r"Hi|Hello|Hai"
     regex2=r"Good Morning|Good Evening|Good Afternoon|GM"
     compiled_re1=re.compile(regex1,flags=re.I)
     res1=compiled_re1.search(text[0])
     if res1:
        if len(text)>1:
            compiled_re2=re.compile(regex2,flags=re.I)
            greet=data['text'].strip(text[0])
            res2=compiled_re2.search(greet.lstrip(' '))

            if res2:
                    msg = data['text']
                    msg += '\r\n Type help for command info'
                    self.outputs.append([data['channel'], msg])
            else:

                    self.outputs.append([data['channel'],"Type help for command info" ])
        else:
            compiled_re2 = re.compile(regex2, flags=re.I)
            res2 = compiled_re2.search(data['text'])
            if res2:
                    msg = data['text']
                    msg += '\r\n Type help for command info'
                    self.outputs.append([data['channel'], msg])
     elif(data['text']=='help'):
         message  ='Please type the following to get more details'
         message += '\r\n ```for detailed command list type !git help ``` \n ```for detailed command list type !svn help ``` \r ```for detailed command list type !kibana help` ```'
         self.outputs.append([data['channel'], message])
     elif(data['text']=='!git help'):

         message = ' `git commands` '
         message += '\r\n ```!git adduser -u <user> -e <email> -d <description>``` '
         message += '\r\n ```!git addrepo -r <repo> -p <project>``` '
         message += '\r\n ```!git addproject -p <project>``` '
         message += '\r\n ```!git addpermission -u <user> -a <permission> -p <project> OR !git addpermission -u <user> -a <permission> -p <project> -r <repo>``` '
         self.outputs.append([data['channel'], message])

     elif (data['text'] == '!svn help'):
         message = ' `svn commands` '
         message += '\r\n```!svn adduser -u <user> -e <email> -d <description>``` '
         message += '\r\n```!svn addrepo -r <repo> -p <project>```  '
         message += '\r\n!```svn addproject -p <project>``` '
         message += '\r\n!```svn addpermission -u <user> -a <permission> -p <project>``` '
         self.outputs.append([data['channel'], message])

     elif (data['text'] == '!kibana help'):
         message = '`kibana commands`'
         message += '\r\n```!kibana adduser -u <user> -e <email> -d <description>``` '
         message += '\r\n```!kibana addrepo -r <repo> -p <project>``` '
         message += '\r\n```!kibana addproject -p <project>``` '
         message += '\r\n```!kibana addpermission -u <user> -a <permission> -p <project> ``` '
         self.outputs.append([data['channel'], message])
     '''else:
         self.outputs.append([data['channel'], "invalid command!!! try _help"])'''


