import os
import platform


def doScan(ip, msg=""):
    command = msg + " nmap -O -A -sT -F " + ip
    if platform.system() == "Linux":
        command = "sudo " + command
    print("Doing scan with command:", command)
    os.system(command + "> output")

if __name__ == "__main__":
	ip = input("Enter IP or subnet: ")
	doScan(ip)
