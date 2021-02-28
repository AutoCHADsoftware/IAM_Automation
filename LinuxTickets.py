
class LinuxTicket:
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

    def NewUser_Linux(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            username = ''
            print(userhost)

            myinput1 = str("grep " + self.userid + " /etc/passwd ").encode('utf-8')
            result1 = run(['ssh', userhost, '/bin/bash'], stdout=PIPE, input=myinput1)
            self.stdout = result1.stdout.decode('utf-8')
            print("self.stdout: {}".format(self.stdout))

            try:
                colon = self.stdout.index(':')
                username = self.stdout[0:colon]
                print("Username: {}".format(username))
                print("self.user: {}".format(self.userid))
            except ValueError as e:
                print("Value Error: {}".format(e))
                print("Username: {}".format(username))
                print("self.user: {}".format(self.userid))
                pass

            if self.userid not in username:
                myinput2 = str(
                    "echo -e '" + self.mypw + "\n' | sudo -S /usr/sbin/useradd -g users -u " + self.uid + " -c '" +
                    self.command + "' " + self.userid + "; sudo -S chage -d0 " + self.userid +
                    " ;groups " + self.userid + " ;echo -e '" + self.userpw + "\n" + self.userpw +
                    "\n' | sudo -S passwd " + self.userid + ";").encode('utf-8')
                result2 = run(['ssh', userhost, '/bin/bash'], stdout=PIPE, input=myinput2)
                self.stdout = result2.stdout.decode('utf-8')
                print("Output 2: " + self.stdout)
                return self.stdout
            else:
                print("User " + self.userid + " already exists.")

        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def ChangeMyPassword_Linux(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput = str("echo -e '" + self.mypw + "\n" + self.mypw + "\n' | sudo -S passwd " + self.myuser +
                          " && echo Successfully Executed\n").encode('utf-8')
            result = run(['ssh', userhost], stdout=PIPE, input=myinput)
            self.stdout = result.stdout.decode('utf-8')
            print(self.stdout)
            return self.stdout

        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def ChangeUserPassword_Linux(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput1 = str("echo '***************' | sudo passwd --stdin laytonc && sudo /usr/bin/chage -d 0 laytonc && echo Successfully Executed").encode('utf-8')
            result1 = run(['ssh', userhost, '/bin/bash'], stdout=PIPE, input=myinput1)
            self.stdout = result1.stdout.decode('utf-8')
            print("Output 1: " + self.stdout)
            return self.stdout
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def ChangeGroups_Linux(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput1 = str(
                    "echo -e '" + self.mypw + "\n' | sudo -S /usr/sbin/usermod -a " + self.userid +
                    " -G " + self.usergroup + " && groups " + self.userid + " && echo Successfully Executed").encode('utf-8')
            result1 = run(['ssh', userhost, '/bin/bash'], stdout=PIPE, input=myinput1)
            self.stdout = result1.stdout.decode('utf-8')
            print("Output 1: " + self.stdout)
            return self.stdout
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def CreatePrivOnDevice_Linux(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput1 = str(
                    "echo -e '" + self.mypw + "\n' | sudo -S /usr/sbin/groupadd " + self.usergroup +
                    " && echo Successfully Executed").encode('utf-8')
            result1 = run(['ssh', userhost, '/bin/bash'], stdout=PIPE, input=myinput1)
            self.stdout = result1.stdout.decode('utf-8')
            print("Output 1: " + self.stdout)
            return self.stdout
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def RemoveUser_Linux(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput = str("echo -e '" + self.mypw + "' | sudo -S /usr/sbin/userdel -r " + self.userid +
                          " && echo Successfully Executed\n").encode('utf-8')
            result = run(['ssh',  userhost, '/bin/bash'], stdout=PIPE, input=myinput)
            self.stdout = result.stdout.decode('utf-8')
            print(self.stdout)
            return self.stdout

        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

