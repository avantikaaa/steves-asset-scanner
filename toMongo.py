import pymongo
from Host import *

def writeToDB(hosts, error_popup):
	try:
		myclient = pymongo.MongoClient("mongodb+srv://<username>:<password>@todo.348ky.mongodb.net/flipkart?retryWrites=true&w=majority")
		mydb = myclient["<database_name>"]

		mycol = mydb["<table_name>"]

		cursor = mycol.find({})
		for document in cursor:
			mycol.update_one({"_id": document["_id"]}, {"$set": {"status": "down"}})

		fields = ["serial_no", "IP", "MAC", "Name", "Domain info", "OS", "Workgroup", "Status"]

		hosts.sort(key=lambda host: host.ip)
		for i in range(1, len(hosts) + 1):
			mycol.update_one({"_id": hosts[i - 1].mac}, {
				"$set": {"_id": hosts[i - 1].mac, "IP": hosts[i - 1].ip, "MAC": hosts[i - 1].mac, "Name": hosts[i - 1].name,
						"Domain": hosts[i - 1].domain, "OS": hosts[i - 1].OS, "Workgroup": hosts[i - 1].workgroup,
						"status": hosts[i - 1].status, "time stamp": hosts[i - 1].ts}}, upsert=True)

	except Exception as e:
		print("Error occured in connecting to db", e)
		error_popup.setText("Can't connect to DB")
		error_popup.exec_()
