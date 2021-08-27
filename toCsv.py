from Host import *
import csv
import os.path

def writeToCSV(hosts):
	# write to all_scans
	fields = ["serial_no","IP", "MAC", "Name", "Domain info", "OS","Workgroup","Status", "time stamp"]

	with open("current_scan.csv", 'w') as csvfile: 
		# creating a csv writer object 
		csvwriter = csv.writer(csvfile) 
			
		# writing the fields 
		csvwriter.writerow(fields) 
		hosts.sort(key=lambda host: host.ip)
		# writing the data rows 
		for host in hosts:
			csvwriter.writerow([101 , host.ip, host.mac, host.name, host.domain, host.OS,  host.workgroup, host.status, host.ts])


