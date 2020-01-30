from subprocess import *


def psVersionTable():
    myinput = str("$PSVersionTable\n").encode('utf-8')
    result = run(['pwsh'], stdout=PIPE, input=myinput)
    print(result.stdout.decode('utf-8'))


hosts = ['172.25.223.38', '172.25.123.38']
endUsers = ['btbrooks', 'ejroesbery', 'jrgibbo', 'kjble', 'ncoffman', 'wehrhard', 'wltice']


def psNYCTremoveUsers():
    for host in hosts:
        for endUser in endUsers:
            username = "mta-bsc.org\garrett.jones"
            password = "Get-Content '/Users/garrettjones/MTAstring.rtf' | ConvertTo-SecureString"
            cred = "new-object -typename System.Management.Automation.PSCredential -argumentlist " + username + password
            myinput = str("Remove-LocalUser -Name " + endUser + " -ComputerName " + host +
                          " ` -Authentication default ` -Credential " + cred + "\n").encode('utf-8')
            result = run(['pwsh'], stdout=PIPE, input=myinput)
            print(result.stdout.decode('utf-8'))


# def psPasswordFile():
#     myinput = str("read-host -assecurestring | convertfrom-securestring | out-file /Users/garrettjones/MTAstring.rtf\n").encode('utf-8')
#     result = run(['pwsh'], stdout=PIPE, input=myinput)
#     print(result.stdout.decode('utf-8'))


# psVersionTable()
# psConnectAndVerify()
# psPasswordFile()
psNYCTremoveUsers()

# # # # # # # # # # # # # # # # # # # # # #
# Import-PSSession -Session (New-PSSession -HostName 172.25.223.38 -UserName mta-bsc.org\garrett.jones) -Module Import-Module ActiveDirectory
# $username = "mta-bsc.org\garrett.jones"
# $password = Get-Content 'C:\mysecurestring.txt' | ConvertTo-SecureString
# $cred = new-object -typename System.Management.Automation.PSCredential `
#          -argumentlist $username, $password
#
# $serverNameOrIp = "192.168.1.1"
# Restart-Computer -ComputerName $serverNameOrIp `
#                  -Authentication default `
#                  -Credential $cred
#                  <any other parameters relevant to you>
