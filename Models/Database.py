import psycopg2
import random
import datetime
import time
from Models.TraineeModel import Trainee
from Models.SchoolModel import School
from Models.TaskModel import Task
# from TaskModel import Task

class DatabaseManager:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="ojtdb",
            user="postgres",
            password="011456",
            host="localhost",
            port=5432,
        )

    def get_schools(self):
        schools = []
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM SCHOOL")
            results = cursor.fetchall()
            for row in results:
                from Models.SchoolModel import School
                school = School()
                school.sid = row[0]
                school.name = row[1]
                school.address = row[2]
                school.coordinator = row[3]
                school.contact = row[4]
                school.requiredHours = row[5]
                school.initials = row[6]
                schools.append(school)
        return schools

    def get_trainee_school_by_id(self,trainee_id):
        # school_id = self.get_trainee_school_id(trainee_id)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT school_name FROM SCHOOL INNER JOIN TRAINEE USING(SCHOOL_ID) WHERE TRAINEE_ID = %s",(trainee_id,))
                res = cursor.fetchone()
                if res:
                    return res[0]
        except Exception as e:
            raise e


    def get_school_by_id(self,school_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM SCHOOL WHERE SCHOOL_ID = %s",(school_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            raise e

    def add_school(self, school):
        query = "INSERT INTO SCHOOL(SCHOOL_ID,SCHOOL_NAME,SCHOOL_ADDRESS,SCHOOL_COORDINATOR,SCHOOL_CONTACT,SCHOOL_REQUIRED_TIME,SCHOOL_INITIAL) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        school.sid,
                        school.name,
                        school.address,
                        school.coordinator,
                        school.contact,
                        school.requiredHours,
                        school.initials
                    ),
                )
                self.connection.commit()
                return cursor.rowcount > 0
        except psycopg2.DatabaseError as error:
            print(error)
            return False

    
    def update_school(self, id, school):
        query = "UPDATE SCHOOL SET SCHOOL_NAME = %s, SCHOOL_ADDRESS = %s, SCHOOL_COORDINATOR = %s,SCHOOL_CONTACT = %s, SCHOOL_REQUIRED_TIME = %s, SCHOOL_INITIAL = %s WHERE SCHOOL_ID = %s"
        try:
            with self.connection.cursor() as cursor:
                success = cursor.execute(query, (school.name, school.address, school.coordinator, school.contact,school.requiredHours,school.initials,id))
                self.connection.commit()
                return success is not None and success > 0            
        except psycopg2.DatabaseError as error:
            print("error")

    def delete_school(self, sid):
        query = "DELETE FROM SCHOOL WHERE SCHOOL_ID = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (sid,))
                self.connection.commit()
                return cursor.rowcount > 0        
        except psycopg2.DatabaseError as error:
            print(error)

    def count_school(self):
        query = "SELECT COUNT(*) FROM SCHOOL"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                count = cursor.fetchone()
                if count is not None:
                    return int(count[0])
                return 0
        except Exception as e:
            raise


    def count_trainees(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM TRAINEE")
                count = cursor.fetchone()
                if count is not None:
                    return int(count[0])
                return 0
        except Exception as e:
            raise


    def add_trainee(self, trainee):
       
        query = "INSERT INTO TRAINEE(TRAINEE_ID,TRAINEE_FIRSTNAME,TRAINEE_LASTNAME,TRAINEE_EMAIL,TRAINEE_COURSE,TRAINEE_CONTACT,SCHOOL_ID) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (trainee.id, trainee.firstname, trainee.lastname, trainee.email, trainee.course,trainee.contact,trainee.school_id))
                self.connection.commit()
                self.remove_student(trainee.email)
                return cursor.rowcount > 0
        except psycopg2.DatabaseError as error:
            print(error)
    def get_all_trainees_id(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT trainee_id FROM TRAINEE")
                return cursor.fetchall()
        except Exception as e:
            raise e
    def get_school_initial(self,school_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT SCHOOL_INITIAL FROM SCHOOL WHERE SCHOOL_ID = %s",(school_id,))
                res = cursor.fetchone()
                return res[0] if res else "Unknown"
        except Exception as e:
            raise e
    


    def get_trainees(self):

        trainees = []
        try:

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TRAINEE WHERE TRAINEE_STATUS != 'deleted'")
                for row in cursor.fetchall():
                    trainee = Trainee()
                    trainee.firstname = str(row[1])
                    trainee.lastname = str(row[2])
                    trainee.email = str(row[3])
                    trainee.course = str(row[4])
                    trainee.id = str(row[0])
                    trainee.sid = str(row[5])
                    trainee.contact = str(row[6])          
                    trainees.append(trainee)
            return trainees
        except psycopg2.DatabaseError as error:
            print(error)

    def get_ongoing_trainees(self):

        trainees = []
        try:

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TRAINEE WHERE TRAINEE_STATUS != 'deleted' AND TRAINEE_STATUS = 'ongoing'")
                for row in cursor.fetchall():
                    trainee = Trainee()
                    trainee.firstname = str(row[1])
                    trainee.lastname = str(row[2])
                    trainee.email = str(row[3])
                    trainee.course = str(row[4])
                    trainee.id = str(row[0])
                    trainee.sid = str(row[5])
                    trainee.contact = str(row[6])          
                    trainees.append(trainee)
            return trainees
        except psycopg2.DatabaseError as error:
            print(error)


    def get_completers(self):

        trainees = []
        try:

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TRAINEE WHERE TRAINEE_STATUS = 'completed'")
                for row in cursor.fetchall():
                    trainee = Trainee()
                    trainee.firstname = str(row[1])
                    trainee.lastname = str(row[2])
                    trainee.email = str(row[3])
                    trainee.course = str(row[4])
                    trainee.id = str(row[0])
                    trainee.sid = str(row[5])
                    trainee.contact = str(row[6])          
                    trainees.append(trainee)
            return trainees
        except psycopg2.DatabaseError as error:
            print(error)

    def get_deleted_trainees(self):

        trainees = []
        try:

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TRAINEE WHERE TRAINEE_STATUS = 'deleted'")
                for row in cursor.fetchall():
                    trainee = Trainee()
                    trainee.firstname = str(row[1])
                    trainee.lastname = str(row[2])
                    trainee.email = str(row[3])
                    trainee.course = str(row[4])
                    trainee.id = str(row[0])
                    trainee.sid = str(row[5])
                    trainee.contact = str(row[6])          
                    trainees.append(trainee)
            return trainees
        except psycopg2.DatabaseError as error:
            print(error)

    def get_trainee_by_id(self,idNum):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TRAINEE WHERE TRAINEE_ID = %s", (idNum,))
                return cursor.fetchone()           
        except psycopg2.DatabaseError as error:
            print(error)
    def get_trainee_id_by_fullname(self,firstname,lastname):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT trainee_id FROM TRAINEE WHERE TRAINEE_FIRSTNAME = %s AND TRAINEE_LASTNAME = %s",(firstname,lastname))
                result = cursor.fetchone()
                if result:
                    return result[0]
        except Exception as e:
            raise e

    def get_full_name_by_id(self,tid):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT TRAINEE_FIRSTNAME,TRAINEE_LASTNAME FROM TRAINEE WHERE TRAINEE_ID = %s ", (tid,))
                return cursor.fetchone()
        except psycopg2.DatabaseError as error:
            raise error

    def trainee_exists(self,email):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TRAINEE WHERE TRAINEE_EMAIL = %s",(email,))
                result = cursor.fetchone()
                return True if result else False
        except Exception as e:
            print(e)


    def add_student(self, trainee):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO REGISTRY(REG_FIRSTNAME,REG_LASTNAME,REG_COURSE,REG_CONTACT,REG_EMAIL,SCHOOL_ID) VALUES(%s,%s,%s,%s,%s,%s)",
                    (trainee.firstname, trainee.lastname, trainee.course, trainee.contact, trainee.email, trainee.school_id),
                )
                self.connection.commit()
                return cursor.rowcount > 0
        except psycopg2.DatabaseError as error:
            print(error)

    def remove_student(self, student_email):
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM REGISTRY WHERE REG_EMAIL = %s",
                        (student_email,)
                    )
                    self.connection.commit()
                    return cursor.rowcount > 0
            except psycopg2.DatabaseError as error:
                print(error)

    def get_students(self):
        students = []
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT reg_firstname,reg_lastname, reg_course, reg_contact, reg_email, school_id FROM REGISTRY")
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        student = Trainee()
                     
                        student.firstname = row[0]
                        student.lastname = row[1]
                        student.course = row[2]
                        student.email = row[4]
                        student.contact = row[3]
                        student.school_id = row[5]
                        students.append(student)
                return students
        except psycopg2.DatabaseError as error:
            print(error)

    def get_student_by_email(self, email):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM REGISTRY WHERE REG_EMAIL = %s", (email,))
                new_trainee = cursor.fetchone()
                if new_trainee is not None:
                    return new_trainee
        except psycopg2.DatabaseError as error:
            print(error)


    def student_exists(self,email):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM REGISTRY WHERE REG_EMAIL = %s",(email,))
                result = cursor.fetchone()
                return True if result else False
        except psycopg2.DatabaseError as error:
            pass

    def is_duplicate_name(self,firstname,lastname):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM REGISTRY WHERE REG_FIRSTNAME = %s AND REG_LASTNAME = %s",(firstname,lastname))
                result = cursor.fetchall()
                return True if result else False
        except Exception as e:
            raise e

    def add_attendance(self,tid):
        try:
            with self.connection.cursor() as cursor:
                date = datetime.datetime.now().date()
               
                cursor.execute("INSERT INTO attendance(trainee_id, attend_date,attend_time_in) VALUES (%s,CURRENT_DATE,CURRENT_TIME)",(tid,))
                self.connection.commit()
        except Exception as e:
            raise e

    def logout_attendance(self,tid):
        #if has log in
        if self.attendance_checked:
            #if not logged out
            if not self.has_logged_out(tid):
                try:
                    date_now = datetime.datetime.now().date()
                    with self.connection.cursor() as cursor:
                        cursor.execute("UPDATE attendance SET attend_time_out = CURRENT_TIME WHERE attend_date = CURRENT_DATE AND trainee_id = %s",(tid,))
                        self.connection.commit()
                        return cursor.rowcount > 0 
                    
                except Exception as e:
                    raise e
        return False

    #has logged in
    def attendance_checked(self,trainee_id):        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM attendance WHERE trainee_id = %s AND attend_date = CURRENT_DATE AND attend_time_in IS NOT NULL",(trainee_id,))
                result = cursor.fetchone()
                return True if result else False
        except Exception as e:
            raise e

    def has_logged_out(self,tid):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM attendance WHERE attend_time_out IS NOT NULL AND trainee_id = %s AND attend_date = CURRENT_DATE",(tid,))
                return True if cursor.fetchone() else False
        except Exception as e:
            raise e

    def get_trainee_required_time(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT SCHOOL_REQUIRED_TIME FROM SCHOOL INNER JOIN TRAINEE USING(SCHOOL_ID) WHERE TRAINEE_ID = %s",(trainee_id,))
                result = cursor.fetchone()
                return float(result[0])
        except Exception as e:
            raise e


    def get_trainee_total_hours_worked(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT TOTAL_HOURS_WORKED FROM TRAINEE WHERE TRAINEE_ID = %s", (trainee_id,))
                result = cursor.fetchone()
                
            return float(result[0])

        except Exception as e:
            raise e

    def is_trainee_status_complete(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TRAINEE WHERE TRAINEE_STATUS = 'completed' AND TRAINEE_ID = %s",(trainee_id,))
                result = cursor.fetchone()
                return True if result else False
        except Exception as e:
            raise e
 

    def get_school_name_by_id(self,sid):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT SCHOOL_NAME FROM SCHOOL WHERE SCHOOL_ID = %s", (sid,))
                result = cursor.fetchone()
                return str(result[0]) if result else None
        except Exception as ex:
            raise ex

    def get_school_id_by_name(self,name):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT school_id FROM school WHERE school_name = %s",(name.strip(),))
                result = cursor.fetchall()
                return result[0][0]
        except Exception as e:
            raise e

    def get_unlogged_trainees(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT trainee_id FROM attendance WHERE attend_date = CURRENT_DATE AND attend_time_in IS NOT NULL AND attend_time_out IS NULL")
                result = cursor.fetchall()
                return [item[0] for item in result]
                
        except Exception as ex:
            raise ex

    def get_force_logout_timestamp(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT TO_TIMESTAMP(setting_value,'HH12:MI am')::TIME FROM admin_setting WHERE setting_name = 'auto-log-out'")
                res = cursor.fetchone()
                return res[0]
        except Exception as e:
            raise e

    def force_log_out(self):
        unlogged_trainees = self.get_unlogged_trainees()
        if unlogged_trainees:
            for trainee_id in unlogged_trainees:
                self.logout_attendance(trainee_id)
                try:
                    with self.connection.cursor() as cursor:
                        cursor.execute("INSERT INTO auto_logged VALUES(%s,CURRENT_DATE)",(trainee_id,))
                        self.connection.commit()
                except Exception as ex:
                    raise ex
            return True
        return False

    # #TASKS



    def add_new_task(self,taskObject):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                        BEGIN;
                        INSERT INTO task(task_title,task_descript,task_due) VALUES (%s,%s,%s)
                        RETURNING task_id;

                         """,(taskObject.title, taskObject.description,taskObject.due))
                task_id = cursor.fetchone()[0]
                self.connection.commit()
                return task_id
                print("done")

        except Exception as e:
            raise e

    def set_trainee_deleted(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE TRAINEE SET TRAINEE_STATUS = 'deleted' WHERE TRAINEE_ID = %s",(trainee_id,))
                self.connection.commit()
                return cursor.rowcount > 0

        except Exception as e:
            raise e
    def assign_task_to_trainee(self,task_id,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO task_assignment(task_id, trainee_id) VALUES(%s, %s)",(task_id,trainee_id))
                self.connection.commit()

                return cursor.rowcount > 0
        except Exception as e:
            raise e

  
    def get_all_tasks(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TASK")
                result = cursor.fetchall()
                task_list = []
                for row in result:
                    task = Task()
                    task.title = row[1]
                    task.description = row[2]
                    task.due = row[3]
                    task.created_at = row[4]
                    task_list.append(task)
                return task_list
        except Exception as e:
            raise e
    def get_ongoing_tasks(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TASK WHERE TASK_STATUS = 'ongoing'")
                result = cursor.fetchall()
                task_list = []
                for row in result:
                    task = Task()
                    task.title = row[1]
                    task.description = row[2]
                    task.due = row[3]
                    task.created_at = row[4]
                    task_list.append(task)
                return task_list
        except Exception as e:
            raise e
    def get_completed_tasks(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TASK WHERE TASK_STATUS = 'completed'")
                result = cursor.fetchall()
                task_list = []
                for row in result:
                    task = Task()
                    task.title = row[1]
                    task.description = row[2]
                    task.due = row[3]
                    task.created_at = row[4]
                    task_list.append(task)
                return task_list
        except Exception as e:
            raise e
    


    def get_task(self,task_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TASK WHERE TASK_ID = %s",(task_id,))
                result = cursor.fetchone()
                task = Task()
                task = Task()
                task.title = result[1]
                task.description = result[2]
                task.due = result[3]
               
                task.created_at = result[4]
                return task

        except Exception as e:
            raise e
    def get_task_id(self,title,due):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT task_id FROM TASK WHERE TASK_TITLE = %s AND TASK_DUE = %s",(title,due))
                res = cursor.fetchone()
                return res[0] if res else '0'
        except Exception as e:
            raise e
    def get_assigned_task(self,task_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT TRAINEE_ID FROM TASK_ASSIGNMENT WHERE TASK_ID = %s",(task_id,))
                result = cursor.fetchall()
                return [assign_id[0] for assign_id  in result]
        except Exception as e:
            raise e

    def set_task_done(self,title,due):
        try:
            with self.connection.cursor() as cursor:
                status = 'completed'
                due_date_converted = datetime.datetime.strptime(due, "%Y-%m-%d").date()
                if datetime.datetime.now().date() > due_date_converted:
                    status = 'late'
                cursor.execute("UPDATE TASK SET TASK_STATUS = %s WHERE TASK_TITLE = %s AND TASK_DUE = %s",(status,title,due))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            raise e
    def set_task_abandoned(self,title,due):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE TASK SET TASK_STATUS = 'abandoned' WHERE TASK_TITLE = %s AND TASK_DUE = %s",(title,due))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            raise e



    def get_task_status(self,task_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT TASK_STATUS FROM TASK WHERE TASK_ID = %s",(task_id,))
                res = cursor.fetchone()
                if res:
                    return str(res[0])
        except Exception as e:
            raise e


    ###USER TASKS
    def get_trainee_new_tasks(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TASK INNER JOIN TASK_ASSIGNMENT USING(TASK_ID) INNER JOIN TRAINEE USING (TRAINEE_ID) where TASK.TASK_STATUS ='ongoing' AND TASK.TASK_DUE >= CURRENT_DATE AND TASK_ASSIGNMENT.TRAINEE_ID = %s ",(trainee_id,))
                res = cursor.fetchall()
                tasks =  []
                if res:
                    
                    for tup in res:
                        task = Task()
                        task.title = tup[2]

                        task.description = tup[3]
                        task.due = tup[4]
                        task.created_at = tup[5]
                        task.status = tup[6]
                        tasks.append(task)
                print(tasks)
                return tasks

        except Exception as e:
            raise e

    def get_trainee_completed_tasks(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TASK INNER JOIN TASK_ASSIGNMENT USING(TASK_ID) INNER JOIN TRAINEE USING(TRAINEE_ID) WHERE TASK.TASK_STATUS = 'completed' AND TASK_ASSIGNMENT.TRAINEE_ID = %s",(trainee_id,))
                res = cursor.fetchall()
                tasks = []
                for column in res:
                    task = Task()
                    task.title= column[2]
                    task.description = column[3]
                    task.due = column[4]
                    task.created_at = column[5]
                    tasks.append(task)
                return tasks
        except Exception as e:
            raise e


    def  is_trainee_assigned_this_task(self,trainee_id,task_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TASK_ASSIGNMENT WHERE ")
        except Exception as e:
            raise e


    ####ADMIN

    def validate_admin(self,username,password):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM ADMIN WHERE ADMIN_USERNAME = %s AND ADMIN_PASSWORD = %s",(username,password))
                return cursor.rowcount > 0
        except Exception as e:
            raise e

    def is_deleted_trainee(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TRAINEE WHERE TRAINEE_ID = %s AND TRAINEE_STATUS = 'deleted'",(trainee_id,))
                return True if cursor.fetchone() else False
        except Exception as e:
            raise e

    def change_admin_login_credentials(self,username,password,cur_username):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE ADMIN SET ADMIN_USERNAME = %s, ADMIN_PASSWORD = %s WHERE ADMIN_USERNAME = %s",(username,password,cur_username))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            raise e

    def get_reg_time_in(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT SETTING_VALUE FROM ADMIN_SETTING WHERE SETTING_NAME = 'reg_time_in'")
                return cursor.fetchone()[0]
        except Exception as e:
            raise e



    def get_company_name(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT SETTING_VALUE FROM ADMIN_SETTING WHERE SETTING_NAME = 'company_name'")
                return str(cursor.fetchone()[0])
        except Exception as e:
            raise e

    def get_reg_time_out(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT SETTING_VALUE FROM ADMIN_SETTING WHERE SETTING_NAME = 'reg_time_out'")
                return cursor.fetchone()[0]
        except Exception as e:
            raise e

    def save_new_company_name(self,name):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE ADMIN_SETTING SET SETTING_VALUE = %s WHERE SETTING_NAME = 'company_name'",(name,))
                self.connection.commit()
        except Exception as e:
            raise e    
    def save_new_reg_time_in(self,time):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE ADMIN_SETTING SET SETTING_VALUE = %s WHERE SETTING_NAME = 'reg_time_in'",(time,))
                self.connection.commit()
        except Exception as e:
            raise e
    def save_new_reg_time_out(self,time):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE ADMIN_SETTING SET SETTING_VALUE = %s WHERE SETTING_NAME = 'reg_time_out'",(time,))
                self.connection.commit()
        except Exception as e:
            raise e
    def save_new_auto_log_out(self,time):
        try:
            with self.connection.cursor() as cursor:
                
                cursor.execute("UPDATE ADMIN_SETTING SET SETTING_VALUE = %s WHERE SETTING_NAME = 'auto-log-out'", (str(time),))

                self.connection.commit()
        except Exception as e:
            raise e

    def get_trainee_total_task_taken(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT TOTAL_TASKS_TAKEN FROM TRAINEE WHERE TRAINEE_ID = %s",(trainee_id.strip(),))
                return int(cursor.fetchone()[0])
        except Exception as e:
            raise e

    def get_trainee_total_task_completed(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT TOTAL_TASKS_COMPLETED FROM TRAINEE WHERE TRAINEE_ID = %s",(trainee_id.strip(),))
                return int(cursor.fetchone()[0])
        except Exception as e:
            raise e
    def get_trainee_total_late_tasks(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT TOTAL_LATE_TASKS FROM TRAINEE WHERE TRAINEE_ID = %s",(trainee_id.strip(),))
                return int(cursor.fetchone()[0])
        except Exception as e:
            raise e
    def get_trainee_total_abandoned_tasks(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT TOTAL_TASKS_ABANDONED FROM TRAINEE WHERE TRAINEE_ID = %s",(trainee_id.strip(),))
                return int(cursor.fetchone()[0])
        except Exception as e:
            raise e

    def restore_trainee(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE TRAINEE SET TRAINEE_STATUS = 'ongoing' WHERE TRAINEE_ID = %s",(trainee_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            raise e

    def get_admin_password(self,username):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT ADMIN_PASSWORD FROM ADMIN WHERE ADMIN_USERNAME = %s",(username,))
                res = cursor.fetchone()
                return res[0] if res else "oooognih"
        except Exception as e:
            raise e
    def add_new_admin(self,admin):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO ADMIN(ADMIN_FIRSTNAME,ADMIN_LASTNAME,ADMIN_USERNAME,ADMIN_PASSWORD) VALUES(%s,%s,%s,%s)",(admin[0],admin[1],admin[2],admin[3]))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            raise e
    def restore_all(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE TRAINEE SET TRAINEE_STATUS = 'ongoing' WHERE TRAINEE_STATUS = 'deleted'")
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            raise e
    def clear_all(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM TRAINEE WHERE TRAINEE_STATUS = 'deleted'")
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            raise e

    def estimate_days(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT SETTING_VALUE FROM ADMIN_SETTING WHERE SETTING_NAME = 'reg_working_hours'")
                reg_working_hours = float(cursor.fetchone()[0])
                print(reg_working_hours)
            
                remaining = 0
                if self.get_trainee_total_hours_worked(trainee_id) > 0:
                    remaining =  self.get_trainee_required_time(trainee_id) - self.get_trainee_total_hours_worked(trainee_id)
                days_left = remaining / reg_working_hours
                return days_left


        except Exception as e:
            raise e

    def get_auto_logged(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT T.TRAINEE_ID, T.TRAINEE_FIRSTNAME, T.TRAINEE_LASTNAME, A.LOGGED_DATE FROM TRAINEE T INNER JOIN AUTO_LOGGED A USING(TRAINEE_ID) ")
                res = cursor.fetchall()
                return res
        except Exception as e:
            raise e
    def get_active(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT T.TRAINEE_ID, T.TRAINEE_FIRSTNAME, T.TRAINEE_LASTNAME, S.SCHOOL_NAME FROM TRAINEE T INNER JOIN ATTENDANCE A USING(TRAINEE_ID) INNER JOIN SCHOOL S USING(SCHOOL_ID) WHERE ATTEND_TIME_IN IS NOT NULL AND ATTEND_TIME_OUT IS NULL AND ATTEND_DATE = CURRENT_DATE ")
                res = cursor.fetchall()
                return res
        except Exception as e:
            raise e
    def get_trainee_missed_task(self,trainee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM TASK INNER JOIN TASK_ASSIGNMENT USING(TASK_ID) INNER JOIN TRAINEE USING(TRAINEE_ID) WHERE TASK.TASK_STATUS = 'abandoned' AND TASK_ASSIGNMENT.TRAINEE_ID = %s",(trainee_id,))
                res = cursor.fetchall()
                return res
        except Exception as e:
            raise e








