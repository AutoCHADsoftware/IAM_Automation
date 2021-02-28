
class WindowsTicket:
    def __init__(self, command):
        self.command = command

    def RemoveUser_Windows(self):
        try:
            wu = win_user
            print(self.command)
            print(wu.EXAMPLES)

            # userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            # print(userhost)
            # myinput = str("echo -e '" + self.mypw + "' | sudo -S /usr/sbin/userdel -r " + self.userid +
            #               " && echo Successfully Executed\n").encode('utf-8')
            # result = run(['ssh',  userhost, '/bin/bash'], stdout=PIPE, input=myinput)
            # self.stdout = result.stdout.decode('utf-8')
            # print(self.stdout)
            # return self.stdout
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass
