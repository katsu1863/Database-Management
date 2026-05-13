from database import Database

def findProfessor(db):
    query = "SELECT * FROM Dept;"
    db.executeSelect(query)
    dept = input("Enter department code: ")

    if db.departmentExists(dept):
        # Display all professors from a department
        query = f"SELECT * FROM Professor WHERE dept_code = '{dept}';"
        db.executeSelect(query)

def findSection(db):
    print("\n1) Display all sections")
    print("2) Display all sections by department")
    print("3) Display all sections by course level")
    choice = input("Enter an option: ")

    query = '''SELECT dept_code, course_num, building, room_num, days, start_time, end_time,
            (max_enrollment - current_enrollment) AS seats_available
            FROM Section'''

    if choice == '1':
        db.executeSelect(query + ";")
    elif choice == '2':
        dept = input("Enter department code: ")

        if db.departmentExists(dept):
            db.executeSelect(query + f" WHERE dept_code = '{dept}';")
    elif choice == '3':
        allowedValues = {'1000', '2000', '3000', '4000', '5000'}
        level = input("Enter course level: ")

        if level not in allowedValues:
            print(f"ERROR: {level} is not a valid course level.")
        else:
            level = level[0] # Truncate last 3 characters in course level
            db.executeSelect(query + f" WHERE course_num LIKE '{level}%';")
    else:
        print("ERROR: Invalid input.")

def addSection(db):
    query = "SELECT * FROM Course;"
    db.executeSelect(query)

    deptCode = input("Enter department code: ")
    courseNum = input("Enter course number: ")

    if db.courseExists(deptCode, courseNum):
        print("\nEnter NULL for fields with no value.")
        profId = input("Enter professor ID: ")
        roomNum = input("Enter room number: ")
        building = input("Enter building: ")
        days = input("Enter days: ")
        startTime = input("Enter start time: ")
        endTime = input("Enter end time: ")
        maxEnrollment = input("Enter max enrollment: ")
        currentEnrollment = input("Enter current enrollment: ")
        
        if db.validateProf(profId) and db.validateRoom(roomNum, building):
            if not db.roomAvailable(roomNum, building, days, startTime, endTime):
                print("ERROR: That room is already booked by another section at that time.")
                return
            
            sid = db.getSidMax() + 1 # Generate a unique section ID by incrementing the highest one
            values = f"{sid}, '{deptCode}', '{courseNum}', {profId}, {roomNum}, '{building}', '{days}', '{startTime}', '{endTime}', '2023-08-21', '2023-12-07', {maxEnrollment}, {currentEnrollment}"
            db.insert("Section", values)
            print(f"A new section for {deptCode} {courseNum} was successfully added.")

def updateSection(db):
    deptCode = input("\nEnter department code: ")
    courseNum = input("Enter course number: ")
    
    query = f"SELECT * FROM Section WHERE dept_code = '{deptCode}' AND course_num = '{courseNum}';"
    db.executeSelect(query)

    sid = input("Enter the SID of the section you want to update: ")
    if db.sectionExists(sid):
        field = input("Enter the field you want to update: ")
        newVal = input("Enter the new value: ")

        allowedValues = {"dept_code", "course_num", "prof_id", "room_num", "building", "days", "start_time", "end_time", "start_day", "end_day", "max_enrollment", "current_enrollment"}
        if field == "sid":
            print("ERROR: Primary key cannot be altered.")
            return
        elif field not in allowedValues:
            print("ERROR: Input is an invalid field.")
            return
        
        query = f"UPDATE Section SET {field} = {newVal} WHERE sid = {sid};"
        db.executeUpdate(query)
        print(f"Section {sid} was successfully updated.")

def reportEnrollments(db):
    query = '''SELECT d.dept_code, SUM(s.current_enrollment) AS total_enrollments
            FROM Dept d LEFT JOIN Section s ON d.dept_code = s.dept_code
            GROUP BY d.dept_code;'''
    db.executeSelect(query)

def findAvailableRooms(db):
    building = input("Enter building: ")
    roomType = input("Enter room type: ")
    minCapacity = input("Enter minimum capacity: ")
    days = input("Enter days: ")
    startTime = input("Enter start time: ")
    endTime = input("Enter end time: ")
    
    rooms = db.getRooms(building, roomType, minCapacity)
    if not rooms:
        print(f"ERROR: There are no rooms in {building} that are of type {roomType} and have a capacity of at least {minCapacity}.")
        return

    availableRooms = []

    # Filter through rooms that meet the requirements to see if they're available
    for room in rooms:
        roomNum = room[0]
        if db.roomAvailable(roomNum, building, days, startTime, endTime):
            availableRooms.append(room)

    if not availableRooms:
        print(f"ERROR: There are rooms that match the criteria, but they are currently booked by another section.")
        return

    # Print available rooms
    headers = ["room_num", "building", "capacity", "room_type"]
    db.printFormat(availableRooms, headers)

if __name__ == "__main__":
    mysql_username = 'shirleyl'
    mysql_password = 'ahjael7B'
    db = Database('localhost', mysql_username, mysql_password, mysql_username)

    run = True
    while run:
        print("\n1) Find Professors")
        print("2) Find Sections")
        print("3) Add Section")
        print("4) Update Section")
        print("5) Report Enrollments")
        print("6) Available Rooms")
        print("7) Quit")
        choice = input("Enter an option: ")

        if choice == '1':
            findProfessor(db)
        elif choice == '2':
            findSection(db)
        elif choice == '3':
            addSection(db)
        elif choice == '4':
            updateSection(db)
        elif choice == '5':
            reportEnrollments(db)
        elif choice == '6':
            findAvailableRooms(db)
        elif choice == '7':
            print("Quitting program...")
            run = False
        else:
            print("ERROR: Invalid input.")

    db.close_db()