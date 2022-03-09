import csv

def remove_csv_linebreak(old_csv, new_csv):
    with open(old_csv, 'r') as csvfile, open(new_csv, 'w', newline='') as newcsv:
        reader = csv.reader(csvfile)
        writer = csv.writer(newcsv)
        for row in reader:
            for index, value in enumerate(row):
                if '\r\n' in value:
                    row[index] = row[index].replace('\r\n', ' ')
                if '\n' in value:
                    row[index] = row[index].replace('\n', '')
            writer.writerow(row)