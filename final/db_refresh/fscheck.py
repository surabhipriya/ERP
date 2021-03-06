from __future__ import division
from paramiko import *
import paramiko
from sys import *
import re
from log4erp import *

def mount(hostname, username, password, database_sid):

    user = "ora" + database_sid.lower()
    path_array = []
    total= 0

    try:
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

	sftp_client = client.open_sftp()
        command = '/home/' + user + '/control_script_' + database_sid.upper() + '.sql' # | grep -i "sapdata*"' # variable IN
        #print command
        remote_file = sftp_client.open(command)
        remote_file = list(set(remote_file))
#	print remote_file

	for line in remote_file:
		paths = ""
#		print line
		if "ALTER" not in line:
                        if re.search("sapdata", line):
                                directory = line.split("/")
				#print directory
				for dire in directory:
#					print "dire"
#					print dire
                                        if "sapdata" in dire:
                                                paths = str(paths) + "/" + str(dire)
				#		print paths
						break
                                        else:
                                                paths = str(paths) + "/" + str(dire)
				#		print paths

				path_array.append(paths[4:])

	path_array = list(set(path_array))
        #print path_array	

	for each in path_array:
                command = "sudo du -sh "+ each + " | awk '{print $1}'"
	#	print command
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                output = stdout.readline().rstrip()

		if output.rstrip()[-1] == "M":
                        total = float(total) + (float(output[:-1]) / 1024)
                else:
                        total = float(total) + float(output[:-1])

	command = "sudo du -sh /sapmnt/ | awk '{print $1}'"
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readline().rstrip()
	
	total_mnt = 0
	if output.rstrip()[-1] == "M":
		total_mnt = float(total_mnt) + (float(output[:-1]) / 1024)
	else:
		total_mnt = float(total_mnt) + float(output[:-1])

	totals = float(total) + float(total_mnt)
	
	return float(totals)
	
	channel.close()
	client.close()

    except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
                print "FSCHECK:F:GERR_1101:Hostname unknown for " + system_name + " server (" + hostname + ")"
                write(logfile,'PRE:F:Hostname unknown [Error Code - 1101] for ' + system_name + ' server (' + hostname + ')')
                exit()
        elif str(e) == "list index out of range":
                print "FSCHECK:F:GERR_1102:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
                print "FSCHECK:F:GERR_1103:Authentication failed for " + system_name + " server (" + hostname + ")"
                write(logfile,'PRE:F:Authentication failed for .' + system_name + ' server (' + hostname + ') [Error Code - 1103]')
                exit()
        elif str(e) == "[Errno 110] Connection timed out":
                print "FSCHECK:F:GERR_0504: " + system_name + " Host Unreachable (" + hostname + ")"
                write(logfile,'PRE:F:GERR_0504: ' + system_name + ' Host Unreachable (' + hostname + ')')
                exit()
        elif "getaddrinfo failed" in str(e):
                print "FSCHECK:F:GERR_0505: Please check the " + system_name + " hostname that you have provide (" + hostname + ")"
                write(logfile,'PRE:F:GERR_0505: Please check the ' + system_name + ' hostname that you have provide (' + hostname + ')')
                exit()
        elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "FSCHECK:F:GERR_0506: " + system_name + "Host Unreachable or Unable to connect to port 22 (" + hostname + ")"
                write(logfile,'PRE:F:GERR_0506: ' + system_name + 'Host Unreachable or Unable to connect to port 22 (' + hostname + ')')
        elif "invalid decimal" in str(e):
                print "FSCHECK:F:GERR_0507:Unknown Error:" + str(e)
                write(logfile,'PRE:F:GERR_0507:Unknown Error:' + str(e))
        else:
                print "FSCHECK:F:" + str(e)


try:
    if argv[1] == "--u":
        print "usage: python fscheck.py <target Host> <target Login user> <target user password> <Target DB SID>"
    else:
	target_server = mount(argv[1], argv[2], argv[3],argv[4])
        print target_server



except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
                print "FSCHECK:F:GERR_1101:Hostname unknown"
                write(logfile,'PRE:F:Hostname unknown [Error Code - 1101]')
        elif str(e) == "list index out of range":
                print "FSCHECK:F:GERR_1102:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
                print "FSCHECK:F:GERR_1103:Authentication failed."
                write(logfile,'PRE:F:Authentication failed.[Error Code - 1103]')
        elif str(e) == "[Errno 110] Connection timed out":
                print "FSCHECK:F:GERR_0504:Host Unreachable"
                write(logfile,'PRE:F:GERR_0504:Host Unreachable')
        elif "getaddrinfo failed" in str(e):
                print "FSCHECK:F:GERR_0505: Please check the hostname that you have provide"
                write(logfile,'PRE:F:GERR_0505: Please check the hostname that you have provide')
        elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "FSCHECK:F:GERR_0506:Host Unreachable or Unable to connect to port 22"
                write(logfile,'PRE:F:GERR_0506:Host Unreachable or Unable to connect to port 22')
        elif "invalid decimal" in str(e):
                print "FSCHECK:F:GERR_0507:Unknown Error:" + str(e)
                write(logfile,'PRE:F:GERR_0507:Unknown Error:' + str(e))
        else:
                print "FSCHECK:F:" + str(e)
