import csv

filepath = "test.csv"
csvfile = open(filepath, "r", encoding="cp1252")
csv_reader = csv.DictReader(csvfile, delimiter=";", quotechar='"')

def parseTweet(entry):
    pass

for row in csv_reader:
    parseTweet(row)


