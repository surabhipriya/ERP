#!/usr/bin/sh
from __future__ import division
import paramiko
import re
import glob
import os
from paramiko import *
from sys import *
import subprocess
import log4erp
from log4erp import *
def space_check(hostname, username, password, profilepath,location,logfile):

	command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "dir ' + profilepath + ' /s /b | findstr DVEBMGS* | findstr -V START"'
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        profilepath = out.split('\n')[3]
        print profilepath

	command='c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"get-content ' + profilepath + ' | select-string login/no_automatic_user_sapstar\\"\""'
	print command
	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	out, err = command.communicate()
	#print out
	out=out.split('\n')
	#print out
	out=''.join(out)
	#print out
	if 'login/no_automatic_user_sapstar' not in out:
		command='c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"add-content ' + profilepath + ' \'login/no_automatic_user_sapstar = 1\'\\"\"'
		print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		#print out
		if command.returncode == 0:
			print 'POST:P:parameter set to one'
			write(logfile,'POST:P:parameter set to one')
		else:
			print 'POST:F:parameter not set to one'
			write(logfile,'POST:F:parameter not set to one')
	else:
		parameter = out.split('used',1)
		#print parameter
		parameter = parameter[1].strip()
		print parameter
		command='c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"(Get-Content ' + profilepath +').Replace(\'' + parameter + '\',\'login/no_automatic_user_sapstar = 1\') | set-content ' + profilepath + '"\\"\"'
		print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		#print out
		if command.returncode == 0:
			print 'POST:P:parameter set to one'
			write(logfile,'POST:P:parameter set to one')
		else:
			print 'POST:F:parameter not set to one'
		        write(logfile,'POST:F:parameter not set to one')
try:
    if argv[1] == "--u":
        print "usage: c:\python27\python  POST.py <Target Host> <Target Sudo Username> <Target Sudo Password> <profilepath>"
    else:
		hostname = argv[1]
		username = argv[2]
		password = argv[3]
		profilepath = argv[4]
		location = argv[5]
		logfile = argv[6]
		space_check(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6])

except Exception as e:
	if "No such file or directory" in str(e):
		print "No such file"
#		write(logfile,'No such file')
	elif "name 'user' is not defined" in str(e):
		print "POST:F: Please enter App for Application Server or Db for Database Server"
#		write(logfile,'POST:F:Please enter App for Application Server or Db for Database Server')
	elif str(e).strip() == "list index out of range":
                print "POST:F:GERR_1212:Argument/s missing for the script"
#		write(logfile,'POST:F:GERR_1212:Argument/s missing for the script')
	else:
		print "POST :" + str(e)
#		write(logfile,'POST:' + str(e))
