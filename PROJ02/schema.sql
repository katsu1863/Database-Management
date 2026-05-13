CREATE TABLE Dept (
    dept_code CHAR(4),
    dept_name VARCHAR(50) NOT NULL,
    room_num INT NOT NULL,
    building VARCHAR(50) NOT NULL,

    PRIMARY KEY (dept_code)
);

CREATE TABLE Room (
    room_num INT,
    building VARCHAR(50),
    capacity INT,
    room_type VARCHAR(15),

    PRIMARY KEY (room_num, building),

    CHECK (capacity > 0)
);

CREATE TABLE Course (
    dept_code CHAR(4),
    course_num VARCHAR(5),
    course_name VARCHAR(50) NOT NULL,
    credit INT NOT NULL,

    PRIMARY KEY (dept_code, course_num),

    CHECK (credit >= 1 AND credit <= 6)
);

CREATE TABLE Professor (
    prof_id INT,
    prof_name VARCHAR(50) NOT NULL,
    rank_title VARCHAR(30),
    dept_code CHAR(4) NOT NULL,
    email VARCHAR(50) NOT NULL,

    PRIMARY KEY (prof_id),

    FOREIGN KEY (dept_code) REFERENCES Dept(dept_code)
        ON DELETE RESTRICT
);

CREATE TABLE Section (
    sid INT,
    dept_code CHAR(4),
    course_num VARCHAR(5),
    prof_id INT,
    room_num INT,
    building VARCHAR(50),
    days VARCHAR(7),
    start_time TIME,
    end_time TIME,
    start_day DATE NOT NULL,
    end_day DATE NOT NULL,
    max_enrollment INT,
    current_enrollment INT DEFAULT 0,

    PRIMARY KEY (sid),

    FOREIGN KEY (dept_code, course_num) REFERENCES Course(dept_code, course_num)
        ON DELETE RESTRICT,
    FOREIGN KEY (prof_id) REFERENCES Professor(prof_id)
        ON DELETE CASCADE,
    FOREIGN KEY (room_num, building) REFERENCES Room(room_num, building)
        ON DELETE RESTRICT,

    CHECK (max_enrollment >= 0)
);

INSERT INTO Dept VALUES ('CSCE', 'Computer Science & Computer Engineering', 504, 'JBHT');
INSERT INTO Dept VALUES ('ELEG', 'Electrical Engineering', 3217, 'BELL');
INSERT INTO Dept VALUES ('MEEG', 'Mechanical Engineering', 204, 'MEEG');

INSERT INTO Professor VALUES (123456, 'Susan Gauch', 'Professor', 'CSCE', 'sgauch@uark.edu');
INSERT INTO Professor VALUES (123457, 'John Gauch', 'Professor', 'CSCE', 'jgauch@uark.edu');
INSERT INTO Professor VALUES (222222, 'Yanjun Pan', 'Assistant Professor', 'CSCE', 'yanjunp@uark.edu');
INSERT INTO Professor VALUES (317778, 'Alan Mantooth', 'Distinguished Professor', 'ELEG', 'mantooth@uark.edu');
INSERT INTO Professor VALUES (310101, 'Brajendra Panda', 'Professor', 'CSCE', 'bpanda@uark.edu');
INSERT INTO Professor VALUES (444555, 'Alexander Nelson', 'Associate Professor', 'CSCE', 'ahnelson@uark.edu');
INSERT INTO Professor VALUES (555110, 'Kevin Jin', 'Associate Professor', 'CSCE', 'dongjin@uark.edu');

INSERT INTO Course VALUES ('CSCE', '2004', 'Programming Foundations I', 3);
INSERT INTO Course VALUES ('CSCE', '2114', 'Programming Foundations II', 3);
INSERT INTO Course VALUES ('CSCE', '3193', 'Programming Paradigms', 3);
INSERT INTO Course VALUES ('CSCE', '3193H', 'Honors Programming Paradigms', 3);
INSERT INTO Course VALUES ('CSCE', '4553', 'Information Retrieval Lab', 2);
INSERT INTO Course VALUES ('CSCE', '4263', 'Mobile Programming', 3);
INSERT INTO Course VALUES ('CSCE', '4623', 'Advanced Data Structures', 3);
INSERT INTO Course VALUES ('ELEG', '4188', 'Power Electronics', 3);
INSERT INTO Course VALUES ('CSCE', '4963', 'Capstone II', 3);
INSERT INTO Course VALUES ('CSCE', '5533', 'Advanced Information Retrieval', 3);
INSERT INTO Course VALUES ('CSCE', '4988', 'Embedded Systems Lab', 2);

INSERT INTO Room VALUES (239, 'JBHT', 36, 'Lab');
INSERT INTO Room VALUES (236, 'JBHT', 45, 'Lab');
INSERT INTO Room VALUES (147, 'JBHT', 140, 'Classroom');
INSERT INTO Room VALUES (216, 'JBHT', 170, 'Classroom');
INSERT INTO Room VALUES (2269, 'BELL', 70, 'Conference');
INSERT INTO Room VALUES (2286, 'BELL', 100, 'Classroom');
INSERT INTO Room VALUES (225, 'MEEG', 70, 'Classroom');

INSERT INTO Section VALUES (9597, 'CSCE', '2004', 222222, 2269, 'BELL', 'MWF', '15:05:00', '15:55:00', '2023-08-21', '2023-12-07', 70, 0);
INSERT INTO Section VALUES (1449, 'CSCE', '2114', 123457, 216, 'JBHT', 'MWF', '12:55:00', '13:45:00', '2023-08-21', '2023-12-07', 138, 0);
INSERT INTO Section VALUES (2930, 'CSCE', '3193', 222222, 216, 'JBHT', 'TR', '15:30:00', '16:45:00', '2023-08-21', '2023-12-07', 140, 0);
INSERT INTO Section VALUES (4636, 'CSCE', '3193H', 222222, 216, 'JBHT',	'TR', '15:30:00', '16:45:00', '2023-08-21',	'2023-12-07', 30, 0);
INSERT INTO Section VALUES (11957, 'CSCE', '4263', 555110, 239, 'JBHT', 'TR', '8:00:00', '9:15:00', '2023-08-21', '2023-12-07', 0, 0);
INSERT INTO Section VALUES (12550, 'CSCE', '4553', 123456, 239, 'JBHT',	'MWF', '9:40:00', '10:30:00', '2023-08-21', '2023-12-07', 30, 0);
INSERT INTO Section VALUES (6704, 'CSCE', '4623', 444555, 2286, 'BELL',	'MWF', '10:45:00', '11:35:00', '2023-08-21', '2023-12-07', 65, 0);
INSERT INTO Section VALUES (6325, 'CSCE', '4963', 444555, 147, 'JBHT', 'MWF', '15:05:00', '15:55:00', '2023-08-21', '2023-12-07', 50, 0);
INSERT INTO Section VALUES (11944, 'CSCE', '5533', 123456, 239, 'JBHT',	'MWF', '15:05:00', '15:55:00', '2023-08-21', '2023-12-07', 30, 0);