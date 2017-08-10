import os
from sys import *
import subprocess
import log4erp
from log4erp import *

try:
#    if argv[1] == "--u":
#        print "usage: python assign_passwd.py <Target DB Hostname> <Target DB Sudo User> <Target DB Sudo User passwd> <Target Database SID> <Refresh ID>"
#    else:

        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        dbsid = argv[4]
        user_db = "ora" + dbsid.lower()
        refresh_id = argv[5] + '.log'
        location = argv[6]

        command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \"alter user SAPBOA identified by BOA_' + dbsid + '01;\" | sqlplus / as sysdba"'
        print command
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        if command.returncode == 0:
            print "BOA:P: The password for the user BOA has been changed successfully in the target database server (hostname - " + hostname + ")"
            log4erp.write(refresh_id,'POST:P:The password for the user BOA has been changed successfully in the target database server (Hostname -' + hostname + ')')
        else:
            print "BOA:F: The password for the user BOA has not been changed successfully in the target database server (hostname - " + hostname + ")"
            log4erp.write(refresh_id,'POST:F: The password for the user BOA has not been changed successfully in the target database server (Hostname -' + hostname + ')')

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "BOA:F:GERR_2501:Hostname unknown"
        log4erp.write(refresh_id, 'POST:F: Hostname unknown [Error Code - 2501]')
    elif str(e).strip() == "list index out of range":
        print "BOA:F:GERR_2502:Argument/s missing for BOA script"
    elif str(e) == "Authentication failed.":
        print "BOA:F:GERR_2503:Authentication failed."
        log4erp.write(refresh_id, 'POST:F:Authentication failed[Error Code - 2503]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "BOA:F:GERR_2504::Host Unreachable"
        write(refresh_id,'POST:F:Host Unreachable.[Error Code - 2504]')
    elif "getaddrinfo failed" in str(e):
        print "BOA:F:GERR_2505: Please check the hostname that you have provide"
        log4erp.write(refresh_id, 'POST:F: Please check the hostname that you have provide [Error Code - 2505]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "BOA:F:GERR_2506:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2506]')
    else:
        print "POST:F: " + str(e)

