import time
from random import randrange as rand
from Type1Playbook import *
from tkinter import *
from tkinter import filedialog
from tkinter import font as tkfont
from subprocess import *
from ttkwidgets import CheckboxTreeview
import csv
import glob
import os
import numpy as np
from UATSelenium import *
import string
import secrets

# MAKE SURE TO HAVE PROXIFIER SET UP, WHERE YOUR PROFILES ARE NAMED AFTER YOUR CUSTOMER ENVIRONMENTS/DELIVERY TEAMS,
# e.g. 'DELIVERY_TEAM-IAM.ppx', IN THE FOLLOWING DIRECTORY: ~/Library/Application Support/Proxifier/Profiles/{}.ppx'


class Counter:
    def __init__(self):
        self.complete_counter = 0
        self.failed_counter = 0
        self.total_counter = 0

    def complete_increment(self):
        self.complete_counter += 1

    def failed_increment(self):
        self.failed_counter += 1

    def reset(self):
        self.complete_counter = 0
        self.failed_counter = 0
        self.total_counter = 0

    def get_value(self):
        return self.complete_counter, self.failed_counter, self.total_counter


class Leftovers:
    CHECKBOX_List = []
    FILE_path = ''

    def boxed_list(self):
        return self.CHECKBOX_List

    def file_path(self):
        return self.FILE_path


def getValues():
    return Leftovers()


class UATApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MainStart, Config, MainComplete):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name #
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.menuBar = Menu(master=self)
        self.filemenu = Menu(self, tearoff=0)
        self.filemenu.add_command(label="Quit", command=self.quit)
        self.menuBar.add_cascade(label="File", menu=self.filemenu)

        self.leftframe = Frame(master=self)
        self.leftframe.pack(side=LEFT)

        self.lab = Label(self.leftframe)
        self.lab.img = PhotoImage(file='uat.gif')
        self.lab.config(image=self.lab.img)
        self.lab.grid()

        self.rightframe = Frame(master=self)
        self.rightframe.pack(side=RIGHT)

        self.startbutton = Button(self.rightframe, fg='black', width=10, text="Start", command=lambda: controller.show_frame("MainStart"))
        self.startbutton.grid(row=0, padx=25, pady=25, ipady=10)

        self.configbutton = Button(self.rightframe, text='Credentials\nManager', fg='black', width=10, command=lambda: controller.show_frame("Config"))
        self.configbutton.grid(row=1, padx=25, pady=25, ipady=10)

        self.exitbutton = Button(self.rightframe, text='Exit', fg='black', width=10, command=self.quit)
        self.exitbutton.grid(row=2, padx=25, pady=25, ipady=10)


class MainStart(Frame):
    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller
        self.filepath, self.Browse_button, self.Entry_user, self.Entry_password = '', '', '', ''
        self.tree, self.checkbox, self.data, self.Next_Button, self.Compare_Button = '', '', '', '', ''

        self.slicedRequests = ''
        self.slicedServices = ''
        self.slicedCustEnv = ''
        self.slicedPlatforms = ''
        self.slicedIPs = ''
        self.slicedEmpOwners = ''
        self.slicedDevices = ''
        self.slicedSerials = ''
        self.slicedUserIDs = ''
        self.slicedPrivs = ''
        self.empty_array = ''

        self.NewDeliveryTeams, self.NewPlatforms, self.NewHosts, self.NewIPAddresses, self.NewUserIDs, self.NewPasswords = [], [], [], [], [], []

        self.os_dirpath = os.path.abspath('.') + '/UATLogs/'
        os_filename = 'UATcreds.csv'
        self.os_path = os.path.join(self.os_dirpath, os_filename)

        self.sub_dirpath = '~/UAT/UATLogs/'
        sub_filename = 'UATcreds.csv'
        self.subprocess_path = os.path.join(self.sub_dirpath, sub_filename)

        self.boxtree = CheckboxTreeview()

        self.leftframe = Frame(master=self)
        self.leftframe.pack(side=LEFT)

        self.User_var, self.Passwd_var = StringVar(), StringVar()
        self.UserEntry = Entry(self.leftframe, textvariable=self.User_var)
        self.UserEntry.bind('<Return>', self.show_output_user)

        self.PasswordEntry = Entry(self.leftframe, textvariable=self.Passwd_var, show='*')
        self.PasswordEntry.bind('<Return>', self.show_output_passwd)

        Button(self.leftframe, text="Back", command=lambda: controller.show_frame("StartPage")).grid(row=5, column=1, sticky='w')
        Label(self.leftframe, text="File").grid(row=1, column=0)
        self.entry = Entry(self.leftframe).grid(row=1, column=1)

        # .grid() must be on separate line to ensure function only runs when clicked, 'lambda:' for similar reasons
        self.Creds_button = Button(self.leftframe, text="Verify Credentials", state=DISABLED, command=lambda: self.verifyW3())
        self.Creds_button.grid(row=2, column=1)

        self.Run_button = Button(self.leftframe, text="Run", state=DISABLED, command=lambda: self.processCSV())
        self.Run_button.grid(row=2, column=2)

        self.Browse_button = Button(self.leftframe, text="Browse", command=lambda: self.loadCSV())
        self.Browse_button.grid(row=1, column=2)

        self.rightframe = Frame(master=self)
        self.rightframe.pack(side=RIGHT)
        Label(self.rightframe, text="Load a CSV", font=controller.title_font).grid(row=0, sticky='w')
        TableMargin = Frame(self.rightframe, height=300, width=400)
        TableMargin.grid(row=1, sticky='w')


    def show_output_user(self, event):
        print("User: {}".format(self.User_var.get()))


    def show_output_passwd(self, event):
        print("Password: {}".format(self.Passwd_var.get()))


    def verifyW3(self):

        Label(self.leftframe, text="w3 UserID").grid(row=3, column=0)
        Label(self.leftframe, text="w3 Password").grid(row=4, column=0)

        self.UserEntry.grid(row=3, column=1)
        self.PasswordEntry.grid(row=4, column=1)

        stdoutdata = getoutput("cat ~/UAT/UATLogs/UATcreds.csv")
        splitdata = stdoutdata.split()
        # print("Data: {}".format(splitdata))

        if 'w3' not in splitdata:
            self.Creds_button.destroy()
            self.Creds_button = Button(self.leftframe, text="Create New Hosts File", command=lambda: self.getW3data())
            self.Creds_button.grid(row=5, column=1, sticky='e')
        else:
            # Need to add in logic for checking existing creds against .csv, and
            # ensuring all new hostnames/IPs get added, before switching Run button state to 'normal'
            Label(self.leftframe, text="Enter User ID").grid(row=3, column=0)
            Label(self.leftframe, text="Enter Password").grid(row=4, column=0)
            self.Run_button.config(state="normal")
            self.Creds_button.config(state=DISABLED)
            self.Browse_button.config(state=DISABLED)


    def getW3data(self):
        # self.UserEntry.grid(row=3, column=1)
        self.Entry_user = self.User_var.get()
        self.show_output_user('<return>')

        # self.PasswordEntry.grid(row=4, column=1)
        self.Entry_password = self.Passwd_var.get()
        self.show_output_passwd('<return>')

        if self.Entry_user == '' and self.Entry_password == '':
            print("Please enter your w3 ID and Password")
            self.verifyW3()
        elif self.Entry_user == '' and self.Entry_password != '':
            print("Please enter your w3 ID")
            self.verifyW3()
        elif self.Entry_user != '' and self.Entry_password == '':
            print("Please enter your w3 Password")
            self.verifyW3()
        elif self.Entry_user != '' and self.Entry_password != '':
            self.create_creds()
        else:
            return self.Entry_user, self.Entry_password


    def getIDandPassword(self):
        # self.UserEntry.grid(row=3, column=1)
        self.Entry_user = self.User_var.get()
        self.show_output_user('<return>')

        # self.PasswordEntry.grid(row=4, column=1)
        self.Entry_password = self.Passwd_var.get()
        self.show_output_passwd('<return>')

        if self.Entry_user == '' and self.Entry_password == '':
            print("Please enter your ID and Password for the checked boxes")
            self.compareHosts()
        elif self.Entry_user == '' and self.Entry_password != '':
            print("Please enter your ID for the checked boxes")
            self.compareHosts()
        elif self.Entry_user != '' and self.Entry_password == '':
            print("Please enter your Password for the checked boxes")
            self.compareHosts()
        elif self.Entry_user != '' and self.Entry_password != '':
            print("Running updateHosts()")
            self.updateHosts()
        else:
            return self.Entry_user, self.Entry_password


    def create_creds(self):
        # self.show_output_user()
        # self.show_output_passwd()
        row = ['Delivery Team', 'Platform', 'Hostname', 'IP Address', 'User ID', 'Password']
        row2 = ['w3 SSO', 'None', 'None', 'None', self.Entry_user, self.Entry_password]

        print("SubP Path: {}".format(self.subprocess_path))
        print("OS Path: {}".format(self.os_path))

        try:
            if not os.path.exists(self.os_dirpath):
                os.makedirs(self.os_dirpath)

            with open(self.os_path, 'w') as writeFile:
                writer = csv.writer(writeFile, delimiter=';')
                writer.writerow(row)
                writer.writerow(row2)

        except IOError as e:
            print("Error creating UATcreds.csv: {}".format(e))

        try:
            chmod600 = run("chmod 600 {}".format(self.subprocess_path), stdout=PIPE, shell=True)
            chmod_output = chmod600.stdout.decode('utf-8')
            print(chmod_output)
            self.verifyW3()
        except IOError as e:
            print("Chmod error {}".format(e))

    # not adding new user/pass to .csv, not populating 2nd treebox with info,
    # not changing 'process tickets' button to 'normal' state

    def ParsedCsv(self, filepath):
        self.filepath = filepath

        # filepath = '/Users/*/Downloads/*.csv'
        list_of_files = glob.glob(self.filepath)
        latest_file = max(list_of_files, key=os.path.getctime)

        print("Latest file: {}".format(latest_file))

        with open(latest_file, newline='') as incsv:
            readCSV = csv.reader(incsv, delimiter=';')
            sortedCSV = sorted(readCSV, key=lambda r: r[5])
            Requests = []
            Services = []
            CustEnvs = []
            Devices = []
            Platforms = []
            IPs = []
            Emp_Owners = []
            Serials = []
            UserIDs = []
            Privs = []

            for row in sortedCSV:
                request = row[1]
                service = row[2]
                custenv = row[5]
                device = row[6]
                platform = row[7]
                ip = row[8]
                emp_owner = row[9]
                serial = row[10]
                userid = row[12]
                priv = row[13]

                Requests.append(request)
                Services.append(service)
                CustEnvs.append(custenv)
                Platforms.append(platform)
                IPs.append(ip)
                Emp_Owners.append(emp_owner)
                Devices.append(device)
                Serials.append(serial)
                UserIDs.append(userid)
                Privs.append(priv)

            parsed_csv = np.array([Requests, Services, CustEnvs, Platforms, IPs, Emp_Owners, Devices, Serials, UserIDs, Privs])
            self.slicedRequests = (parsed_csv[0, 1:])
            self.slicedServices = (parsed_csv[1, 1:])
            self.slicedCustEnv = (parsed_csv[2, 1:])
            self.slicedPlatforms = (parsed_csv[3, 1:])
            self.slicedIPs = (parsed_csv[4, 1:])
            self.slicedEmpOwners = (parsed_csv[5, 1:])
            self.slicedDevices = (parsed_csv[6, 1:])
            self.slicedSerials = (parsed_csv[7, 1:])
            self.slicedUserIDs = (parsed_csv[8, 1:])
            self.slicedPrivs = (parsed_csv[9, 1:])
        return self.slicedRequests, self.slicedServices, self.slicedCustEnv, self.slicedPlatforms, self.slicedIPs, self.slicedEmpOwners, self.slicedDevices, self.slicedSerials, self.slicedUserIDs, self.slicedPrivs


    def loadCSV(self):
        lo = Leftovers()
        self.controller.withdraw()
        lo.FILE_path = filedialog.askopenfilename()
        self.controller.wm_deiconify()
        self.entry = Entry(self.leftframe)
        self.entry.grid(row=1, column=1)
        self.entry.insert(10, lo.FILE_path)
        self.filepath = lo.FILE_path
        self.Creds_button.config(state="normal")


    def processCSV(self):
        # print("loadCSV - File path: {}".format(self.filepath))
        if '.csv' in self.filepath:
            # If user clicks 'OK' multiple times, this will prevent things from breaking :)
            Frame(self.rightframe).destroy()
            Leftovers.CHECKBOX_List = []

            Select_all = Button(self.rightframe, text="Select All", command=lambda: self.selectAllBoxes())
            Select_all.grid(row=5, sticky='w')
            Deselect_all = Button(self.rightframe, text="De-select All", command=lambda: self.deselectAllBoxes())
            Deselect_all.grid(row=6, sticky='w')


            TableMargin = Frame(self.rightframe, height=300, width=400)
            TableMargin.grid(row=1, sticky='w')

            scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
            scrollbary = Scrollbar(TableMargin, orient=VERTICAL)

            self.boxtree = CheckboxTreeview(TableMargin, columns=('Request', "Service", "CustEnv", "Platform", 'IP', 'Owner', 'Device', 'Serial', 'UserID', 'Priv'),
                                            selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

            # self.boxtree = CheckboxTreeview(TableMargin, columns="Select", yscrollcommand=scrollbary.set)
            scrollbary.config(command=self.boxtree.yview)
            scrollbary.grid(row=3, column=0, sticky='s', ipady=5)

            scrollbarx.config(command=self.boxtree.xview)
            scrollbarx.grid(row=4, sticky='w')


            self.boxtree.heading('Request', text="Request", anchor=W)
            self.boxtree.heading('Service', text="Service", anchor=W)
            self.boxtree.heading('CustEnv', text="Customer Env", anchor=W)
            self.boxtree.heading('Platform', text="Platform", anchor=W)
            self.boxtree.heading('IP', text="IP", anchor=W)
            self.boxtree.heading('Owner', text="Owner", anchor=W)
            self.boxtree.heading('Device', text='Device', anchor=W)
            self.boxtree.heading('Serial', text="Serial", anchor=W)
            self.boxtree.heading('UserID', text="User ID", anchor=W)
            self.boxtree.heading('Priv', text="Privilege", anchor=W)
            self.boxtree.column('#0', stretch=NO, minwidth=0, width=30)
            self.boxtree.column('#1', stretch=NO, minwidth=0, width=100)
            self.boxtree.column('#2', stretch=NO, minwidth=0, width=100)
            self.boxtree.column('#3', stretch=NO, minwidth=0, width=100)
            self.boxtree.column('#4', stretch=NO, minwidth=0, width=100)
            self.boxtree.column('#5', stretch=NO, minwidth=0, width=100)
            self.boxtree.column('#6', stretch=NO, minwidth=0, width=100)
            self.boxtree.column('#7', stretch=NO, minwidth=0, width=100)
            self.boxtree.column('#8', stretch=NO, minwidth=0, width=100)
            self.boxtree.column('#9', stretch=NO, minwidth=0, width=100)
            self.boxtree.column('#10', stretch=NO, minwidth=0, width=100)
            self.boxtree.grid(row=3, column=0, sticky='nw')

            self.ParsedCsv(self.filepath)
            # parsed_csv = np.array([Requests, Services, CustEnvs, Platforms, IPs, Emp_Owners, Devices, Serials, UserIDs, Privs])
            for (request, service, cust_env, platform, ip, owner, device, serial, user_id, priv) in zip(
                    self.slicedRequests, self.slicedServices, self.slicedCustEnv, self.slicedPlatforms, self.slicedIPs,
                    self.slicedEmpOwners, self.slicedDevices, self.slicedSerials, self.slicedUserIDs, self.slicedPrivs):
                self.boxtree.change_state(self.checkbox, "checked")
                self.boxtree.insert("", 0, values=(request, service, cust_env, platform, ip, owner, device, serial, user_id, priv))
                Leftovers.CHECKBOX_List.append(request)
            print(Leftovers.CHECKBOX_List)

            #next version, have 'command=lambda: self.controller.show_frame("MainComplete")
            self.compareHosts()
        else:
            pass


    def compareHosts(self):
        #Need to get select all/de-select all working
        #Need another option to check/un-check by account
        #Need 3rd option to check/un-check by checkbox click
        TableMargin = Frame(self.rightframe, height=300, width=400)
        TableMargin.grid(row=2, sticky='w')

        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        scrollbary.config(command=self.boxtree.yview)
        scrollbary.grid(row=3, column=0, sticky='s', ipady=5)

        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbarx.config(command=self.boxtree.xview)
        scrollbarx.grid(row=4, sticky='w')

        # Delivery Team	Platform	Hostname	IP Address	User ID	Password
        self.boxtree = CheckboxTreeview(TableMargin, columns=('DeliveryTeam', 'Platform', 'Hostname', 'IPAddress', 'UserID', 'Password'),
                                        selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

        self.boxtree.heading('DeliveryTeam', text="Delivery Team", anchor=W)
        self.boxtree.heading('Platform', text="Platform", anchor=W)
        self.boxtree.heading('Hostname', text="Hostname", anchor=W)
        self.boxtree.heading('IPAddress', text="IP Address", anchor=W)
        self.boxtree.heading('UserID', text="User ID", anchor=W)
        self.boxtree.heading('Password', text="Password", anchor=W)

        self.boxtree.column('#0', stretch=NO, minwidth=0, width=30)
        self.boxtree.column('#1', stretch=NO, minwidth=0, width=100)
        self.boxtree.column('#2', stretch=NO, minwidth=0, width=100)
        self.boxtree.column('#3', stretch=NO, minwidth=0, width=100)
        self.boxtree.column('#4', stretch=NO, minwidth=0, width=100)
        self.boxtree.column('#5', stretch=NO, minwidth=0, width=100)
        self.boxtree.column('#6', stretch=NO, minwidth=0, width=100)

        self.boxtree.grid(row=3, column=0, sticky='sw')

        self.Compare_Button = Button(self.leftframe, text="Enter UserID and Pass", command=lambda: self.getIDandPassword())
        self.Compare_Button.grid(row=5, column=1, sticky='e')

        #     Leftovers.CHECKBOX_List.append(request)
        # print(Leftovers.CHECKBOX_List)


    def updateHosts(self):

        self.Next_Button = Button(self.leftframe, text="Process Tickets", state=DISABLED, command=lambda: self.main())
        self.Next_Button.grid(row=6, column=1, sticky='e')

        DeliveryTeams, Platforms, Hosts, IPAddresses, UserIDs, Passwords = [], [], [], [], [], []

        with open(self.os_path, newline='') as incsv:
            readCSV = csv.reader(incsv, delimiter=';')

            # may allow for user input to select 'index' value of below sort
            # and display the hosts in a treebox so they can compare/control both with one checkbox
            # sortedCSV = sorted(readCSV, key=lambda r: r[5])

            for row in readCSV:
                print("Row: {}".format(row))
                deliveryteam = row[0]
                platform = row[1]
                host = row[2]
                ipaddress = row[3]
                userid = row[4]
                password = row[5]

                DeliveryTeams.append(deliveryteam)
                Platforms.append(platform)
                Hosts.append(host)
                IPAddresses.append(ipaddress)
                UserIDs.append(userid)
                Passwords.append(password)

            # OldArray = np.array([DeliveryTeams, Platforms, Hosts, IPAddresses, UserIDs, Passwords])
            # OldDelTeams = (OldArray[0, 2:])
            # OldPlatforms = (OldArray[1, 2:])
            # OldHosts = (OldArray[2, 2:])
            # OldIPs = (OldArray[3, 2:])
            # OldUsers = (OldArray[4, 2:])
            # OldPasswords = (OldArray[5, 2:])


        self.empty_array = np.array([self.NewDeliveryTeams, self.NewPlatforms, self.NewHosts, self.NewIPAddresses, self.NewUserIDs, self.NewPasswords])

        # parsed_csv = np.array([Requests, Services, CustEnvs, Platforms, IPs, Emp_Owners, Devices, Serials, UserIDs, Privs])
        # Delivery Team	Platform	Hostname	IP Address	User ID	Password

        for team, platform, host, ipaddress in zip(self.slicedCustEnv, self.slicedPlatforms, self.slicedDevices, self.slicedIPs):
            print("Hostname: {}\nslicedOld: {}\nParsedcsv Devices: {}\n".format(host, Hosts, self.slicedDevices))
            if host not in Hosts:
                self.NewDeliveryTeams.append(team)
                self.NewPlatforms.append(platform)
                self.NewHosts.append(host)
                self.NewIPAddresses.append(ipaddress)
                self.NewUserIDs.append(self.Entry_user)
                self.NewPasswords.append(self.Entry_password)
            try:
                with open(self.os_path, 'a') as writeFile:
                    writer = csv.writer(writeFile, delimiter=';')
                    writer.writerows(self.NewDeliveryTeams)
                    writer.writerows(self.NewPlatforms)
                    writer.writerows(self.NewHosts)
                    writer.writerows(self.NewIPAddresses)
                    writer.writerows(self.NewUserIDs)
                    writer.writerows(self.NewPasswords)
            except IOError as e:
                print("Error appending Hosts log {}".format(e))
            else:
                print("{} was found in {}".format(host, Hosts))
                self.Next_Button.config(state='normal')
                #change another button state to disabled?

        for (team, platform, hostname, ipaddress, userid, passwd) in zip(self.NewDeliveryTeams, self.NewPlatforms, self.NewHosts,
                                                                         self.NewIPAddresses, self.NewUserIDs, self.NewPasswords):
            print("Updating boxtree")
            self.boxtree.change_state(self.checkbox, "checked")
            self.boxtree.insert("", 0, values=(team, platform, hostname, ipaddress, userid, passwd))


    def selectAllBoxes(self):
        for (request, service, cust_env, platform, ip, owner, device, serial, user_id, priv) in zip(self.ParsedCsv(self.filepath)[0], self.ParsedCsv(self.filepath)[1], self.ParsedCsv(self.filepath)[2], self.ParsedCsv(self.filepath)[3], self.ParsedCsv(self.filepath)[4], self.ParsedCsv(self.filepath)[5], self.ParsedCsv(self.filepath)[6], self.ParsedCsv(self.filepath)[7], self.ParsedCsv(self.filepath)[8], self.ParsedCsv(self.filepath)[9]):
            self.boxtree.change_state(self.checkbox, "checked")
            if request not in Leftovers.CHECKBOX_List:
                Leftovers.CHECKBOX_List.append(request)
            print(Leftovers.CHECKBOX_List)


    def deselectAllBoxes(self):
        for (request, service, cust_env, platform, ip, owner, device, serial, user_id, priv) in zip(self.ParsedCsv(filepath=self.filepath)[0], self.ParsedCsv(filepath=self.filepath)[1], self.ParsedCsv(filepath=self.filepath)[2], self.ParsedCsv(filepath=self.filepath)[3], self.ParsedCsv(filepath=self.filepath)[4], self.ParsedCsv(filepath=self.filepath)[5], self.ParsedCsv(filepath=self.filepath)[6], self.ParsedCsv(filepath=self.filepath)[7], self.ParsedCsv(filepath=self.filepath)[8], self.ParsedCsv(filepath=self.filepath)[9]):
            self.boxtree.change_state(self.checkbox, "unchecked")
            if request in Leftovers.CHECKBOX_List:
                Leftovers.CHECKBOX_List.remove(request)
            print(Leftovers.CHECKBOX_List)


    def main(self):
        ###future goal to implement button that will connect to UAT and auto-download .CSV###
        # bs = BrowserSelect(browser=webdriver.Safari(), input_browser='', url='https://uat.us.ibm.com/iam?SSOlogin=true')
        # bs.browserDefintion()
        # print(bs.browser)
        # bs.uatDownloadCSV()
        mc = Counter()
        UID = str(rand(4000, 44000))

        CompletedTickets = []
        FailedTickets = []
        row = ['Request Number', 'Completed/Failed', 'User ID', 'Temp Passwd']

        timestr = time.strftime("%Y%m%d-%H%M%S")
        os_dirpath = os.path.abspath('.') + '/UATLogs/'
        os_filename = timestr + 'TICKETLOG.csv'
        os_path = os.path.join(os_dirpath, os_filename)

        try:
            if not os.path.exists(os_dirpath):
                os.makedirs(os_dirpath)
            with open(os_path, 'w') as writeFile:
                writer = csv.writer(writeFile, delimiter=';')
                writer.writerow(row)
        except IOError as e:
            print("Error creating UAT log: {}".format(e))



        for (request, service, cust_env, platform, ip, owner, device, serial, user_id, priv) in zip(self.ParsedCsv(self.filepath)[0], self.ParsedCsv(self.filepath)[1], self.ParsedCsv(self.filepath)[2], self.ParsedCsv(self.filepath)[3], self.ParsedCsv(self.filepath)[4], self.ParsedCsv(self.filepath)[5], self.ParsedCsv(self.filepath)[6], self.ParsedCsv(self.filepath)[7], self.ParsedCsv(self.filepath)[8], self.ParsedCsv(self.filepath)[9]):
            if request in Leftovers.CHECKBOX_List:
                try:
                    sub_dirpath = '~/UAT/'
                    sub_filename = '{}.ppx'.format(cust_env)
                    proxy_process_path = os.path.join(sub_dirpath, sub_filename)
                    result = run(['open', '-a', 'Proxifier', proxy_process_path], stdout=PIPE)
                    print(result.stdout.decode('utf-8'))
                except Exception as e:
                    print("Exception: {}".format(e))


                def gecosmaker():
                    c_first = [char for char in serial][-3:]
                    country_code = ''
                    for number in c_first:
                        country_code = country_code + number
                    print("Country code: {}".format(country_code))

                    c_second = [char for char in serial][:-3]
                    emp_serial = ''
                    for number in c_second:
                        emp_serial = emp_serial + number
                    print("Employee Serial: {}".format(emp_serial))
                    print("Employee: {}".format(owner))

                    emp_status = 'I'
                    company = 'IBM'

                    # Either make name counting more sophisticated or add more if/elif statements
                    # Currently does not account for many Spanish/Portuguese names with 5/6 names
                    if owner.count(' ') == 3:
                        space1 = owner.index(' ')
                        first_name = owner[0:space1]

                        space2 = owner.index(' ', space1 + 1)
                        middle_initial = owner[space1 + 1:space2]

                        space3 = owner.index(' ', space2 + 1)
                        nickname = owner[space2 + 1:space3]
                        if nickname == '*CONTRACTOR*':
                            emp_status = 'E'
                        last_name = owner[space3 + 1:]

                        new_namelist = "{}.{} {} {}".format(last_name, first_name, middle_initial, nickname)
                    elif owner.count(' ') == 2:
                        space1 = owner.index(' ')
                        first_name = owner[0:space1]

                        space2 = owner.index(' ', space1 + 1)
                        nickname = owner[space1 + 1:space2]

                        last_name = owner[space2 + 1:]

                        new_namelist = "{}.{} {}".format(last_name, first_name, nickname)
                    elif owner.count(' ') == 1:
                        space1 = owner.index(' ')

                        first_name = owner[0:space1]
                        last_name = owner[space1:]

                        new_namelist = "{}.{}".format(last_name, first_name)
                    else:
                        new_namelist = "{}".format(owner)

                    gecos = "{}/{}/{}/{}/{}/".format(country_code, emp_status, emp_serial, company, new_namelist)
                    print("Gecos: {}".format(gecos))
                    return gecos

                def SecureRandomString(string_length):
                    """Generate a secure random string of letters, digits and special characters """
                    password_characters = string.ascii_letters + string.digits + string.punctuation
                    return ''.join(secrets.choice(password_characters) for i in range(string_length))


                user_pass = SecureRandomString(12)

                Command = gecosmaker()

                spchAIX = SpchAIXTicket(myuser=self.NewUserIDs, mypw=self.NewPasswords, ipaddress=device, userid=user_id,
                                        usergroup=priv, userpw=user_pass, command=Command, uid=UID, stdout='')
                spchLinux = SpchLinuxTicket(myuser=self.NewUserIDs, mypw=self.NewPasswords, ipaddress=device, userid=user_id,
                                            usergroup=priv, userpw=user_pass, command=Command, uid=UID, stdout='')
                nyctAIX = SpchAIXTicket(myuser=self.NewUserIDs, mypw=self.NewPasswords, ipaddress=device, userid=user_id,
                                        usergroup=priv, userpw=user_pass, command=Command, uid=UID, stdout='')
                olinAIX = SpchAIXTicket(myuser=self.NewUserIDs, mypw=self.NewPasswords, ipaddress=device, userid=user_id,
                                        usergroup=priv, userpw=user_pass, command=Command, uid=UID, stdout='')

                # windows = SpchWindowsTicket(command='hi')
                # windows.spchRemoveUserWindows()

                def ticketappend(stdout):
                    words = stdout.split()
                    if "Successfully" not in words:
                        FailedTickets.append([request, "failed"])
                        mc.failed_increment()
                        print("Failed ticket " + str(request))
                    elif "Successfully" in words:
                        CompletedTickets.append([request, "completed"])
                        mc.complete_increment()
                        print("Completed ticket " + str(request))
                        if mc.complete_counter == 1000:
                            uatPart2()
                        else:
                            pass
                    else:
                        pass


                if cust_env == 'SHARED_PRIVATE_CLOUD_HUB-IAM':
                    print(cust_env, service, platform, request)

                    ##OTHER TICKET TYPES
                    #
                    #Transfer Application User - EXAMPLE
                    #sudo /usr/sbin/usermod -c '897/C/*SPCDB2//SHARED_PRIVATE_CLOUD_HUB-DB2_PO/' db2inst1 && echo Successfully Executed
                    #
                    #Create Privilege on device
                    #sudo /usr/sbin/groupadd ibm_ans && echo Successfully Executed
                    #
                    #Reset Personal User Password - weird pw reset type - command faillog not found
                    #sudo /usr/bin/faillog -u trangd -r && echo '***********' | sudo passwd --stdin trangd && sudo /usr/bin/chage -d 0 trangd && echo Successfully Executed
                    #
                    #Create Application User Account
                    #will need to prompt user for gecos desc and uid, and set gecos and uid to user input
                    #U=tivdbadm; C='897/S/*SPCDB2/IBM/SHARED_PRIVATE_CLOUD_HUB-DB2_PO/'; GP=users; sudo /usr/sbin/useradd -g $GP -u 3788 -c "$C" $U && echo '************' | sudo passwd --stdin $U && sudo /usr/bin/chage -d 0 $U && echo Successfully Executed
                    #Perform check on stdout, to see if uid is not unique, give 4 options, "force" UID through, prompt user for new UID, option to not enter a UID altogether, or option to skip that ticket
                    #

                    if service == 'Personal UserID Creation' and platform == 'AIX':
                        print("Starting request " + request)
                        spchAIX.spchNewUserAIX()
                        ticketappend(spchAIX.stdout)


                    elif service == 'Personal UserID Creation' and platform == 'REDHAT LINUX':
                        print("Starting request " + request)
                        spchLinux.spchNewUserLinux()
                        ticketappend(spchLinux.stdout)


                    elif service == 'Privilege Addition of Personnal User Account' and platform == 'REDHAT LINUX':
                        print("Starting request " + request)
                        spchLinux.spchChangeGroupsLinux()
                        ticketappend(spchLinux.stdout)


                    elif service == 'Unlock Personal User Account' and platform == 'AIX':
                        print("Starting request " + request)
                        spchAIX.spchUnlockUserAIX()
                        ticketappend(spchAIX.stdout)

                    elif service == 'Personal UserID Add Profile' and platform == 'AIX':
                        print("Starting request " + request)
                        spchAIX.spchChangeGroupsAIX()
                        ticketappend(spchAIX.stdout)


                    elif service == 'Personal UserID Add Profile' and platform == 'REDHAT LINUX':
                        print("Starting request " + request)
                        spchLinux.spchChangeGroupsLinux()
                        ticketappend(spchLinux.stdout)


                    elif service == 'Application UserID Add Profile' and platform == 'REDHAT LINUX':
                        print("Starting request " + request)
                        UID = input("Please specify the UID for {} on server {}: ".format(spchLinux.userid,
                                                                                          spchLinux.ipaddress))
                        spchLinux.spchChangeGroupsLinux()
                        ticketappend(spchLinux.stdout)


                    elif service == 'Personal UserID Password Reset' and platform == 'AIX':
                        print("Starting request " + request)
                        spchAIX.spchPasswordResetAIX()
                        ticketappend(spchAIX.stdout)

                    elif service == 'Create Privilege on device' and platform == 'REDHAT LINUX':
                        print("Starting request " + request)
                        spchLinux.spchCreatePrivOnDeviceLinux()
                        ticketappend(spchAIX.stdout)

                    else:
                        print(request, "I'm sorry, I can't do {} on {}, Dave".format(service, platform))
                        ticketappend("{} {}".format(spchAIX.stdout, spchLinux.stdout))


                elif cust_env == 'NYCT-IAM':
                    print(cust_env, service, platform)
                    if service == 'Personal UserID Add Profile' and platform == 'AIX':
                        print("Starting request " + request)
                        nyctAIX.spchChangeGroupsAIX()
                        ticketappend(nyctAIX.stdout)
                    else:
                        print(request, "I'm sorry, I can't do " + service + " on " + platform + ", Dave")
                        ticketappend(nyctAIX.stdout)


                elif cust_env == 'OLIN-IAM':
                    print(cust_env, service, platform, request)
                    if service == 'Personal UserID Remove Profile':
                        print("Starting request " + request)
                        olinAIX.spchRemoveGroupsAIX()
                        ticketappend(olinAIX.stdout)

                    elif service == 'Personal UserID Add Profile' and platform == 'AIX':
                        print("Starting request " + request)
                        olinAIX.spchChangeGroupsAIX()
                        ticketappend(olinAIX.stdout)

                    elif service == 'Unlock Personal User Account' and platform == 'AIX':
                        print("Starting request " + request)
                        olinAIX.spchUnlockUserAIX()
                        ticketappend(olinAIX.stdout)

                    elif service == 'Personal UserID Removal' and platform == 'AIX':
                        print("Starting request " + request)
                        olinAIX.spchAIXRemoveUser()
                        ticketappend(olinAIX.stdout)

                    else:
                        print(request, "I'm sorry, I can't do {} on {}, Dave".format(service, platform))
                        ticketappend(olinAIX.stdout)

                else:
                    print("{}: I'm sorry, I can't do {}, Dave".format(request, cust_env))
                    ticketappend("{} {}".format(spchAIX.stdout, spchLinux.stdout))
            else:
                pass

            try:
                with open(os_path, 'a') as writeFile:
                    writer = csv.writer(writeFile, delimiter=';')
                    writer.writerows(CompletedTickets)
                    writer.writerows(FailedTickets)
            except IOError as e:
                print("Error appending UAT log: {}".format(e))

            def uatPart2():
                response = input("Read output. Enter 'y' to close tickets, or 'n' to quit: ").lower()
                if response == 'y':
                    print("Ok, closing tickets.....NOT")
                    quit()
                elif response == 'n':
                    print("Ok, not closing tickets....HAVE A GOOD DAY")
                    quit()
                else:
                    print("Please enter either 'y' or 'n'")
                    uatPart2()



class Config(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.ms = MainStart(parent='', controller=controller)
        self.output, self.output1, self.output2 = '', '', ''
        self.controller = controller
        label = Label(self, text="Configuration", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


        # creds_button = Button(self, text="Manually Edit\nCredentials File", command=lambda: self.verifyW3())
        # creds_button.pack()

        rsa_button = Button(self, text="Get RSA Keys", command=lambda: self.RSA())
        rsa_button.pack()

        # editHosts_button = Button(self, text="Manually Edit\nHosts File", command=lambda: self.edithosts())
        # editHosts_button.pack()

        button = Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom")


    def RSA(self):

        prompt = input("Check RSA Keys?").lower()
        if prompt == 'y':
            userprompt = input("Enter your user name: ")
            for host_name in zip(self.ms.ParsedCsv(filepath=self.ms.filepath)[6]):
                userhost = "{}@{}".format(userprompt, str(host_name))
                print(userhost)
                for user in userhost:
                    print(user)
                    result2 = run(['ssh-keyscan', '-H', user, '>> ~/.ssh/known_hosts'], stdout=PIPE)
                    print(result2)
                    output2 = result2.stdout.decode('utf-8')
                    print(user + " had this result " + output2)
        elif prompt == 'n':
            print("Quitting without checking RSAs")
        else:
            print("Please enter a 'y' or 'n'")
            self.RSA()


    def edithosts(self):
        try:
            passw = str(input("Please enter your password here: "))
            for ip_address, host_name in zip(self.ms.ParsedCsv(filepath=self.ms.filepath)[4], self.ms.ParsedCsv(filepath=self.ms.filepath)[6]):
                matches_in_hosts = "$(grep -n $" + host_name + "/etc/hosts | cut -f1 -d:)"
                host_entry = "${" + ip_address + "} ${" + host_name + "}"

                myinput = str(
                    "echo " + passw + "; if [ ! -z " + matches_in_hosts + " ];then;echo 'Updating existing hosts entry.';while read -r line_number; do;sudo sed -i '' '${line_number}s/.*/${" + host_entry + "} /' /etc/hosts;done <<< " + matches_in_hosts + ";else;echo 'Adding new hosts entry.';echo " + host_entry + " | sudo tee -a /etc/hosts > /dev/null;fi;")
                result = run(['sudo', '--', 'sh', '-c', myinput], stdout=PIPE, shell=True)
                self.output = result.stdout.decode('utf-8')
                print("Output: " + self.output)

                myinput1 = str("'echo '" + ip_address + "\t" + host_name + "\n' >> /etc/hosts'")
                result1 = run(['sudo', '--', 'sh', '-c', myinput1], stdout=PIPE, shell=True)
                self.output1 = result1.stdout.decode('utf-8')
                print("Output 1: " + self.output1)

                result2 = run(['sudo', '--', 'sh', '-c', 'echo', ip_address, '\t', host_name, '>> /etc/hosts', '\n'],
                              stdout=PIPE)
                self.output2 = result2.stdout.decode('utf-8')
                print(self.output2)

        except TimeoutExpired(timeout=5, cmd=[b'Timeout Exceeded 5 seconds, disconnecting']):
            pass


class MainComplete(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Process Tickets", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.entry = Entry(self)
        self.entry.pack()
        p1main = MainStart(controller=controller, parent=parent)
        for request in Leftovers.CHECKBOX_List:
            self.entry.insert(self, request)
            self.entry.pack()

        button = Button(self, text="Back", command=lambda: controller.show_frame("MainStart"))
        button.pack(side="bottom")

        Process_Tickets = Button(self, text="Process Above\nTickets", command=lambda: p1main.main())
        Process_Tickets.pack(side="bottom")


if __name__ == "__main__":
    app = UATApp()
    app.geometry("720x480")
    app.title("UAT ~ Automated")
    app.mainloop()
    #main()
