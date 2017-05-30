import csv

filepath = "american-election-tweets.csv"

csvfile = open(filepath, "r", encoding="cp1252")
csv_filewrite = open("test.csv", "w", encoding="cp1252")

csv_reader = csv.DictReader(csvfile, delimiter=";", quotechar='"')
csv_writer = csv.DictWriter(csv_filewrite, fieldnames=csv_reader.fieldnames,  delimiter=';', quotechar='"')

csv_writer.writeheader()
for row in csv_reader:
    if not (row['truncated'] == 'True' or u"\u2026" in row['text']):
        #print(row['text'])
        csv_writer.writerow(row)
    else:
        print(row['text'])


