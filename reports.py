import sqlite3

import sqlite3


class Cohort():

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name} is an active cohort'

class Exercises():

    def __init__(self, name, language):
        self.name = name
        self.language = language

    def __repr__(self):
        return f'{self.name} is an exercise written in {self.language} language'

class Instructor():

    def __init__(self, first, last, slack, cohort, specialty):
        self.first = first
        self.last = last
        self.slack = slack
        self.cohort = cohort
        self.specialty = specialty

    def __repr__(self):
        return f'{self.first} {self.last} instructs {self.cohort}, and {self.specialty} is the specialty'

class Student():

    def __init__(self, first, last, handle, cohort):
        self.first_name = first
        self.last_name = last
        self.slack_handle = handle
        self.cohort = cohort

    def __repr__(self):
        return f'{self.first_name} {self.last_name} is in {self.cohort}'

class StudentExerciseReports():

    # """Methods for reports on the Student Exercises database"""

    def __init__(self):
        self.db_path = "/Users/Curt/Workspace/python/practice/studentexercises/studentexercises.db"

    def all_students(self):

        # """Retrieve all students with the cohort name"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Student(
            row[1], row[2], row[3], row[5])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select s.Id,
                s.FirstName,
                s.LastName,
                s.Slack,
                s.CohortId,
                c.Name
            from Student s
            join Cohort c on s.CohortId = c.Id
            order by s.CohortId
            """)

            all_students = db_cursor.fetchall()

            for student in all_students:
                print(student)

    def all_exercises(self):

        # """Retrieve all students with the cohort name"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Exercises(
            row[1], row[2])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select e.Id,
                e.ExerciseName,
                e.ExerciseLanguage
            from Exercises e
            """)

            all_exercises = db_cursor.fetchall()

            for exercise in all_exercises:
                print(exercise)

    def all_cohorts(self):

        # """Retrieve all students with the cohort name"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Cohort(
            row[1])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select c.Id,
                c.Name
            from Cohort c
            """)

            all_cohorts = db_cursor.fetchall()

            for cohort in all_cohorts:
                print(cohort)

    def all_instructors(self):

        # """Retrieve all students with the cohort name"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Instructor(
            row[1], row[2], row[3], row[6], row[5])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select i.Id,
                i.FirstName,
                i.LastName,
                i.Slack,
                i.CohortId,
                i.Specialty,
                c.Name
            from Instructor i
            join Cohort c on i.CohortId = c.Id
            order by i.CohortId
            """)

            all_instructors = db_cursor.fetchall()

            for instructor in all_instructors:
                print(instructor)


    def all_assigned_exercises(self):

        exercises = dict()

        with sqlite3.connect(self.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
                select
                    e.Id ExerciseId,
                    e.ExerciseName,
                    s.Id,
                    s.FirstName,
                    s.LastName
                from Exercises e
                join AssignedExercises se on se.ExerciseId = e.Id
                join Student s on s.Id = se.StudentId
            """)

            dataset = db_cursor.fetchall()

            for row in dataset:
                exercise_id = row[0]
                exercise_name = row[1]
                student_id = row[2]
                student_name = f'{row[3]} {row[4]}'

                if exercise_name not in exercises:
                    exercises[exercise_name] = [student_name]
                else:
                    exercises[exercise_name].append(student_name)

                for exercise_name, students in exercises.items():
                    print(exercise_name)
                    for student in students:
                        print(f'\t -{student}')

    def student_exercises(self):

        students = dict()

        with sqlite3.connect(self.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
                select
                    s.Id StudentId,
                    s.FirstName,
                    s.LastName,
                    e.Id ExerciseId,
                    e.ExerciseName
                from Exercises e
                join AssignedExercises se on se.ExerciseId = e.Id
                join Student s on s.Id = se.StudentId
            """)

            dataset = db_cursor.fetchall()

            for row in dataset:
                exercise_id = row[3]
                exercise_name = row[4]
                student_id = row[0]
                student_name = f'{row[1]} {row[2]}'

                if student_name not in students:
                    students[student_name] = [exercise_name]
                else:
                    students[student_name].append(exercise_name)

                for student_name, x in students.items():
                    print(student_name)
                    for exercise in x:
                        print(f'\t -{exercise}')

reports = StudentExerciseReports()
# reports.all_students()
# reports.all_exercises()
# reports.all_cohorts()
# reports.all_instructors()
# reports.all_assigned_exercises()
# reports.student_exercises()



