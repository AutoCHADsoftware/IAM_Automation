# import csv
# import glob
# import os
# import numpy as np
#
#
#
# class ParsedCsv:
#     def __init__(self, filepath):
#         self.filepath = filepath
#
#         #filepath = '/Users/*/Downloads/*.csv'
#         self.list_of_files = glob.glob(filepath)
#         self.latest_file = max(self.list_of_files, key=os.path.getctime)
#
#         with open(self.latest_file, newline='') as incsv:
#             readCSV = csv.reader(incsv, delimiter=';')
#             sortedCSV = sorted(readCSV, key=lambda r: r[5])
#             Requests = []
#             Services = []
#             CustEnvs = []
#             Devices = []
#             Platforms = []
#             IPs = []
#             Emp_Owners = []
#             Serials = []
#             UserIDs = []
#             Privs = []
#
#             for row in sortedCSV:
#                 request = row[1]
#                 service = row[2]
#                 custenv = row[5]
#                 device = row[6]
#                 platform = row[7]
#                 ip = row[8]
#                 emp_owner = row[9]
#                 serial = row[10]
#                 userid = row[12]
#                 priv = row[13]
#
#                 Requests.append(request)
#                 Services.append(service)
#                 CustEnvs.append(custenv)
#                 Platforms.append(platform)
#                 IPs.append(ip)
#                 Emp_Owners.append(emp_owner)
#                 Devices.append(device)
#                 Serials.append(serial)
#                 UserIDs.append(userid)
#                 Privs.append(priv)
#
#
#             parsed_csv = np.array([Requests, Services, CustEnvs, Platforms, IPs, Emp_Owners, Devices, Serials, UserIDs, Privs])
#             self.slicedRequests = (parsed_csv[0, 1:])
#             self.slicedServices = (parsed_csv[1, 1:])
#             self.slicedCustEnv = (parsed_csv[2, 1:])
#             self.slicedPlatforms = (parsed_csv[3, 1:])
#             self.slicedIPs = (parsed_csv[4, 1:])
#             self.slicedEmpOwners = (parsed_csv[5, 1:])
#             self.slicedDevices = (parsed_csv[6, 1:])
#             self.slicedSerials = (parsed_csv[7, 1:])
#             self.slicedUserIDs = (parsed_csv[8, 1:])
#             self.slicedPrivs = (parsed_csv[9, 1:])
