DROP DATABASE IF EXISTS AUC_Catalog;
CREATE DATABASE AUC_Catalog;
use `AUC_Catalog`;
CREATE TABLE Department(
	DeptCode VARCHAR(4) NOT NULL PRIMARY KEY,
    DeptName TEXT NOT NULL
);
#SHOW GLOBAL VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = TRUE;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Department.csv' 
INTO TABLE Department
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY  '\r\n'
IGNORE 1 ROWS;
#SELECT * FROM Department;

CREATE TABLE Course(
	DeptCode VARCHAR(4) NOT NULL,
	CourseNo VARCHAR(4) NOT NULL,
	CourseName TEXT NOT NULL, 
    No_credits INT, 
    Descrip TEXT, 
    notes TEXT,
    PRIMARY KEY (DeptCode, CourseNo),
    FOREIGN KEY (DeptCode) REFERENCES Department (DeptCode)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Course.csv' REPLACE
INTO TABLE Course
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY  '\r\n'
IGNORE 1 ROWS;
#select * from Course;

CREATE TABLE Course_offerings(
	DeptCode VARCHAR(4) NOT NULL,
	CourseNo VARCHAR(4) NOT NULL,
    Semester VARCHAR(10) NOT NULL,
    PRIMARY KEY (DeptCode, CourseNo, Semester),
	CONSTRAINT FOREIGN KEY (DeptCode, CourseNo) REFERENCES Course (DeptCode, CourseNo)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Course_offerings.csv' REPLACE
INTO TABLE Course_offerings
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
#SELECT count(*) FROM Course_offerings;

CREATE TABLE Prerequisite(
	DeptCode VARCHAR(4) NOT NULL,
	CourseNo VARCHAR(4) NOT NULL,
	Concurrent BOOL NOT NULL,
    PrereqDeptCode VARCHAR(4) NOT NULL,
    PrereqCourseNo VARCHAR(4) NOT NULL, 
    PRIMARY KEY (DeptCode, CourseNo, PrereqDeptCode, PrereqCourseNo),
	FOREIGN KEY (DeptCode, CourseNo) REFERENCES Course (DeptCode, CourseNo),
	FOREIGN KEY (PrereqDeptCode, PrereqCourseNo) REFERENCES Course (DeptCode, CourseNo)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Prerequisite.csv' REPLACE
INTO TABLE Prerequisite
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY  '\r\n'
IGNORE 1 ROWS;
#SELECT * FROM Prerequisite;

CREATE TABLE Cross_listed (
	DeptCode VARCHAR(4) NOT NULL,
	CourseNo VARCHAR(4) NOT NULL, 
    CrossDeptCode VARCHAR(4) NOT NULL,
    CrossCourseNo VARCHAR(4) NOT NULL, 
    PRIMARY KEY (DeptCode, CourseNo, CrossDeptCode, CrossCourseNo),
	FOREIGN KEY (DeptCode, CourseNo) REFERENCES Course (DeptCode, CourseNo),
	FOREIGN KEY (CrossDeptCode, CrossCourseNo) REFERENCES Course (DeptCode, CourseNo)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Cross_listed.csv' REPLACE
INTO TABLE Cross_listed
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY  '\r\n'
IGNORE 1 ROWS;
#SELECT * FROM Cross_listed;

CREATE TABLE Student (
	SID VARCHAR(9) NOT NULL PRIMARY KEY,
    FName VARCHAR(12) NOT NULL, 
    MName VARCHAR(12), 
    LName VARCHAR(12) NOT NULL,
    GPA FLOAT NOT NULL,
    standing VARCHAR(10)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Student.csv' 
INTO TABLE Student
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY  '\r\n'
IGNORE 1 ROWS;
#select count(*) from Student;

CREATE TABLE Student_majors(
	SID VARCHAR(9) NOT NULL, 
    DeptCode VARCHAR(4) NOT NULL,
	PRIMARY KEY (SID, DeptCode),
	FOREIGN KEY (DeptCode) REFERENCES Department (DeptCode),
    FOREIGN KEY (SID) REFERENCES Student (SID)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Student_majors.csv' 
INTO TABLE Student_majors
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY  '\r\n'
IGNORE 1 ROWS;
#select count(*) from Student_majors;

CREATE TABLE Courses_finished(
	SID VARCHAR(9) NOT NULL,
    DeptCode VARCHAR(4) NOT NULL,
    CourseNo VARCHAR(4) NOT NULL,
    semester VARCHAR(10) NOT NULL,
    year INT NOT NULL,
    LetterGrade VARCHAR(2), 
    PRIMARY KEY (SID, DeptCode, CourseNo, semester, year),
    FOREIGN KEY (SID) REFERENCES Student (SID),
	FOREIGN KEY (DeptCode, CourseNo) REFERENCES Course (DeptCode, CourseNo)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Courses_finished.csv' REPLACE
INTO TABLE Courses_finished
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY  '\r\n'
IGNORE 1 ROWS;
#select * from Courses_finished;


CREATE TABLE Review (
	SID VARCHAR(9) NOT NULL,
    DeptCode VARCHAR(4) NOT NULL,
    CourseNo VARCHAR(4) NOT NULL,
    rating INT NOT NULL,
    textual_review VARCHAR(500),
	PRIMARY KEY (SID, DeptCode, CourseNo),
    FOREIGN KEY (SID) REFERENCES Student (SID),
	FOREIGN KEY (DeptCode, CourseNo) REFERENCES Course (DeptCode, CourseNo)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Review.csv' REPLACE
INTO TABLE Review
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
#select * from Review;