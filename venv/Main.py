#Imports
import csv
import random
import sqlite3
import pandas as pd
#coded by Duncan Harris
name = ["James", "Mary", "Robert", "John", "Linda", "Diane", "Diana", "Charles", "Charlie", "Beth", "Robin"
        ,"Gabriel", "Arthur", "Daniel", "Alexa", "Abbigial", "Seth", "Bob", "Karl", "Carl"]
surname = ["South", "North", "East", "West", "Jackson", "Martin", "Perez", "Tony", "Antonio", "Wilson"
           ,"Lee", "Smith", "Harris", "Johnson", "Porter", "Thompson", "Sanchez", "Clarkson", "Benson", "Tom"]
def createCSV(value):
        f = open('withDups.csv', 'w', newline="")
        writer = csv.writer(f)
        writer.writerow(['id', 'Name', 'Surname', 'Initial', 'Age', 'DateOfBirth'])

        i = 1
        while i < value:
            rn = random.choice(name)
            rs = random.choice(surname)
            day = random.randint(1, 31)
            month= random.randint(1, 12)
            year = random.randint(1900, 2020)
            date= str(day)+"/"+str(month)+"/"+str(year)
            initial = rn[0]+rs[0]
            writer.writerow([i, rn, rs, initial, random.randint(1, 100), date])
            i = i + 1
        print(str(i)+" Records inserted")    

def removeDuplicates():
    with open('withDups.csv', 'r') as in_file, open('output.csv', 'w') as out_file:

        seen = set()  

        for line in in_file:
            if line in seen:
                continue  

            seen.add(line)
            out_file.write(line)

def uploadToDatabase():
    conn = sqlite3.connect('Devprox_db')
    curs = conn.cursor()

    curs.execute('DROP TABLE IF EXISTS csv_import')
    curs.execute('''
    CREATE TABLE "csv_import"(
        "id" TEXT,
        "name" TEXT,
        "surname" TEXT,
        "initial" TEXT,
        "age" INT,
        "DateOfBirth" TEXT
    )
    ''')

    fileName = "output.csv"

    with open(fileName) as csv_f:
        reader = csv.reader(csv_f, delimiter=',')
        for row in reader:
            id =row[0]
            name =row[1]
            surname =row[2]
            initial =row[3]
            age =row[4]
            DateOfBirth =row[5]
            curs.execute('''INSERT INTO csv_import(id,name,surname,initial,age,DateOfBirth)
            VALUES (?,?,?,?,?,?)''', (id, name, surname, initial, age, DateOfBirth))
            conn.commit()

input = input("Enter amount of CVS entries: ");
value = int(input)
createCSV(value)
removeDuplicates()
print("duplicates Removed")
uploadToDatabase()
print("Database Created")

