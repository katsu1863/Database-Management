# Name: Shirley Lin
# Date: 2/2/26
# Assignment: Homework 1 - Part 2

import csv
import os.path
from Database import DB

def createDatabase(db):
    # Prompt user to enter a filename
    # Creates a corresponding .data and .config for the database
    filename = input("\nEnter the filename without the extension: ")

    # Generate filenames
    csv_filename = filename + ".csv"
    data_filename = filename + ".data"
    config_filename = filename + ".config"

    # Check that filename exists
    if not os.path.isfile(csv_filename):
        print(csv_filename + " not found.")
    else:
        num_records = 0

        # Read CSV file by line and write into data file
        with open(csv_filename, "r") as csv_file, open(data_filename, "w") as data_file:
            for line in csv_file:
                csv_reader = csv.reader([line])
                row = next(csv_reader)
                db.writeRecord(data_file, row[0], row[1], row[2], row[3], row[4], row[5])
                num_records += 1
        csv_file.close()
        data_file.close()

        # Create config file
        with open(config_filename, "w") as config_file:
            config_file.write(f"numRecords={num_records}\n")
            config_file.write(f"recordSize=91\n")

        print(f"{filename} database successfully created with {num_records} records.")

def openDatabase(db):
    # Prompt user to enter database name & open the database
    filename = input("\nEnter the name of the database: ")
    if db.open(filename):
        print(f"{filename} database was successfully opened.")
    else:
        print(f"{filename} database could not be opened. Check that the database has a corresponding .data and .config file.")


def displayRecord(db, name, rank, city, state, zip, employees):
    name[0] = input("\nEnter the primary key of the record you want to display: ")

    record_num = db.findRecord(name, rank, city, state, zip, employees)

    # Display the record or an error message if the record could not be found
    if record_num == -1:
        print("Could not find the corresponding record.")
    else:
        print(f"Record {record_num}, Name: {name[0]:<40} Rank: {rank[0]:<5} City: {city[0]:<20} State: {state[0]:<5} Zip: {zip[0]:<10} Employee: {employees[0]:<10}")

def printReport(db, name, rank, city, state, zip, employees):
    # Display the first 10 records
    record_num = 0
    counter = 0
    while counter < 10:
        if db.readRecord(record_num, name, rank, city, state, zip, employees):
            print(f"Record {record_num}, Name: {name[0]:<40} Rank: {rank[0]:<5} City: {city[0]:<20} State: {state[0]:<5} Zip: {zip[0]:<10} Employee: {employees[0]:<10}")
            counter += 1
        record_num += 1
    
    print("\nReport has been successfully printed.")

def requiresOpen(db):
    if not db.isOpen():
        print("\nThere is not a database open.")
        return False
    
    return True

def main():
    database = DB()
    run = True

    # Declare variables that will temporarily store the values of a record
    name = [""]
    rank = [""]
    city = [""]
    state = [""]
    zip = [""]
    employees = [""]

    # Continue to prompt the user until they quit out of the program
    while run:
        # Print the menu of operations
        print("\t1) Create database")
        print("\t2) Open database")
        print("\t3) Close database")
        print("\t4) Display record")
        print("\t5) Update Record")
        print("\t6) Print report to the screen")
        print("\t7) Delete record")
        print("\t8) Quit program")
        
        # Receive user input and execute the corresponding operation
        choice = input("Enter the operation you would like to perform: ")

        if choice == '1':
            createDatabase(database)
        elif choice == '2':
            if not database.isOpen():
                openDatabase(database)
            else:
                print("\nA database is already open. Close the current database and try again.")
        elif choice == '3':
            if requiresOpen(database):
                database.close()
        elif choice == '4':
            if requiresOpen(database):
                displayRecord(database, name, rank, city, state, zip, employees)
        elif choice == '5':
            if requiresOpen(database):
                # Prompt user for primary key
                name[0] = input("\nEnter the primary key of the record you want to update: ")

                if not database.updateRecord(name, rank, city, state, zip, employees):
                    print("\nCould not update record.")
        elif choice == '6':
            if requiresOpen(database):
                printReport(database, name, rank, city, state, zip, employees)
        elif choice == '7':
            if requiresOpen(database):
                # Prompt user for primary key
                name[0] = input("\nEnter the primary key of the record you want to delete: ")

                if not database.deleteRecord(name):
                    print("\nCould not delete record.")
        elif choice == '8':
            if not database.isOpen():
                print("Closing program...")
                run = False
            else:
                print("\nClose the current database before quitting the program.")
        else:
            print("\nInvalid input. Try again.")

if __name__ == "__main__":
    main()