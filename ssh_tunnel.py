import os
import random
import subprocess

import driver

value = 0

def get_subnet(username, public_ip, private_key_path):
	create_connection = "ssh " + str(username) + "@" + str(public_ip) + " -i " + str(private_key_path)[
																				 :-1] + " ip -o -f inet addr show"
	output = subprocess.check_output(create_connection, shell=True)
	output = output.decode('UTF-8')

	command = "echo \"" + output + "\" | awk '/scope global/ {print $4}'"
	subnet = subprocess.check_output(command, shell=True)
	subnet = subnet.decode('UTF-8')[:-1]

	return subnet


def get_process_id():
	command = 'ps aux | grep "ssh -D 9050"'
	output = subprocess.check_output(command, shell=True)

	output = str(output).split(" ")
	pid = output[8]

	return pid


def close_connection(v,error_popup, ui):
	global value
	value = v
	pid = get_process_id()
	command = "kill " + str(pid)
	os.system(command)

# Add IP 
def execute(command, error_popup, ui):
	try:
		os.system(command)
	except Exception as e:
		print("Failed to Connect!")
		ui.error_popup.setText("Failed execute:", command)
		ui.error_popup.exec_()


def perform_scan(subnet, error_popup, ui):
	driver.main(subnet, "remote", error_popup, ui)


def read_file(arg, error_popup, ui):
	file = open("ssh_details.info", "r")
	data = file.readlines()

	global value

	delimiter = " "

	for line in data:
		if (value == 1):
			break

		info = line.split(delimiter)

		username = info[0]
		public_ip = info[1]
		private_key_path = info[2]

		port_number = 9050

		if(public_ip == arg):
			subnet = get_subnet(username, public_ip, private_key_path)
			command = "ssh -D " + str(port_number) + " -Nf " + str(username) + "@" + str(public_ip) + " -i " + str(private_key_path)
			execute(command, error_popup, ui)
			perform_scan(subnet, error_popup, ui)
			close_connection(value, error_popup, ui)
			break
		elif(arg == "all"):
			subnet = get_subnet(username, public_ip, private_key_path)
			command = "ssh -D " + str(port_number) + " -Nf " + str(username) + "@" + str(public_ip) + " -i " + str(private_key_path)
			execute(command, error_popup, ui)
			perform_scan(subnet, error_popup, ui)
			print('before close all')
			close_connection(value, error_popup,ui)
			print('after close all')


def main(arg, error_popup, ui):
	read_file(arg, error_popup, ui)

if __name__ == '__main__':
	main("all")
