from flask import Flask, request, url_for, redirect, render_template
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)
#app.config["MYSQL_USER"] = 'root'
#app.config["MYSQL_PASSWORD"] = "M01272238355a@#"
#app.config["MYSQL_HOST"] = 'localhost'
#app.config["MYSQL_DB"] = 'auc_catalog'
# app.config["MYSQL_USER"] = 'sql2379159'
# app.config["MYSQL_PASSWORD"] = "nI5*rP4%"
# app.config["MYSQL_HOST"] = 'sql2.freemysqlhosting.net'
# app.config["MYSQL_DB"] = 'sql2379159'
app.config["MYSQL_USER"] = '3wjzHnMcEN'
app.config["MYSQL_PASSWORD"] = "g3BIgloqWm"
app.config["MYSQL_HOST"] = 'remotemysql.com'
app.config["MYSQL_DB"] = '3wjzHnMcEN'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/Courses', methods=['POST', 'GET'])
def Courses():
    if request.method == "POST":
        deptCode = request.form["DeptCode"]
        courseNo = request.form["CourseNo"]
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM Course WHERE DeptCode = %s AND CourseNo = %s", (deptCode, courseNo))
            resultCourse = cur.fetchall()
            if len(resultCourse) > 0:
                message = render_template("CourseInfo.html", DeptCode=deptCode, CourseNo=courseNo, CourseInfo=resultCourse)
            else:
                message = "No Course Exists with these keys"
        except Exception as e:
            mysql.connection.rollback()
            message = "Failure to view the course<br>Problem Description: "+str(e)
        finally:
            cur.close()
            return message
    else:
        return render_template("Courses.html")


@app.route("/Courses/Reviews/<DeptCode>_<CourseNo>", methods=["POST", "GET"])
def ShowReviews(DeptCode, CourseNo):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT rating, textual_review FROM Review WHERE DeptCode = "
                    "%s AND CourseNo = %s", (DeptCode, CourseNo))
        reviews = cur.fetchall()
        if len(reviews) > 0:
            message = render_template("DisplayReviews.html", reviews=reviews)
            # redirect(url_for("CourseInfo", deptCode=deptCode, courseNo=courseNo, rest=resultCourse))
        else:
            message = "<tr>No Review Exists for this Course</tr>"
    except Exception as e:
        mysql.connection.rollback()
        message = "Failure to view the reviews<br>Problem Description: " + str(e)
    finally:
        cur.close()
        return message


@app.route("/SID_<sid>/<semester>_courses", methods=["POST", "GET"])
def ShowAvailableCourses(sid, semester):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT K.DeptCode, K.CourseNo, CourseName, No_credits FROM Course_offerings AS O JOIN (SELECT C.DeptCode, C.CourseNo, CourseName, No_credits FROM Course AS C LEFT JOIN Prerequisite AS P ON C.DeptCode = P.DeptCode AND C.CourseNo = P.CourseNo JOIN Courses_finished AS F ON P.PrereqDeptCode = F.DeptCode AND P.PrereqCourseNo = F.CourseNo WHERE SID = %s AND LetterGrade != 'D' AND LetterGrade != 'F' UNION SELECT C.DeptCode, C.CourseNo, CourseName, No_credits FROM Course AS C LEFT JOIN Prerequisite AS P ON C.DeptCode = P.DeptCode AND C.CourseNo = P.CourseNo WHERE PrereqDeptCode IS NULL OR PrereqCourseNo IS NULL) AS K ON O.DeptCode = K.DeptCode AND O.CourseNo = K.CourseNo WHERE Semester = %s OR Semester IS NULL", (sid, semester))
        courses = cur.fetchall()
        if len(courses) > 0:
            message = render_template("DisplayAvailableCourses.html", Courses=courses)
        else:
            message = "<tr>No Available Courses to take at the moment</tr>"
    except Exception as e:
        mysql.connection.rollback()
        message = "Failure to view the courses<br>Problem Description: " + str(e)
    finally:
        cur.close()
        return message


@app.route('/StudentLogin', methods=["POST", "GET"])
def StudentLogin():
    if request.method == "POST":
        new_sid = request.form["id"]
        return redirect(url_for('Student', sid=new_sid))
    else:
        return render_template("StudentLogin.html")


@app.route('/<sid>', methods=["GET", "POST"])
def Student(sid):
    if request.method == "POST":
        semester = request.form["semester"]
        return redirect(url_for("ShowAvailableCourses", semester=semester, sid=sid))
    else:
        return render_template("Student.html", sid=sid)


@app.route("/<sid>/addReview", methods = ["POST", "GET"])
def addReview(sid):
    if(request.method == "POST"):
        deptCode = request.form["DeptCode"]
        CourseNo = request.form["CourseNo"]
        rating = request.form["rating"]
        textual_review = request.form["textual_review"]
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO Review VALUES (%s, %s, %s, %s, %s)", (sid, deptCode, CourseNo, rating, textual_review))
            mysql.connection.commit()
            message = "Review Added successfully"
        except Exception as e:
            mysql.connection.rollback()
            message = "Failure to add the review\nProblem Description: "+str(e)
        finally:
            cur.close()
            return message
    else:
        return render_template("addReview.html")


@app.route("/Administration/add_student", methods = ["POST", "GET"])
def addStudent():
    if(request.method == "POST"):
        SID = request.form["SID"]
        FName = request.form["FName"]
        MName = request.form["MName"]
        LName = request.form["LName"]
        GPA = request.form["GPA"]
        standing = request.form["standing"]
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO Student VALUES (%s, %s, %s, %s, %s, %s)", (SID, FName, MName, LName, GPA, standing))
            mysql.connection.commit()
            message = "Student Added successfully"
        except Exception as e:
            mysql.connection.rollback()
            message = "Failure to add the student<br>Problem Description: "+str(e)
        finally:
            cur.close()
            return message
    else:
        return render_template("addStudent.html")


@app.route('/<sid>/add_finished_course', methods = ["POST", "GET"])
def AddFinishedCourse(sid):
    if (request.method == "POST"):
        DeptCode = request.form["DeptCode"]
        CourseNo = request.form["CourseNo"]
        semester = request.form["semester"]
        year = request.form["year"]
        LetterGrade = request.form["letter"]
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO Courses_finished VALUES (%s, %s, %s, %s, %s, %s)",
                        (sid, DeptCode, CourseNo, semester, year, LetterGrade))
            mysql.connection.commit()
            message = "Course Added  to your course history"
        except Exception as e:
            mysql.connection.rollback()
            message = "Failure to add the course<br>Problem Description: " + str(e)
        finally:
            cur.close()
            return message
    else:
        return render_template("addFinishedCourse.html")


@app.route('/Administration')
def Administration():
    return render_template("Administration.html")


@app.route('/viewCourseInfo')
def viewCourseInfo():
    return render_template("CourseInfo.html")


if __name__ == "__main__":
    app.run(debug=True)
