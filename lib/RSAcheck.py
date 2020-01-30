from lib.UATMain import *
from ansible.plugins.inventory import BaseInventoryPlugin

p1 = MainStart(controller='', parent='')
p1.ParsedCsv(filepath='')


class RSAcheck:
    def __init__(self, myuser, mypw, ipaddress, userid, userpw, command, uid, usergroup, stdout):
        self.myuser = myuser
        self.mypw = mypw
        self.ipaddress = ipaddress
        self.userid = userid
        self.userpw = userpw
        self.command = command
        self.uid = uid
        self.usergroup = usergroup
        self.stdout = stdout


    def RSA(self):
        prompt = input("Check RSA Keys?").lower()
        if prompt == 'y':
            userhost = self.myuser + str(self.ipaddress)
            print(userhost)
            for user in userhost:
                print(user)
                result2 = run(['ssh-keyscan', '-H', user, '>> ~/.ssh/known_hosts'], stdout=PIPE)
                print(result2)
                output2 = result2.stdout.decode('utf-8')
                print(user + " had this result " + output2)
            quit()
        elif prompt == 'n':
            print("Quitting without checking RSAs")
            quit()
        else:
            print("Please enter a 'y' or 'n'")
            self.RSA()



class InventoryModule(BaseInventoryPlugin):
    NAME = p1.ParsedCsv(filepath='')[0]
