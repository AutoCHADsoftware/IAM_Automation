
class AIXTicket:
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

    def NewUser_AIX(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput1 = str("grep " + self.userid + " /etc/passwd").encode('utf-8')
            result1 = run(['ssh', userhost], stdout=PIPE, input=myinput1)
            self.stdout = result1.stdout.decode('utf-8')
            print(self.stdout)

            if self.stdout != '':
                colon = self.stdout.index(':')
                username = self.stdout[0:colon]
            else:
                username = self.stdout

            if self.userid not in username:
                myinput2 = str(
                    "echo -e '" + self.mypw + "\n' | sudo -S mkuser gecos='" + self.command + "' " + self.uid + " " + self.userid +
                    " && echo -e " + self.userid + ":" + self.mypw + " | sudo -S /usr/bin/chpasswd && echo Successfully Executed;").encode('utf-8')
                result2 = run(['ssh', userhost], stdout=PIPE, input=myinput2)
                self.stdout = result2.stdout.decode('utf-8')
                print(self.stdout)
            else:
                print("User " + self.userid + " already exists.")
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def ChangeMyPassword_AIX(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput = str("echo -e '" + self.mypw + "\n" + self.mypw + "\n' | sudo -S passwd " + self.userid +
                          " && echo Successfully Executed\n").encode('utf-8')
            result = run(['ssh', userhost], stdout=PIPE, input=myinput)
            self.stdout = result.stdout.decode('utf-8')
            print("Output 1: " + self.stdout)
            return self.stdout
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def ChangeUserPassword_AIX(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput1 = str("sudo /usr/bin/chuser unsuccessful_login_count=0 " + self.userid + " && echo "
                           + self.userid + ":'" + self.userpw + "' | sudo /usr/bin/chpasswd && echo Successfully Executed").encode('utf-8')
            result1 = run(['ssh', userhost], stdout=PIPE, input=myinput1)
            self.stdout = result1.stdout.decode('utf-8')
            print("Output 1: " + self.stdout)
            return self.stdout
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def UnlockUser_AIX(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput1 = str("sudo /usr/bin/chuser unsuccessful_login_count=0 " + self.userid +
                           " && echo Successfully Executed").encode('utf-8')
            result1 = run(['ssh', userhost], stdout=PIPE, input=myinput1)
            self.stdout = result1.stdout.decode('utf-8')
            print("Output 1: " + self.stdout)
            return self.stdout
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    #AIX user removal sometimes will not allow removal of /home/ drive, so 2nd remove user type is needed
    def RemoveUser_AIX(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput = str("echo -e '" + self.mypw + "\n' | sudo -S /usr/sbin/rmuser -p " + self.userid +
                        " && echo Successfully Executed").encode('utf-8')
            result = run(['ssh', userhost], stdout=PIPE, input=myinput)
            self.stdout = result.stdout.decode('utf-8')
            print(self.stdout)
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def RemoveUserAndHomeDrive_AIX(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput = str("echo -e '" + self.mypw + "\n' | sudo -S /usr/sbin/rmuser -p " + self.userid +
                        " && sudo -S rm -rf /home/" + self.userid + "; echo Successfully Executed").encode('utf-8')
            result = run(['ssh', userhost], stdout=PIPE, input=myinput)
            self.stdout = result.stdout.decode('utf-8')
            print(self.stdout)
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def ChangeGroups_AIX(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput1 = str(
                "U=" + self.userid + "; GROUP=" + self.usergroup + "; G=$(lsuser -a groups $U|awk -F'=' {'print $2'}|sed 's/ //g'); echo -e '" + self.mypw +
                "\n' | sudo -S chuser groups=$G,$GROUP $U && G=$(lsuser -a groups $U|awk -F'=' {'print $2'}) && echo User:" + self.userid + " has Groups:$G - Successfully Executed").encode('utf-8')
            result1 = run(['ssh', userhost], stdout=PIPE, input=myinput1)
            self.stdout = result1.stdout.decode('utf-8')
            print("Output 1: " + self.stdout)
            if "Operation timed out" in self.stdout:
                pass
            return self.stdout
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

    def RemoveGroups_AIX(self):
        try:
            userhost = ("{}@{}".format(self.myuser, self.ipaddress))
            print(userhost)
            myinput1 = str(
                "U=" + self.userid + "; GROUP=" + self.usergroup + "; LSUSER='lsuser -a groups'; ERMSG='ERROR: Cannot remove primary group'; P=$(id -gn $U); G=$(id -Gn $U|sed 's/ /,/g'); Gt=,$G,; Gt=$(echo $Gt|grep ,$GROUP,); if [[ $Gt = '' ]]; then echo ERROR: " + self.userid +
                " does not have group '" + self.usergroup + "'; else if [[ $P = $G ]]; then echo $ERMSG; elif [[ $P = $GROUP ]]; then echo $ERMSG; else G=${G#$GROUP,}; G=${G%,$GROUP}; G=$(echo $G|sed 's/,$GROUP,/,/g;'); G=${G#$P,}; G=${G%$P,}; G=$(echo $G|sed 's/,$P,/,/g;'); if [[ $G = $P ]]; then id $U>/dev/null && echo '" + self.mypw +
                "\n' | sudo -S chuser groups=$P $U && G=$(id -Gn $U|sed 's/ /,/g') && echo $G - Successfully Executed Option 1; else id $U>/dev/null && echo '" + self.mypw +
                "\n' | sudo -S chuser groups=$G $U && G=$(id -Gn $U|sed 's/ /,/g') && echo $G - Successfully Executed Option 2; fi; fi; fi;"
            ).encode('utf-8')
            result1 = run(['ssh', userhost], stdout=PIPE, input=myinput1)
            self.stdout = result1.stdout.decode('utf-8')
            print("Output 1: " + self.stdout)
            if "Operation timed out" in self.stdout:
                pass
            return self.stdout
        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass

