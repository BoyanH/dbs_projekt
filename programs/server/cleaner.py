import csv
from Contract import Contract
import os

def cleanData():
	filepath = Contract.CSV_INITIAL
	root_dir = os.path.dirname(os.getcwd())
	explicitPathRead = os.path.join(root_dir, filepath)
	explicitPathWrite = os.path.join(root_dir, Contract.CSV_CLEAN)

	csvfile = open(explicitPath, "r", encoding="cp1252")
	csv_filewrite = open(explicitPathWrite, "w+", encoding="cp1252")

	csv_reader = csv.DictReader(csvfile, delimiter=";", quotechar='"')
	csv_writer = csv.DictWriter(csv_filewrite, fieldnames=csv_reader.fieldnames,  delimiter=';', quotechar='"')

	csv_writer.writeheader()
	for row in csv_reader:
	    if not (row['truncated'] == 'True' or u"\u2026" in row['text']):
	        csv_writer.writerow(row)
