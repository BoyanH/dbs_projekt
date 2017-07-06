import csv
from Contract import Contract
import os

def cleanData():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	filepath = Contract.CSV_INITIAL
	explicitPathRead = os.path.join(dir_path, filepath)
	explicitPathWrite = os.path.join(dir_path, Contract.CSV_CLEAN)

	csvfile = open(explicitPathRead, "r", encoding="cp1252")
	csv_filewrite = open(explicitPathWrite, "w+", encoding="cp1252")

	csv_reader = csv.DictReader(csvfile, delimiter=";", quotechar='"')
	csv_writer = csv.DictWriter(csv_filewrite, fieldnames=csv_reader.fieldnames,  delimiter=';', quotechar='"')

	csv_writer.writeheader()
	for row in csv_reader:
	    if not (row['truncated'] == 'True' or u"\u2026" in row['text']):
	        csv_writer.writerow(row)
