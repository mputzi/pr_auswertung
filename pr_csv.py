import csv

class MyCSV():
    def __init__(self, filename="test.csv"):
        self.filename = filename
        
    def write(self, data_list):
        print("Schreibe in CSV")
        
        with open(self.filename, mode='w') as csv_file:
            fieldnames = ['Nachname', 'Vorname', 'Gruppe']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            try:
                writer.writeheader()
            except:
                print("Fehler beim Schreiben des Headers")
                return False
            
            try:
                for element in data_list:
                    d = element.getDict()
                    writer.writerow(d)
            except:
                print("Fehler beim Schreiben")
                return False
        
        return True
        
    def read(self):
        print("Lese von CSV")
        
        list_of_dicts = list()
        columns = list()
        
        with open(self.filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            
            for row in csv_reader:
                if line_count == 0:
                    #print(f'Column names are {", ".join(row)}')
                    columns = list(dict(row).keys())
                    #print(columns)
                else:
                    pass
                
                print(f'\t{row[columns[1]]} {row[columns[0]]} ist in Gruppe {row[columns[2]]}.')
                list_of_dicts.append(dict(row))
                line_count += 1
        print(f'Processed {line_count} lines.')
        
        #dict = {"Vorname" : "Hans", "Nachname": "Dampf", "Gruppe": "1"}
        return list_of_dicts
