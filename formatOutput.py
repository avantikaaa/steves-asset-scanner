import datetime
from Host import *
import subprocess
import platform

def getAllLines(data, substr):
	out = []
	while substr in data:
		start = data.find(substr)
		end = data[start:].find("\n")
		out.append(data[start + len(substr):start + end].strip("\n"))
		data = data[start + end: ]
	return out

def getLine(data, substr):
	start = data.find(substr)
	if start == -1:
		return ""
	end = data[start:].find("\n")

	return data[start + len(substr):start + end].strip("\n")

def getSelfInfo():
	if platform.system() == "Windows":
		stdout = subprocess.check_output("ipconfig /all", shell = True)
		stdout = stdout.decode("utf-8")

		hostName = getLine(stdout, "Host Name")
		hostName = hostName.split(": ")[1]

		IP = getLine(stdout, "IPv4 Address")
		IP = IP.split(": ")[1]
		IP = IP.split("(Preferred)")[0]

		MAC = getAllLines(stdout, "Physical Address")[-1]
		MAC = MAC.split(": ")[1]
		

		return {"mac": MAC.strip("\r"), "ip": IP.strip("\r"), "name": hostName.strip("\r")}

	elif platform.system() == "Linux":
		ip = subprocess.check_output("hostname -I | awk \'{print $1}\'", shell = True)
		ip = ip.decode("utf-8").strip("\n")

		mac = subprocess.check_output("ip -o link | grep ether | awk '{ print $2\" : \"$17 }' | grep $(ip route show default | awk '/default/ {print $5}')", shell=True)
		mac = mac.decode("utf-8")
		mac = mac.split(": : ")[-1].strip("\n")

		name = subprocess.check_output("hostname", shell = True)
		name = name.decode("utf-8").strip("\n")

		return {"mac": mac, "ip":ip, "name": name}		

	else:
		ip = subprocess.check_output("ipconfig getifaddr eth0", shell = True)
		ip = ip.decode("utf-8").strip("\n")

		mac = subprocess.check_output("fconfig en1 | awk \'/ether/{print $2}\'", shell=True)
		mac = mac.decode("utf-8")
		# print(mac)
		mac = mac.strip("\n")

		name = subprocess.check_output("whoami", shell = True)
		name = name.decode("utf-8").strip("\n")

		return {"mac": mac, "ip":ip, "name": name}

def formatOutput(data):
	print("Reading data")
	timeStamp = str(datetime.datetime.now())[:-7]

	tmp = data.find("\n")
	data = data[tmp+1:]
	data = data.split("Nmap scan report for ")
	data = data[1:]

	out = {}
	flag = True

	for device in data:
		host = Host()
		host.ts = timeStamp

		# host status
		if "Host is up" in device:
			host.status = "up"

		# mac address
		mac = getLine(device, "MAC Address: ")
		if len(mac) > 0:
			mac = mac.split(" ")
			host.mac = mac[0]

		rawData = device.split("\n")
		# os in use
		os = getLine(device, "Service Info: OS: ")
		if len(os) > 0:
			host.OS = os

		#read IP, name(if available)
		ip = rawData[0].split(" ")
		if len(ip) == 1:
			host.ip = ip[0]
		else:
			host.ip = ip[1][1:-1]
			host.name = ip[0]

		out[host.ip] = host

	selfInfo = getSelfInfo()
	if selfInfo["ip"] in out:
		out[selfInfo["ip"]].mac = selfInfo["mac"]
		out[selfInfo["ip"]].name = selfInfo["name"]

	else:
		host = Host()
		host.ip = selfInfo["ip"]
		host.mac = selfInfo["mac"]
		host.name = selfInfo["name"]
		host.ts = timeStamp
		out[selfInfo["ip"]] = host

	return [out[i] for i in out]

def printData(hosts):
	print("ip \t\t mac \t\t\t name \t\t status  OS\t\t time")
	for host in hosts:
		print(host.ip, "\t", host.mac, "\t", host.name, "\t", host.status, "\t", host.OS, "\t", host.ts)


if __name__ == "__main__":
	f = open("output", "r")
	out = formatOutput(f.read())
	f.close()
	printData(out)