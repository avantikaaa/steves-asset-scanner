import sys
from doScan import *
from formatOutput import *
from toCsv import *
from toMongo import *
import application

def main(ip, type, error_popup, ui):
	ui.setTextfunc(text=ui.Status.toPlainText() + "\nScanning")
	if type == 'local':
		doScan(ip)
	elif type == 'remote':
		doScan(ip, 'proxychains')

	f = open("output", "r")
	data = formatOutput(f.read())
	f.close()
	ui.setTextfunc(text=ui.Status.toPlainText() + "\nWriting to CSV file")
	writeToCSV(data)

	f = open("output", "r")
	data = formatOutput(f.read())
	f.close()
	ui.setTextfunc(text=ui.Status.toPlainText() + "\nWriting to CSV file")
	writeToCSV(data)

	ui.setTextfunc(text=ui.Status.toPlainText() + "\nWriting to Database")
	writeToDB(data, ui.error_popup)


if __name__ == '__main__':
	main(sys.argv[1])
