import mysql.connector
from tabulate import tabulate

class Database:
    def __init__(self, hostname, user_name, mysql_pw, database_name):
        self.conn = mysql.connector.connect (
            host = hostname,
            user = user_name,
            password = mysql_pw,
            database = database_name
        )
        self.cursor = self.conn.cursor()

    # Allows for manual input of headers
    # If no headers are passed in, assume corresponding query was executed beforehand
    def printFormat(self, result, header=None):
        if header is None:
            header = []
            for cd in self.cursor.description: # Get headers
                header.append(cd[0])

        print('')
        print('Query Result:')
        print('')
        print(tabulate(result, headers=header)) # Print results in table format
        print('')

    def executeSelect(self, query):
        self.cursor.execute(query)
        self.printFormat(self.cursor.fetchall())

    def insert(self, table, values):
        query = "INSERT into " + table + " values (" + values + ")" + ';'
        self.cursor.execute(query)
        self.conn.commit()

    def executeUpdate(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def close_db(self):
        self.cursor.close()
        self.conn.close()

# ---------- Helper Methods ----------
    def getSidMax(self):
        query = "SELECT MAX(sid) FROM Section;"
        self.cursor.execute(query)
        
        return self.cursor.fetchone()[0]
    
    def getRooms(self, building, roomType, minCapacity):
        query = f'''SELECT * FROM Room WHERE building = '{building}'
                AND room_type = '{roomType}'
                AND capacity >= {minCapacity};'''
        self.cursor.execute(query)
       
        return self.cursor.fetchall() # Returns list of all the rooms that meet the requirements

# ---------- Error Checking Methods ----------
    def departmentExists(self, dept):
        query = f"SELECT * FROM Dept WHERE dept_code = '{dept}';"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        if not result:
            print(f"ERROR: Department {dept} does not exist.")
            return False
        
        return True
    
    def courseExists(self, deptCode, courseNum):
        query = f"SELECT * FROM Course WHERE dept_code = '{deptCode}' AND course_num = '{courseNum}';"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        if not result:
            print(f"ERROR: Course {deptCode} {courseNum} does not exist.")
            return False
        
        return True
    
    def sectionExists(self, sid):
        query = f"SELECT * FROM Section WHERE sid = {sid};"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        if not result:
            print(f"ERROR: Section {sid} does not exist.")
            return False
        
        return True
    
    def validateProf(self, profId):
        query = f"SELECT * FROM Professor WHERE prof_id = {profId};"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if profId == "NULL":
            print("ERROR: Professor ID cannot be NULL.")
            return False
        elif result is None:
            print(f"ERROR: Professor ID {profId} does not exist.")
            return False
        
        return True
        
    def validateRoom(self, roomNum, building):
        query = f"SELECT * FROM Room WHERE room_num = {roomNum} AND building = '{building}';"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if roomNum == "NULL":
            print("ERROR: Room number cannot be NULL.")
            return False
        elif building == "NULL":
            print("ERROR: Building cannot be NULL.")
            return False
        elif result is None:
            print(f"ERROR: Room {building} {roomNum} does not exist.")
            return False
        
        return True
    
    def roomAvailable(self, roomNum, building, days, startTime, endTime):
        query = f'''SELECT * FROM Section WHERE room_num = {roomNum}
                AND building = '{building}'
                AND days = '{days}'
                AND (start_time < '{endTime}' AND end_time > '{startTime}');'''
        self.cursor.execute(query) # Find sections that overlap with specified timeframe
        result = self.cursor.fetchone()

        if result is not None:
            return False
        
        return True