# Name: Shirley Lin
# Date: 2/2/26
# Assignment: Homework 1 - Part 2

import csv
import os.path

class DB:

    # Default constructor
    def __init__(self):
        self.num_records = -1
        self.record_size = -1
        self.data_filestream = None
        self.config_filename = None

    # Open the database
    def open(self, filename):
        data_filename = filename + ".data"
        self.config_filename = filename + ".config"
        
        # Check that the data and config files for the database exist
        if not os.path.isfile(data_filename) or not os.path.isfile(self.config_filename):
            return False
        else:
            self.data_filestream = open(data_filename, 'r+')

            # Parse the config file to set numRecords and recordSize
            with open(self.config_filename, 'r') as config_file:
                for line in config_file:
                    key, value = line.split("=")

                    if key == "numRecords":
                        self.num_records = int(value)
                    elif key == "recordSize":
                        self.record_size = int(value)
            config_file.close()

            return True

    # Close the database
    def close(self):
        self.data_filestream.close()

        # Save the variables in the config file
        with open(self.config_filename, 'w') as config_file:
            config_file.write(f"numRecords={self.num_records}\n")
            config_file.write(f"recordSize={self.record_size}\n")
        config_file.close()

        # Reset the member variables
        self.num_records = -1
        self.record_size = -1
        self.sorted_records = -1
        self.unsorted_records = -1
        self.data_filestream = None
        self.config_filestream = None

        print("\nThe current database has been closed.")


    # Check if a database is open
    def isOpen(self):
        if self.data_filestream:
            return True
        return False

    # Read the specified record from the database
    def readRecord(self, record_num, name, rank, city, state, zip, employees):
        if 0 <= record_num < self.num_records:
            self.data_filestream.seek(record_num * self.record_size)
            line = self.data_filestream.readline().rstrip('\n')
            name[0] = line[:40].strip()
            rank[0] = line[40:45].strip()
            city[0] = line[45:65].strip()
            state[0] = line[65:70].strip()
            zip[0] = line[70:80].strip()
            employees[0] = line[80:90].strip()

            # Check if the record has been deleted
            if rank[0] == "" and city[0] == "" and state[0] == "" and zip[0] == "" and employees[0] == "":
                return False
            
            return True
            
        return False
    
    # Writes a fixed length record to the given file location
    def writeRecord(self, filestream, name, rank, city, state, zip, employees):
        try:
            filestream.write("{:40.40}".format(name))
            filestream.write("{:5.5}".format(rank))
            filestream.write("{:20.20}".format(city))
            filestream.write("{:5.5}".format(state))
            filestream.write("{:10.10}".format(zip))
            filestream.write("{:10.10}".format(employees))
            filestream.write("\n")
            return True
        except IOError:
            return False
        
    def binarySearch(self, name, rank, city, state, zip, employees):

        low = 0
        high = self.num_records - 1

        target_name = name[0]  # Do not strip leading zeros

        while high >= low:
            middle = (low + high) // 2
            temp_name = [None]  # Use a list to hold the ID read from the record
            if not self.readRecord(middle, temp_name, rank, city, state, zip, employees):
                return -1

            mid_name = temp_name[0]  # Do not strip leading zeros

            if mid_name == target_name:
                return middle
            elif mid_name < target_name:
                low = middle + 1
            else:
                high = middle - 1

        return -1

    # Uses binary search to find the record number of the corresponding primary key
    # Returns -1 if the record could not be found
    def findRecord(self, name, rank, city, state, zip, employees):
        record_num = self.binarySearch(name, rank, city, state, zip, employees)

        return record_num 

    # Update a specified field of a record given its corresponding primary key
    def updateRecord(self, name, rank, city, state, zip, employees):
        # Find the record and display it
        record_num = self.findRecord(name, rank, city, state, zip, employees)
        
        if record_num != -1:
            print(f"Record {record_num}, Name: {name[0]:<40} Rank: {rank[0]:<5} City: {city[0]:<20} State: {state[0]:<5} Zip: {zip[0]:<10} Employee: {employees[0]:<10}")

            # Prompt user for the field they want to update
            field_name = (input("Enter the field you want to update: ")).lower()
            new_value = input("Enter the new value: ")

            if field_name == "name":
                print("The primary key of a record cannot be updated.")
                return False
            elif field_name == "rank":
                rank[0] = new_value
            elif field_name == "city":
                city[0] = new_value
            elif field_name == "state":
                state[0] = new_value
            elif field_name == "zip":
                zip[0] = new_value
            elif field_name == "employees":
                employees[0] = new_value
            else:
                print("Invalid field name.")
                return False
            
            # Calculate byte offset & move the cursor to the beginning of the specific record
            offset = record_num * self.record_size
            self.data_filestream.seek(offset)
            
            # Update the corresponding field with writeRecord
            # Note that the name of a record cannot be modified
            if self.writeRecord(self.data_filestream, name[0], rank[0], city[0], state[0], zip[0], employees[0]):
                print(f"The {field_name} field of record {record_num} was successfully updated.")
                return True
        
        return False

    def deleteRecord(self, name):
        record_num = self.findRecord(name, [""], [""], [""], [""], [""])

        if record_num != -1:
            # Calculate byte offset & move cursor to the beginning of the specific record
            offset = record_num * self.record_size
            self.data_filestream.seek(offset)

            # Use writeRecord to fill all fields except name with empty values
            if self.writeRecord(self.data_filestream, name[0], "", "", "", "", ""):
                print("Record was successfully deleted.")
                return True
        
        return False