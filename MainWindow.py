from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from PyQt5.uic import loadUiType
from Models.Database import DatabaseManager
from Models.TraineeModel import Trainee
from Models.SchoolModel import School
from Models.TaskModel import Task
from Models.State import State
from DialogBox import Dialog
from AlertDialog import AlertDialog

import string
import random
import datetime
import time
import re
ui, _ = loadUiType('Content/ojtms.ui')

class MainWindow(QMainWindow,ui):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.setWindowTitle("Final Project Ojtms")
		
		self.initialSettings()
		
		self.ToLoginAdmin.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(1))
		self.ToLoginTrainee.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(3))
		self.RegisterNewBtn.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(4))	
		self.DashboardBtn.clicked.connect(self.clickedDashboard)
		self.TraineesBtn.clicked.connect(self.clickedTrainees)
		self.SchoolBtn.clicked.connect(self.clickedSchool)
		self.ProgressBtn.clicked.connect(self.clickedProgressBtn)	
		self.Registry.clicked.connect(self.clickedRegistry)

		self.BtnAddSchool.clicked.connect(self.add_new_school)
		self.AdminLoginBtn.clicked.connect(self.login_admin)	
		self.RegistryTbl.itemSelectionChanged.connect(self.show_approval_display)
		self.SchoolTbl.itemSelectionChanged.connect(self.show_frame_34_36)
		self.RegisterBtn.clicked.connect(self.insert_student)
		self.ApproveBtn.clicked.connect(self.promote_student_as_trainee)
		self.DeclineBtn.clicked.connect(self.decline_student)
		self.AddNewBtn.clicked.connect(self.toggle_school_frames)	
		self.EditBtn.clicked.connect(self.set_txtbox_to_selected_school)
		self.UpdateSchoolBtn.clicked.connect(self.update_a_school)
		self.DeleteBtn.clicked.connect(self.delete_a_school)
		self.SchoolTbl.itemSelectionChanged.connect(self.clear_textbox_in_add_school)
		self.SchoolBtn.clicked.connect(self.clear_selections_in_admin)
		self.DashboardBtn.clicked.connect(self.clear_selections_in_admin)
		self.TraineesBtn.clicked.connect(self.clear_selections_in_admin)
		self.backButton.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(0))
		self.num0Btn.clicked.connect(lambda:self.displayNumLoginTrainee(self.num0Btn.text()))
		self.num1Btn.clicked.connect(lambda:self.displayNumLoginTrainee(self.num1Btn.text()))
		self.num2Btn.clicked.connect(lambda:self.displayNumLoginTrainee(self.num2Btn.text()))
		self.num3Btn.clicked.connect(lambda:self.displayNumLoginTrainee(self.num3Btn.text()))
		self.num4Btn.clicked.connect(lambda:self.displayNumLoginTrainee(self.num4Btn.text()))
		self.num5Btn.clicked.connect(lambda:self.displayNumLoginTrainee(self.num5Btn.text()))
		self.num6Btn.clicked.connect(lambda:self.displayNumLoginTrainee(self.num6Btn.text()))
		self.num7Btn.clicked.connect(lambda:self.displayNumLoginTrainee(self.num7Btn.text()))
		self.num8Btn.clicked.connect(lambda:self.displayNumLoginTrainee(self.num8Btn.text()))
		self.num9Btn.clicked.connect(lambda:self.displayNumLoginTrainee(self.num9Btn.text()))
		self.registerCancelBtn.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(3))
		self.loginBtn.clicked.connect(self.login_trainee_clicked)
		self.delBtn.clicked.connect(self.del_clicked)
		self.resetBtn.clicked.connect(self.resetClicked)
		self.toolButton.clicked.connect(self.toggle_widescreen_school)		
		self.sortSchoolComboBox.currentIndexChanged.connect(self.handle_sort_school_change)
		self.logoutBtn.clicked.connect(self.logout_trainee_attendance)
		self.LogoutBtn.clicked.connect(self.logout_admin)
		self.Tasks.clicked.connect(self.clickedTasks)
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_clock)
		self.timer.timeout.connect(self.force_log_out)
		self.timer.start(1000) 
		
		self.taskDoneBtn.clicked.connect(self.taskDoneBtnClicked)
		self.title_timer = QTimer()
		self.title_timer.timeout.connect(self.slide_title)
		self.title_timer.start(5000)

		self.force_logout_executed = False


		# #TASKS
		# self.assignTaskBtn.clicked.connect(self.clickedAssignedTaskBtn)
		self.AddNewTaskBtn.clicked.connect(self.add_new_task)
		self.filterListWidget.textChanged.connect(self.filter_list_widget)
		
		self.viewTaskTable.itemSelectionChanged.connect(self.task_table_selection_changed)
		self.ongoingTaskTable.itemSelectionChanged.connect(self.ongoing_task_table_selection_changed)

		self.filterTrainee.textChanged.connect(self.filterTraineeTable)

		self.tasksTab.currentChanged.connect(self.task_tab_changed)
		self.saveChangesChangeCredentialsBtn.clicked.connect(self.saveChangesChangeCredentialsBtnClicked)

		#################progress part
		self.ViewTraineesTbl.itemSelectionChanged.connect(self.viewTraineesTblChanged)
		self.TaskProgressTbl.itemSelectionChanged.connect(self.TaskProgressTblChanged)
		self.ManageTraineesTbl.itemSelectionChanged.connect(self.toggleDeleteTraineeBtn)
		self.collapsable.clicked.connect(self.toggle_menu)
		self.mousePressEvent = self.onMousePressEvent
		self.tabWidget.currentChanged.connect(self.deselectTablesOnTrainee)

		self.contactTxtBx.setValidator(QRegExpValidator(QRegExp(r"\d{1,%d}" % 11)))
		self.emailTxtBx.setValidator(QRegularExpressionValidator(QRegularExpression(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")))#email validator



		#user side
		self.userSideSeeTasksBtn.clicked.connect(self.userSideSeeTasksBtnClicked)
		self.deleteTraineeBtn.clicked.connect(self.deleteTraineeClicked)
		self.backButton_2.clicked.connect(self.backButton_2Clicked)
		self.pushButton_8.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(3))
		self.adminSettingsBtn.clicked.connect(self.adminSettingsBtnClicked)

		self.changeCompanyNameBtn.clicked.connect(self.changeCompanyNameBtnClicked)
		self.regTimeInBtn.clicked.connect(self.regTimeInBtnClicked)
		self.regTimeOutBtn.clicked.connect(self.regTimeOutBtnClicked)
		self.autoLogOutBtn.clicked.connect(self.autoLogOutBtnClicked)
		self.saveGeneralSettings.clicked.connect(self.saveGeneralSettingsClicked)
		self.Registry.clicked.connect(lambda:self.stackedWidget_2.setCurrentIndex(5))
		self.ProgressBtn.clicked.connect(lambda:self.stackedWidget_2.setCurrentIndex(6))


		self.filterTrainee_3.textChanged.connect(self.filterManageTraineesTable)
		self.filterTrainee_2.textChanged.connect(self.filterTaskProgressTbl)
		self.SearchBox.textChanged.connect(self.filterSchoolTbl)
		self.filterTrainee_4.textChanged.connect(self.filterCompletersTable)
		self.filterTrainee_5.textChanged.connect(self.filterDeletedTable)
		self.taskAbandoned.clicked.connect(self.abandonTaskClicked)

		self.selectAllCheckBox_1.stateChanged.connect(lambda:self.selectAllListWidget(self.selectAllCheckBox_1,self.listWidget))

		self.TaskProgressTbl.itemSelectionChanged.connect(lambda:self.frame_102.show())
		self.DeletedTable.itemSelectionChanged.connect(lambda:self.restoreBtn.show())

		self.restoreBtn.clicked.connect(self.restore_trainee)
		self.addAdminBtn.clicked.connect(lambda:self.frame_127.show())
		self.confirmPasswordEnter.clicked.connect(self.confirmPasswordEnterClicked)

		self.restoreAllBtn.clicked.connect(self.restore_all)
		self.clearAllBtn.clicked.connect(self.clear_deleted)
		self.SchoolRequiredHoursInput.setValidator(QIntValidator(0,2147483647))
		self.SchoolIdAddInput.setValidator(QIntValidator())
		self.SchoolNameAddInput.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]+")))
		self.label_100.setText(DatabaseManager().get_company_name().upper())
		self.displayLabel.setValidator(QIntValidator())
		self.toolButton_2.clicked.connect(self.toggle_password_visibility)
		self.frame_138.mousePressEvent = lambda event: self.navigate_present()
		self.frame_41.mousePressEvent = lambda event: self.navigate_trainee()
		self.frame_40.mousePressEvent = lambda event: self.navigate_school()
		self.pushButton_2.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(0))

	def navigate_present(self):
		self.clickedTrainees()
		self.stackedWidget_2.setCurrentIndex(1)
		self.tabWidget.setCurrentIndex(3)
		
	def navigate_school(self):
		self.clickedTrainees()
		self.stackedWidget_2.setCurrentIndex(2)
		


	def navigate_trainee(self):
		self.clickedTrainees()
		self.stackedWidget_2.setCurrentIndex(1)
		self.tabWidget.setCurrentIndex(0)



		

	def initialSettings(self):
		self.TraineeApprovalDisplay.hide()
		self.populateComboBox()
		self.schoolComBox.setCurrentIndex(0)
		self.stackedWidget.setCurrentIndex(0)
		self.stackedWidget_2.setCurrentIndex(0)
		self.designTable()
		phonevalidator = QRegularExpressionValidator()
		pattern =  QRegularExpression("^[0-9]{11}$")
		phonevalidator.setRegularExpression(pattern)
		self.SchoolContactAddInput.setValidator(phonevalidator)
		self.populate_school_table()
		self.populate_trainee_table()
		self.populate_task_progress_table()
		self.populate_manage_traines_table()
		self.populateCompletersTable()
		self.populateDeletedTable()
		self.frame_35.hide()
		self.admin_dashboard_set_counts()
		self.stackedWidget_5.setCurrentIndex(0)
		self.stackedWidget_3.setCurrentIndex(0)
		
		self.ViewTraineesTbl.horizontalHeader().setVisible(True)
		self.CompletersTable.horizontalHeader().setVisible(True)
		self.DeletedTable.horizontalHeader().setVisible(True)
		self.TaskProgressTbl.horizontalHeader().setVisible(True)
		self.tabWidget_2.setCurrentIndex(0)


		self.deleteTraineeBtn.hide()
		self.backButton_2.hide()

		self.companyNameInput.setReadOnly(True)
		self.regTimeIn.setReadOnly(True)
		self.regTimeOut.setReadOnly(True)
		self.autoLogOut.setReadOnly(True)
		self.DeleteBtn.hide()

		#Tasks
		
		self.dueDate.setMinimumDate(QDate().currentDate())

		self.dueDate.calendarWidget().setSelectedDate(QDate().currentDate())
		self.frame_102.hide()
		self.frame_97.hide()
		self.frame_127.hide()
		self.newAdminAddBtn.clicked.connect(self.add_new_admin)
		self.ActiveTable.horizontalHeader().setVisible(True)
		self.label_98.setText(str(len(DatabaseManager().get_active())))

	def viewTraineesTblChanged(self):
		if len(self.ViewTraineesTbl.selectedItems()) > 0:
			self.set_progress(self.ViewTraineesTbl.selectedItems()[0].text())
	def deselectTablesOnTrainee(self):
		self.ViewTraineesTbl.clearSelection()
		self.RegistryTbl.clearSelection()
		self.CompletersTable.clearSelection()
		self.DeletedTable.clearSelection()
		self.ManageTraineesTbl.clearSelection()
		self.restoreBtn.hide()


		# self.populate_list_widget(0)
	def validate_email(self,email):
	    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
	    return re.match(pattern, email) is not None

	def login_admin(self):
		admin_username = self.adminUsername.text()
		admin_password = self.adminPassword.text()
		database = DatabaseManager()
		if database.validate_admin(admin_username,admin_password):
			self.adminState = State(admin_username)
			self.adminUsername.setText("")
			self.adminPassword.setText("")
			self.stackedWidget.setCurrentIndex(2)
			self.label_96.setText(self.adminState.data.upper())

			self.populate_registry_table()
		else:
			AlertDialog(self,"error","Invalid Admin Credentials").exec()




		
   
	
	def add_new_school(self):

		sid = self.SchoolIdAddInput.text()
		name = self.SchoolNameAddInput.text().lower()
		address = self.SchoolAddressAddInput.text().lower()
		coordinator = self.SchoolCoordinatorAddInput.text().lower()
		contact = self.SchoolContactAddInput.text()
		requiredHours = self.SchoolRequiredHoursInput.text()
		initials = self.School_Initials.text().lower()

		database = DatabaseManager()
		if sid.strip() != "" and name.strip() != "" and address.strip() != "" and coordinator.strip() != "" and contact.strip() != "" and requiredHours.strip() != "" and initials.strip() != "":
			new_school = School()
			new_school.sid = sid
			new_school.name = name.lower()
			new_school.address = address.lower()
			new_school.coordinator = coordinator.lower()
			new_school.contact = contact
			new_school.requiredHours = requiredHours
			new_school.initials = initials
			success = database.add_school(new_school)
			if success:
				AlertDialog(self,"success","School Added Successfully.").exec()
				self.populate_school_table()
				self.clear_textbox_in_add_school()
			else:
				AlertDialog(self,"error","Adding School Failed.").exec()
		else:
			AlertDialog(self,"error","All Fields Are Required.").exec()
			

	def delete_a_school(self):
		selected = self.SchoolTbl.selectedItems()
		if selected:
			sid = selected[0].text()
			mess = "Are you sure to delete this school?\n\nNote: This will also delete all trainees in this school"
			reply = QMessageBox.question(self,"Confirm",mess,QMessageBox.Yes|QMessageBox.No)
			if reply == QMessageBox.Yes:
				database = DatabaseManager()
				success = database.delete_school(sid)
				if success:
					AlertDialog(self,"success","School Deleted Successfully.").exec()
					self.populate_school_table()
					self.populate_trainee_table()
			else:
				return
		else:
			AlertDialog(self,"warning","Select A School To Delete.").exec()

	def update_a_school(self):
		database = DatabaseManager()
		school = School()
		school.sid =self.SchoolIdAddInput.text()
		school.address =self.SchoolAddressAddInput.text()
		school.coordinator =self.SchoolCoordinatorAddInput.text()
		school.contact =self.SchoolContactAddInput.text()
		school.name = database.get_school_name_by_id(school.sid).lower()
		school.requiredHours= self.SchoolRequiredHoursInput.text()
		school.initials = self.School_Initials.text()
		itemSelected = self.SchoolTbl.selectedItems()		
		if school.name == self.SchoolNameAddInput.text() and school.address == itemSelected[2].text() and school.coordinator == itemSelected[3].text() and school.contact== itemSelected[4].text() and school.requiredHours== itemSelected[5].text() and itemSelected[1].text() == school.initials:
			AlertDialog(self,"Warning","No Changes Made").exec()
		else:
			school.name = self.SchoolNameAddInput.text()
			database.update_school(itemSelected[0].text(),school)
			self.clear_textbox_in_add_school()
			AlertDialog(self,"success","School updated successfully").exec()
			self.SchoolTbl.clearSelection()
			self.populate_school_table()

	#Student in this code refers to registration
	#Students

	def insert_student(self):
		school_id_map = self.get_schoolId_schoolName_map()
		firstname = self.firstnameTxtBx.text().strip().lower()
		lastname = self.lastnameTxtBx.text().strip().lower()
		course = self.courseTxtBx.text().strip().lower()
		email = self.emailTxtBx.text().strip().lower()
		contact = self.contactTxtBx.text().strip()

		if self.schoolComBox.currentIndex() != 0 and firstname != "" and lastname != "" and course != "":
			school_id = school_id_map[self.schoolComBox.currentText().lower()]
			database = DatabaseManager()
			trainee = Trainee("",firstname,lastname,email,course,contact,school_id)
			if self.validate_email(email):
				if not database.student_exists(email):
					if not database.is_duplicate_name(firstname,lastname):
						success = database.add_student(trainee)
						if success:
							AlertDialog(self,"success","Please Wait For Admin's Approval").exec()
							self.clear_student_registration_form()
					else:
						AlertDialog(self,"error","Student already in registry.\n Please wait for admin's approval.").exec()
				else:
					AlertDialog(self,"error","This Email Already Exist").exec()
			else:
				AlertDialog(self,"error","Invalid email").exec()
				self.emailTxtBx.setFocus()

		else:
			AlertDialog(self,"error","All Fields Are Required").exec()



	def decline_student(self):
		reg_email = self.RegistryTbl.selectedItems()[1].text()
		answer = QMessageBox.question(self,"Confirm","Decline this student?",QMessageBox.Yes|QMessageBox.No)
		if answer == QMessageBox.Yes:
			database = DatabaseManager()
			success = database.remove_student(reg_email)
			if success:
				AlertDialog(self,"success","Student Declined!").exec()
				self.populate_registry_table()
			else:
				AlertDialog(self,"success","Fail Removing Student..").exec()

	def clear_student_registration_form(self):
		self.firstnameTxtBx.setText("")
		self.lastnameTxtBx.setText("")
		self.contactTxtBx.setText("")
		self.emailTxtBx.setText("")
		self.courseTxtBx.setText("")
		self.schoolComBox.setCurrentIndex(0)
	#student accepted
	def promote_student_as_trainee(self):
		school_id_map = self.get_schoolId_schoolName_map()
		selectedSchoolName = self.display6.text().lower()	
		generated_id = self.generate_unique_id()
		firstname = self.display1.text().lower()
		lastname = self.display2.text().lower()
		email = self.display3.text().lower()
		course =  self.display4.text().lower()
		contact = self.display5.text().lower()
		school_id =  school_id_map[selectedSchoolName]
		trainee = Trainee()
		trainee.id = generated_id
		trainee.firstname = firstname
		trainee.lastname = lastname
		trainee.email = email
		trainee.course = course
		trainee.school_id = school_id
		trainee.contact =  contact
		database = DatabaseManager()
		answer = QMessageBox.question(self,"Confirm","Do you want to add this student?",QMessageBox.Yes|QMessageBox.No)
		if answer == QMessageBox.Yes:
			if not database.trainee_exists(trainee.email):	
				success = database.add_trainee(trainee)	
				if success:
					AlertDialog(self,"success",f"{firstname.title()} is now officially a new trainee.").exec()
					self.populate_registry_table()
					self.populate_trainee_table()
					self.RegistryTbl.clearSelection()
					self.TraineeApprovalDisplay.hide()
				else:
					QMessageBox.information(self,"Fail","Adding Student to Trainees Failed.",QMessageBox.Ok)	
			else:
				QMessageBox.information(self,"Fail","This student is already a trainee",QMessageBox.Ok)					
		else:
			return

	def add_attendance(self,trainee_id):
		database = DatabaseManager()
		database.add_attendance(trainee_id)


	


	"""HELPERS"""
	def designTable(self):
		self.RegistryTbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.ManageTraineesTbl.horizontalHeader().setVisible(True)
		self.SchoolTbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.userSideNewTaskTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.userSideCompletedTaskTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.userSideMissedTaskTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

		#fix some column width
		self.ViewTraineesTbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)	
		self.ViewTraineesTbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
		self.ViewTraineesTbl.horizontalHeader().resizeSection(0, 130)

		self.ActiveTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)	
		self.ActiveTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
		self.ActiveTable.horizontalHeader().resizeSection(0, 130)



		self.TaskProgressTbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)	
		self.TaskProgressTbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
		self.TaskProgressTbl.horizontalHeader().resizeSection(0, 130)

		self.ManageTraineesTbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)	
		self.ManageTraineesTbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
		self.ManageTraineesTbl.horizontalHeader().resizeSection(0, 130)

		self.CompletersTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)	
		self.CompletersTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
		self.CompletersTable.horizontalHeader().resizeSection(0, 130)

		self.DeletedTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)	
		self.DeletedTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
		self.DeletedTable.horizontalHeader().resizeSection(0, 130)




		self.SchoolTbl.horizontalHeader().setSectionResizeMode(0,QHeaderView.Fixed)
		self.SchoolTbl.horizontalHeader().resizeSection(0,130)
		self.SchoolTbl.horizontalHeader().setSectionResizeMode(1,QHeaderView.Fixed)
		self.SchoolTbl.horizontalHeader().resizeSection(1,100)
		self.SchoolTbl.horizontalHeader().setSectionResizeMode(4,QHeaderView.Fixed)
		self.SchoolTbl.horizontalHeader().resizeSection(4,150)
		self.SchoolTbl.horizontalHeader().setSectionResizeMode(5,QHeaderView.Fixed)
		self.SchoolTbl.horizontalHeader().resizeSection(5,130)
		self.SchoolTbl.horizontalHeader().setStretchLastSection(False)


		self.viewTaskTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.viewTaskTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
		self.viewTaskTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
		self.viewTaskTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
		self.viewTaskTable.horizontalHeader().resizeSection(0,50)
		self.viewTaskTable.horizontalHeader().resizeSection(2,100)
		self.viewTaskTable.horizontalHeader().resizeSection(3,100)

		self.ongoingTaskTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.ongoingTaskTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
		self.ongoingTaskTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
		self.ongoingTaskTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
		self.ongoingTaskTable.horizontalHeader().resizeSection(0,50)
		self.ongoingTaskTable.horizontalHeader().resizeSection(2,100)
		self.ongoingTaskTable.horizontalHeader().resizeSection(3,100)

		self.taskAssignedListWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


	def onMousePressEvent(self, event: QMouseEvent):
	        # Check if the event occurred outside the table
	        if event.pos().x() < self.RegistryTbl.pos().x() or event.pos().x() > self.RegistryTbl.pos().x() + self.RegistryTbl.width() or \
	                event.pos().y() < self.RegistryTbl.pos().y() or event.pos().y() > self.RegistryTbl.pos().y() + self.RegistryTbl.height():
	            # Clear the selection of the table
	            self.RegistryTbl.clearSelection()

	        # Call the base class implementation
	        super(MainWindow, self).mousePressEvent(event)
    
	def filterTraineeTable(self, text):
	    for row in range(self.ViewTraineesTbl.rowCount()):
	        hidden = all(text.lower() not in self.ViewTraineesTbl.item(row, column).text().lower() for column in range(self.ViewTraineesTbl.columnCount()))
	        self.ViewTraineesTbl.setRowHidden(row, hidden)

	def filterManageTraineesTable(self,text):
	    for row in range(self.ManageTraineesTbl.rowCount()):
	        hidden = all(text.lower() not in self.ManageTraineesTbl.item(row, column).text().lower() for column in range(self.ManageTraineesTbl.columnCount()))
	        self.ManageTraineesTbl.setRowHidden(row, hidden)
	def filterTaskProgressTbl(self,text):
	    for row in range(self.TaskProgressTbl.rowCount()):
	        hidden = all(text.lower() not in self.TaskProgressTbl.item(row, column).text().lower() for column in range(self.TaskProgressTbl.columnCount()))
	        self.TaskProgressTbl.setRowHidden(row, hidden)

	def filterSchoolTbl(self,text):
	    for row in range(self.SchoolTbl.rowCount()):
	        hidden = all(text.lower() not in self.SchoolTbl.item(row, column).text().lower() for column in range(self.SchoolTbl.columnCount()))
	        self.SchoolTbl.setRowHidden(row, hidden)

	def filterCompletersTable(self,text):
	    for row in range(self.CompletersTable.rowCount()):
	        hidden = all(text.lower() not in self.CompletersTable.item(row, column).text().lower() for column in range(self.CompletersTable.columnCount()))
	        self.CompletersTable.setRowHidden(row, hidden)
	def filterDeletedTable(self,text):
	    for row in range(self.DeletedTable.rowCount()):
	        hidden = all(text.lower() not in self.DeletedTable.item(row, column).text().lower() for column in range(self.DeletedTable.columnCount()))
	        self.DeletedTable.setRowHidden(row, hidden)




		#populate schools to the register page combobox
	def populateComboBox(self):
			school_id_map = self.get_schoolId_schoolName_map()
			school_names = school_id_map.keys()
			school_name_in_title_case = [name.title() for name in school_names]
			self.schoolComBox.addItems(school_name_in_title_case)

	def get_schoolId_schoolName_map(self):
		database = DatabaseManager()
		schools = database.get_schools()
		school_id_map = {}
		for school in schools:
			school_id_map[school.name.lower()] = school.sid
		return school_id_map

	def populate_school_table(self):
		database = DatabaseManager()
		schools = database.get_schools()	
		self.SchoolTbl.setRowCount(len(schools))
		for index, school in enumerate(schools):
			if school.initials:
				school_name = school.initials.upper()
			else:
				school_name = school.name.title()
			self.SchoolTbl.setItem(index,0,QTableWidgetItem(school.sid))
			self.SchoolTbl.setItem(index,1,QTableWidgetItem(school_name))
			self.SchoolTbl.setItem(index,2,QTableWidgetItem(school.address.title()))
			self.SchoolTbl.setItem(index,3,QTableWidgetItem(school.coordinator.title()))
			self.SchoolTbl.setItem(index,4,QTableWidgetItem(school.contact))
			self.SchoolTbl.setItem(index,5,QTableWidgetItem(str(school.requiredHours)))
		

	def populate_registry_table(self):
		database = DatabaseManager()
		students = database.get_students()	
		school_id_map = self.get_schoolId_schoolName_map()
		self.RegistryTbl.setRowCount(len(students))
		for index,student in enumerate(students):
			name = f"{student.firstname} {student.lastname}"
			course = student.course
			email = student.email
			contact = student.contact
			for key,value in school_id_map.items():
				if value == student.school_id:
					schoolname = key
			
			self.RegistryTbl.setItem(index,0,QTableWidgetItem(name.title()))
			self.RegistryTbl.setItem(index,1,QTableWidgetItem(email))
			self.RegistryTbl.setItem(index,2,QTableWidgetItem(contact))
			self.RegistryTbl.setItem(index,3,QTableWidgetItem(course.title()))
			self.RegistryTbl.setItem(index,4,QTableWidgetItem(schoolname.title()))

	def populate_trainee_table(self):
		database = DatabaseManager()
		all_trainees = database.get_ongoing_trainees()
		school_id_map = self.get_schoolId_schoolName_map()
		self.ViewTraineesTbl.setRowCount(len(all_trainees))
		for index,trainee in enumerate(all_trainees):	
			school = database.get_school_initial(trainee.sid)	
			fullname = f"{trainee.firstname} {trainee.lastname}"	
			self.ViewTraineesTbl.setItem(index,0,QTableWidgetItem(trainee.id))
			self.ViewTraineesTbl.setItem(index,1,QTableWidgetItem(fullname.title()))
			self.ViewTraineesTbl.setItem(index,2,QTableWidgetItem(school.upper()))
			self.ViewTraineesTbl.setItem(index,3,QTableWidgetItem(trainee.contact))
			self.ViewTraineesTbl.setItem(index,4,QTableWidgetItem(trainee.email))

	def populate_task_progress_table(self):
		database = DatabaseManager()
		all_trainees = database.get_trainees()
		school_id_map = self.get_schoolId_schoolName_map()
		self.TaskProgressTbl.setRowCount(len(all_trainees))
		for index,trainee in enumerate(all_trainees):	
			school = database.get_school_initial(trainee.sid)	
			fullname = f"{trainee.firstname} {trainee.lastname}"	
			self.TaskProgressTbl.setItem(index,0,QTableWidgetItem(trainee.id))
			self.TaskProgressTbl.setItem(index,1,QTableWidgetItem(fullname.title()))
			self.TaskProgressTbl.setItem(index,2,QTableWidgetItem(school.upper()))
			self.TaskProgressTbl.setItem(index,3,QTableWidgetItem(trainee.contact))
			self.TaskProgressTbl.setItem(index,4,QTableWidgetItem(trainee.email))

	def populate_manage_traines_table(self):
		database = DatabaseManager()
		all_trainees = database.get_ongoing_trainees()
		self.ManageTraineesTbl.setRowCount(len(all_trainees))
		for index,trainee in enumerate(all_trainees):		
			self.ManageTraineesTbl.setItem(index,0,QTableWidgetItem(trainee.id))
			self.ManageTraineesTbl.setItem(index,1,QTableWidgetItem(trainee.firstname.title()))
			self.ManageTraineesTbl.setItem(index,2,QTableWidgetItem(trainee.lastname.title()))
			self.ManageTraineesTbl.setItem(index,3,QTableWidgetItem(database.get_school_name_by_id(trainee.sid)))
			self.ManageTraineesTbl.setItem(index,4,QTableWidgetItem(trainee.email.lower()))
			self.ManageTraineesTbl.setItem(index,5,QTableWidgetItem(trainee.contact))
			self.ManageTraineesTbl.setItem(index,6,QTableWidgetItem(trainee.course))

	def populateCompletersTable(self):
		database = DatabaseManager()
		all_trainees = database.get_completers()
		self.CompletersTable.setRowCount(len(all_trainees))
		for index,trainee in enumerate(all_trainees):		
			self.CompletersTable.setItem(index,0,QTableWidgetItem(trainee.id))
			self.CompletersTable.setItem(index,1,QTableWidgetItem(trainee.firstname.title()))
			self.CompletersTable.setItem(index,2,QTableWidgetItem(trainee.lastname.title()))
			self.CompletersTable.setItem(index,3,QTableWidgetItem(database.get_school_name_by_id(trainee.sid)))
			self.CompletersTable.setItem(index,4,QTableWidgetItem(trainee.email.lower()))
			self.CompletersTable.setItem(index,5,QTableWidgetItem(trainee.contact))
			self.CompletersTable.setItem(index,6,QTableWidgetItem(trainee.course))

	def populateDeletedTable(self):
		database = DatabaseManager()
		all_trainees = database.get_deleted_trainees()
		self.DeletedTable.setRowCount(len(all_trainees))
		for index,trainee in enumerate(all_trainees):		
			self.DeletedTable.setItem(index,0,QTableWidgetItem(trainee.id))
			self.DeletedTable.setItem(index,1,QTableWidgetItem(trainee.firstname.title()))
			self.DeletedTable.setItem(index,2,QTableWidgetItem(trainee.lastname.title()))
			self.DeletedTable.setItem(index,3,QTableWidgetItem(database.get_school_name_by_id(trainee.sid)))
			self.DeletedTable.setItem(index,4,QTableWidgetItem(trainee.email.lower()))
			self.DeletedTable.setItem(index,5,QTableWidgetItem(trainee.contact))
			self.DeletedTable.setItem(index,6,QTableWidgetItem(trainee.course))



			
			
			
	def show_approval_display(self):
		school_id_map = self.get_schoolId_schoolName_map()
		items = self.RegistryTbl.selectedItems()	
		if items:
			fullname = items[0].text().split(' ')
			firstname = fullname[0]
			lastname = fullname[1]
			email = items[1].text()
			contact = items[2].text()
			course = items[3].text()
			school = items[4].text()
			self.TraineeApprovalDisplay.show()	
			self.display1.setText(firstname)
			self.display2.setText(lastname)
			self.display3.setText(email)
			self.display4.setText(course)
			self.display5.setText(contact)
			self.display6.setText(school)

	def clear_textbox_in_add_school(self):
		self.SchoolIdAddInput.clear()
		self.SchoolNameAddInput.clear()
		self.SchoolAddressAddInput.clear()
		self.SchoolCoordinatorAddInput.clear()
		self.SchoolContactAddInput.clear()
		self.SchoolRequiredHoursInput.clear()
		self.School_Initials.clear()
		self.frame_35.hide()

	def toggle_school_frames(self):
		self.clear_textbox_in_add_school()
		
		self.SchoolIdAddInput.setFocus()
		self.SchoolTbl.clearSelection()
		self.frame_35.show()
		self.frame_36.hide()
		self.stackedWidget_4.setCurrentIndex(0)

	def set_txtbox_to_selected_school(self):
		database = DatabaseManager()
		self.frame_35.show()
		self.frame_36.hide()
		self.SchoolIdAddInput.setReadOnly(True)
		items = self.SchoolTbl.selectedItems()
		if items:
			self.stackedWidget_4.setCurrentIndex(1)
			self.SchoolIdAddInput.setText(items[0].text())
			self.SchoolNameAddInput.setText(database.get_school_name_by_id(items[0].text()))
			self.SchoolAddressAddInput.setText(items[2].text())
			self.SchoolCoordinatorAddInput.setText(items[3].text())
			self.SchoolContactAddInput.setText(items[4].text())
			self.SchoolRequiredHoursInput.setText(items[5].text())
			self.School_Initials.setText(items[1].text())
		else:
			QMessageBox.information(self,"Select Item","Select a school from the table",QMessageBox.Ok)

	def clear_selections_in_admin(self):
		self.RegistryTbl.clearSelection()
		self.SchoolTbl.clearSelection()
		self.frame_35.hide()
		self.TraineeApprovalDisplay.hide()
	def task_tab_changed(self):
		self.viewTaskTable.clearSelection()
		self.ongoingTaskTable.clearSelection()
		
		self.taskDoneBtn.hide()
		self.taskAbandoned.hide()
	
	

	def generate_unique_id(self):
		from Models.Database import DatabaseManager
		database = DatabaseManager()
		all_id = []
		trainees = database.get_trainees()
		while True:
			random_id = ''.join(random.choices(string.digits, k=8))
			if random_id not in all_id:
				return random_id

	def show_frame_34_36(self):
		self.frame_34.show()
		self.frame_36.show()

	def clickedDashboard(self):
	    self.stackedWidget_2.setCurrentIndex(0)
	    self.DashboardBtn.setStyleSheet("background-color: #007fff; color: #ffffff;")
	    self.TraineesBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.SchoolBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.Tasks.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.ProgressBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.Registry.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.adminSettingsBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.admin_dashboard_set_counts()

	def clickedTrainees(self):
	    self.stackedWidget_2.setCurrentIndex(1)
	    self.populateActiveTable()
	    self.tabWidget.setCurrentIndex(0)
	    self.TraineesBtn.setStyleSheet("background-color: #007fff; color: #ffffff;")
	    self.DashboardBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.SchoolBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.Tasks.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.ProgressBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.Registry.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.adminSettingsBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")



	def clickedSchool(self):
	    self.stackedWidget_2.setCurrentIndex(2)
	    self.SchoolBtn.setStyleSheet("background-color: #007fff; color: #ffffff;")
	    self.TraineesBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.DashboardBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.Tasks.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.ProgressBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.Registry.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.adminSettingsBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")

	def clickedTasks(self):
		self.taskDoneBtn.hide()
		self.taskAbandoned.hide()
		self.mainTaskTabWidget.setCurrentIndex(0)
		self.populate_view_task_table()
		self.populate_all_trainee_to_list_widget()
		self.stackedWidget_2.setCurrentIndex(3)
		self.Tasks.setStyleSheet("background-color: #007fff; color: #ffffff;")
		self.TraineesBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.DashboardBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.Registry.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.ProgressBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.adminSettingsBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.tasksTab.setCurrentIndex(0)
		self.populate_ongoing_task_table()

	def clickedProgressBtn(self):
		self.populate_trainee_table()
		self.populate_task_progress_table()
		self.TaskProgressTbl.clearSelection()
		self.frame_102.hide()
		self.tabWidget_4.setCurrentIndex(0)
		self.ProgressBtn.setStyleSheet("background-color: #007fff; color: #ffffff;")
		self.Tasks.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.TraineesBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.DashboardBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.Registry.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.adminSettingsBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.SchoolBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")

	def clickedRegistry(self):
		self.ProgressBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.Tasks.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.TraineesBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.DashboardBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.Registry.setStyleSheet("background-color: #007fff; color: #ffffff;")
		self.adminSettingsBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.SchoolBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
		self.RegistryTbl.clearSelection()
		self.TraineeApprovalDisplay.hide()

	def adminSettingsBtnClicked(self):
	    self.populate_general_settings_inputs()
	    self.stackedWidget_2.setCurrentIndex(4)
	    self.tabWidget_3.setCurrentIndex(0)
	    self.ProgressBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.Tasks.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.TraineesBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.DashboardBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.Registry.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	    self.adminSettingsBtn.setStyleSheet("background-color: #007fff; color: #ffffff;")
	    self.SchoolBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")

		
	# def clickedSchool(self):
	# 	self.stackedWidget_2.setCurrentIndex()
	# 	self.Tasks.setStyleSheet("background-color: #007fff; color: #ffffff;")
	# 	self.TraineesBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	# 	self.DashboardBtn.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")
	# 	self.Schedules.setStyleSheet("background-color: transparent; color: rgb(170, 170, 170);")	

	def handle_sort_school_change(self,index):
		if index == 0:
			self.SchoolTbl.sortItems(0)
		elif index == 1:
			self.SchoolTbl.sortItems(1)
		elif index == 2:
			self.SchoolTbl.sortItems(2)
		elif index == 3:
			self.SchoolTbl.sortItems(3)
		elif index == 4:
			self.SchoolTbl.sortItems(4)
		elif index == 5:
			self.SchoolTbl.sortItems(5)


	def displayNumLoginTrainee(self,buttonText):
		self.displayLabel.setText(self.displayLabel.text()+buttonText)

	def login_trainee_clicked(self):
		database = DatabaseManager()
		trainee_id = self.displayLabel.text().strip()
		if not database.is_trainee_status_complete(trainee_id):
			if trainee_id != "":
				if self.validateTraineeLogin(trainee_id):
					if not self.attendance_checked(trainee_id):#  if not logged in attendance for this day
						if not database.is_deleted_trainee(trainee_id):
							self.add_attendance(trainee_id)
							AlertDialog(self,"success","Attendance Recorded.. ").exec()
						else:
							AlertDialog(self,"error","Your Account is Deleted").exec()
						
					else:
						AlertDialog(self,"error","You already logged in for today..").exec()
						

				else:
					AlertDialog(self,"error","Trainee ID Not Found..").exec()
			else:
				AlertDialog(self,"error","Enter Your ID First").exec()
			self.displayLabel.setText("")
		else:
			AlertDialog(self,"error","You Already Completed The Training").exec()



			

	def logout_trainee_attendance(self):
		database = DatabaseManager()
		trainee_id =self.displayLabel.text()

		if trainee_id != "":
			if self.validateTraineeLogin(trainee_id):
				if not database.has_logged_out(trainee_id):

					success = database.logout_attendance(trainee_id)

					if success:
						AlertDialog(self,"success","Logging Out Attendance Sucessful").exec()
					else:
						AlertDialog(self,"error","Logging Out Failed").exec()
				else:
					AlertDialog(self,"error","You already log out").exec()
			else:
				AlertDialog(self,"error","Trainee Not Found").exec()
		else:
			AlertDialog(self,"error","Enter Your ID First").exec()

	def validateTraineeLogin(self,idNum):
		if idNum != "":
			database = DatabaseManager()
			trainee = database.get_trainee_by_id(idNum)
			return True if trainee else False
	def attendance_checked(self,trainee_id):
		database = DatabaseManager()
		return database.attendance_checked(trainee_id)


	def del_clicked(self):
		
		if len(self.displayLabel.text()):
			self.displayLabel.setText(self.displayLabel.text()[:-1])
	def resetClicked(self):
		self.displayLabel.setText("")

	def toggle_widescreen_school(self):
		if self.toolButton.isChecked():
			self.toolButton.setIcon(QIcon(":/icons/icons/fullscreen-exit-48.png"))
			self.frame_34.hide()
		else:
			self.toolButton.setIcon(QIcon(":/icons/icons/fullscreen-11-48.png"))
			self.frame_34.show()

	def admin_dashboard_set_counts(self):
		database = DatabaseManager()
		self.label_38.setText(str(database.count_school()))
		self.label_41.setText(str(database.count_trainees()))

	def set_progress(self,trainee_id):
		database = DatabaseManager()
		firstname,lastname = database.get_full_name_by_id(trainee_id)
		fullname = str(firstname) +" "+ str(lastname)
		total_hours_worked = database.get_trainee_total_hours_worked(trainee_id)
		required_hours = database.get_trainee_required_time(trainee_id)
		remaining_hours = int(required_hours) - int(total_hours_worked) 
		percent = self.get_worked_percentage(trainee_id)
		estimated_days = database.estimate_days(trainee_id)
	
		if percent == 100:
			first_stop,second_stop = 1,1
		elif percent < 1:
			first_stop,second_stop= 0.998,0.999
		else:
			percent_in_decimal = (100 - percent)/100.0
			first_stop = percent_in_decimal
			second_stop = percent_in_decimal + 0.01

		style = f"border-radius: 125px;background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{first_stop}rgba(63, 0, 95, 30), stop:{second_stop} rgb(163, 14, 255));"
		self.percent_number.setText(f"<p><span style='font-size:36pt;'>{percent}</span><span style='font-size:36pt; vertical-align:super;'>%</span></p>")
		self.progress.setStyleSheet(f"border-radius: 125px;background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{first_stop} rgba(63, 0, 95, 30), stop:{second_stop} #4778ff);");
		if int(required_hours) <= int(total_hours_worked):
			self.label_51.setText(f"{str(int(required_hours))} Hours")
			self.label_53.setText(f"{str(int(required_hours))} Hours")
			self.label_55.setText(f"{str('0')} Hours")
			self.label_49.setText(fullname.title())
			self.label_56.setText(f"{str(int(estimated_days))} Days")
			return


		self.label_51.setText(f"{str(int(total_hours_worked))} Hours")
		self.label_53.setText(f"{str(int(required_hours))} Hours")
		self.label_55.setText(f"{str(remaining_hours)} Hours")
		self.label_49.setText(fullname.title())
		self.label_56.setText(f"{str(int(estimated_days))} Days")

	def set_task_progress(self,trainee_id):
		database = DatabaseManager()
		total_tasks_taken = database.get_trainee_total_task_taken(trainee_id)
		total_tasks_completed = database.get_trainee_total_task_completed(trainee_id)
		total_late_tasks = database.get_trainee_total_late_tasks(trainee_id)
		total_abandoned = database.get_trainee_total_abandoned_tasks(trainee_id)

		self.label_83.setText(str(total_tasks_taken))
		self.label_84.setText(str(total_tasks_completed))
		self.label_85.setText(str(total_late_tasks))
		self.label_86.setText(str(total_abandoned))

		def compute_task_completion_rate():
			if total_tasks_taken == 0:
				rate = 0
			else:
				rate = int(((total_tasks_completed + total_late_tasks) / total_tasks_taken) * 100)
			return rate

		def compute_ontime_task_rate():
			if total_tasks_taken == 0:
				rate = 0
			else:
				rate = int((total_tasks_completed/total_tasks_taken) * 100)
			return rate
		def compute_late_task_rate():
			if total_tasks_taken == 0:
				rate = 0
			else:
				rate = int((total_late_tasks / total_tasks_taken) * 100)
			return rate

		self.progressBar.setValue(compute_task_completion_rate())
		self.progressBar_2.setValue(compute_ontime_task_rate())
		self.progressBar_3.setValue(compute_late_task_rate())






	
	def get_worked_percentage(self,trainee_id):
		database = DatabaseManager()
		total_hours_worked = database.get_trainee_total_hours_worked(trainee_id)

		trainee_required_time = database.get_trainee_required_time(trainee_id)
		percent = (total_hours_worked/trainee_required_time) * 100
		

		if percent > 100:
			percent = 100

		elif percent == 0:
			percent = 0;
		elif percent < 1:
			percent = round(((total_hours_worked/trainee_required_time) * 100),1);
		else:
			percent = int((total_hours_worked/trainee_required_time) * 100)

		
		return percent
	def ViewTraineesTblChangedSelection(self):
		items = self.ViewTraineesTbl.selectedItems()
		if items:
			trainee_id = items[0].text()
			self.set_progress_bar(trainee_id)

	def TaskProgressTblChanged(self):
		items = self.TaskProgressTbl.selectedItems()
		if items:
			trainee_id = items[0].text()
			self.set_task_progress(trainee_id)




	def update_clock(self):

		trainee_clock = datetime.datetime.now().strftime("%I:%M:%S %p %b-%d-%Y")
		admin_clock =  datetime.datetime.now().strftime("%I:%M:%S %p <p><span style='color:#fff; font-size:18px;'>%b-%d-%Y</span></p> ")

		self.label_25.setText(trainee_clock.upper())
		self.label_48.setText(admin_clock.upper())

	def slide_title(self):
		current_index = self.stackedWidget_5.currentIndex()
		next_index = current_index + 1
		if next_index == 3:
			next_index = 0
		self.stackedWidget_5.setCurrentIndex(next_index)

	def toggle_menu(self):
		if self.collapsable.isChecked():
			self.frame_23.setMinimumSize(90,0)
			self.frame_23.setMaximumSize(90,16777215)

			self.collapsable.setIcon(QIcon(":/icons/icons/arrow_right.png"))
		else:
			self.frame_23.setMinimumSize(300,0)
			self.frame_23.setMaximumSize(300,16777215)

			self.collapsable.setIcon(QIcon(":/icons/icons/arrow_left.png"))
	def logout_admin(self):
		Dialog(self,"logout").exec()
		self.adminState = None

	def force_log_out(self):
		
		database = DatabaseManager()
		force_time = database.get_force_logout_timestamp()
		if not self.force_logout_executed and  force_time <= datetime.datetime.now().time():
			database.force_log_out()
			self.force_logout_executed = True
			
		elif self.force_logout_executed and force_time > datetime.datetime.now().time():
			self.force_logout_executed = False
		else:
			pass #Handle this line
	

	#######TASKS#######

	def populate_all_trainee_to_list_widget(self):#populate list widget where admin pick trainee to assign task
		database = DatabaseManager()
		self.listWidget.clear()
		trainees_list = database.get_trainees()
		trainees_name = [(trainee.lastname +", "+ trainee.firstname) for trainee in trainees_list]
		for name in trainees_name:
			item = QListWidgetItem(name.title())
			item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
			item.setCheckState(Qt.Unchecked)
			self.listWidget.addItem(item)

	def add_new_task(self):
		database = DatabaseManager()
		checked_items = self.get_checked_item()
		if checked_items:
			if self.TaskTitle.text() != "":
				task = Task()
				task.title = self.TaskTitle.text().lower()
				task.description = self.TaskDescription.toPlainText()
				task.due = self.dueDate.date().toPyDate()
				task_id = database.add_new_task(task)
				for item in checked_items:
					fullname = item.split(", ")
					firstname = fullname[1]
					lastname = fullname[0]
					trainee_id = database.get_trainee_id_by_fullname(firstname,lastname)
					success = database.assign_task_to_trainee(task_id,trainee_id)
					if success:
						AlertDialog(self,"success","Added Task Successfully!!").exec()
						self.clear_after_create_task()
						self.populate_view_task_table()
						self.populate_ongoing_task_table()
			else:
				AlertDialog(self,"warning","Task Title is required").exec()
		else:
			AlertDialog(self,"warning","Select trainees to assign.").exec()
					



	def get_checked_item(self):
		checked_item = []
		for index in range(self.listWidget.count()):
			if self.listWidget.item(index).checkState() == Qt.Checked:
				checked_item.append(self.listWidget.item(index).text().lower())

		return checked_item



	def filter_list_widget(self):
		for i in range(self.listWidget.count()):
			item = self.listWidget.item(i)
			if self.filterListWidget.text() == "":
				item.setHidden(False)
			else:
				if self.filterListWidget.text().lower() in item.text().lower():
					item.setHidden(False)
				else:
					item.setHidden(True)
	def clear_after_create_task(self):
		self.TaskTitle.clear()
		self.TaskDescription.clear()
		self.dueDate.calendarWidget().setSelectedDate(QDate().currentDate())





	def populate_view_task_table(self):
		database = DatabaseManager()
		task_list = database.get_completed_tasks()
		self.viewTaskTable.setRowCount(len(task_list))
		for index, item in enumerate(task_list):
			item_title = QTableWidgetItem(item.title.title())
			item_date = QTableWidgetItem(str(item.due))
			item_title.setFlags(item_title.flags() & ~Qt.ItemIsEditable)
			item_date.setFlags(item_date.flags() & ~Qt.ItemIsEditable)
			self.viewTaskTable.setItem(index,0,QTableWidgetItem(str(index+1)))
			self.viewTaskTable.setItem(index, 1, item_title)
			self.viewTaskTable.setItem(index,2,item_date)
			self.viewTaskTable.setItem(index,3,QTableWidgetItem(str(database.get_task_status(database.get_task_id(item.title.lower(),item.due)))))
			
	def task_table_selection_changed(self):
		database = DatabaseManager()
		itemSelected = self.viewTaskTable.selectedItems()
		if itemSelected:
			task_id = database.get_task_id(itemSelected[1].text().lower().strip(), str(itemSelected[2].text()).strip())

			if task_id:
				task = database.get_task(task_id)
				if task:
					self.taskDescriptDisplay.setPlainText(task.description.capitalize())
			#set assign to list
			assigned_ids = database.get_assigned_task(task_id)
			self.taskAssignedListWidget.clear()
			
			self.taskAssignedListWidget.setRowCount(len(assigned_ids))
			self.taskAssignedListWidget.setHorizontalHeaderLabels(["Assigned","School"])
			if assigned_ids:
				for index,item in enumerate(assigned_ids):
					fullname = database.get_full_name_by_id(item)
					if fullname:	
						firstname = fullname[0]
						lastname = fullname[1]
					school_name = database.get_trainee_school_by_id(item)		
					
					self.taskAssignedListWidget.setItem(index,0,QTableWidgetItem(f"{lastname.title()}, {firstname.title()}"))
					self.taskAssignedListWidget.setItem(index,1,QTableWidgetItem(school_name.title()))
	def ongoing_task_table_selection_changed(self):
		if len(self.ongoingTaskTable.selectedItems()) <= 0:
			self.taskDoneBtn.hide()
			self.taskAbandoned.hide()
		else:
			self.taskDoneBtn.show()
			self.taskAbandoned.show()
		database = DatabaseManager()
		itemSelected = self.ongoingTaskTable.selectedItems()
		if itemSelected:
			task_id = database.get_task_id(itemSelected[1].text().lower().strip(), str(itemSelected[2].text()).strip())

			if task_id:
				task = database.get_task(task_id)
				if task:
					self.taskDescriptDisplay.setPlainText(task.description.capitalize())
			#set assign to list
			assigned_ids = database.get_assigned_task(task_id)
			self.taskAssignedListWidget.clear()
			
			self.taskAssignedListWidget.setRowCount(len(assigned_ids))
			self.taskAssignedListWidget.setHorizontalHeaderLabels(["Assigned","School"])
			if assigned_ids:
				for index,item in enumerate(assigned_ids):
					fullname = database.get_full_name_by_id(item)
					if fullname:
						firstname =fullname[0]
						lastname = fullname[1]
					school_name = database.get_trainee_school_by_id(item)
					
						#f"<p><span style=' font-weight:600; color:#17e9e1;'>{database.get_assigned_task_status(task_id)}</span></p>" + "\t" + 
					
					
					self.taskAssignedListWidget.setItem(index,0,QTableWidgetItem(f"{lastname.title()}, {firstname.title()}"))
					self.taskAssignedListWidget.setItem(index,1,QTableWidgetItem(school_name.title()))


	def populate_ongoing_task_table(self):
		database = DatabaseManager()
		task_list = database.get_ongoing_tasks()
		self.ongoingTaskTable.setRowCount(len(task_list))	
		for index, item in enumerate(task_list):
			item_title = QTableWidgetItem(item.title.title())
			item_date = QTableWidgetItem(str(item.due))
			item_title.setFlags(item_title.flags() & ~Qt.ItemIsEditable)
			item_date.setFlags(item_date.flags() & ~Qt.ItemIsEditable)
			self.ongoingTaskTable.setItem(index,0,QTableWidgetItem(str(index+1)))
			self.ongoingTaskTable.setItem(index,1,item_title)
			self.ongoingTaskTable.setItem(index,2,item_date)
			self.ongoingTaskTable.setItem(index,3,QTableWidgetItem(str(database.get_task_status(database.get_task_id(item.title.lower(),item.due)))))



	def taskDoneBtnClicked(self):
		database = DatabaseManager()
		selected = self.ongoingTaskTable.selectedItems()
		if selected:
			task_title = selected[1].text().lower()
			task_due = selected[2].text()
			progress = selected[3].text().lower()
			if progress == 'ongoing':
				done = database.set_task_done(task_title,task_due)
				if done:
					
					AlertDialog(self,"success","Task Status Updated!").exec()
					self.populate_view_task_table()
					self.populate_ongoing_task_table()
				else:
					AlertDialog(self,"error","Error Updating Task Status.").exec()
		else:
			print("no selected")

	def abandonTaskClicked(self):
		database = DatabaseManager()
		selected = self.ongoingTaskTable.selectedItems()
		if selected:
			task_title = selected[1].text().lower()
			task_due = selected[2].text()
			progress = selected[3].text().lower()
			if progress == 'ongoing':
				done = database.set_task_abandoned(task_title,task_due)
				if done:		
					AlertDialog(self,"success","Task Abandoned!").exec()
					self.populate_view_task_table()
					self.populate_ongoing_task_table()
				else:
					AlertDialog(self,"error","Error Updating Task Status.").exec()
		else:
			print("no selected")



	#USERS SIDE
	def userSideSeeTasksBtnClicked(self):
		database = DatabaseManager()
		if not database.is_trainee_status_complete(self.displayLabel.text().strip()):

			if self.validateTraineeLogin(self.displayLabel.text().strip()):
				if not database.is_deleted_trainee(self.displayLabel.text().strip()):
					self.state = State(str(self.displayLabel.text().strip()))
					self.populate_userSideNewTaskTable(self.state.data)
					self.populate_userSideCompletedTaskTable(self.state.data)
					self.populateMissedTaskTable(self.state.data)
					self.stackedWidget_3.setCurrentIndex(1)
					self.backButton.hide()
					self.backButton_2.show()
					self.RegisterNewBtn.hide()
					fname = database.get_full_name_by_id(self.state.data)
					firstname = fname[0]
					lastname = fname[1]


					self.label_27.setText(f"{lastname.title()}, {firstname.title()}")
					
				else:
					AlertDialog(self,"error","Your Account is Deleted").exec()
			else:
				AlertDialog(self,"error","Trainee not found!").exec()
		else:
			AlertDialog(self,"error","You Already Completed Training").exec()

	def populate_userSideNewTaskTable(self,trainee_id):
		database = DatabaseManager()
		tasks = database.get_trainee_new_tasks(trainee_id)
		self.userSideNewTaskTable.setRowCount(len(tasks))
		if len(tasks) <= 0:
			self.label_97.hide()
		else:
			self.label_97.show()
		self.label_97.setText(str(len(tasks)))
		for index,task in enumerate(tasks):
			self.userSideNewTaskTable.setItem(index, 0, QTableWidgetItem(task.title))
			self.userSideNewTaskTable.setItem(index, 1, QTableWidgetItem(str(task.due)))
			self.userSideNewTaskTable.setItem(index, 2, QTableWidgetItem(str(task.description)))


	def toggleDeleteTraineeBtn(self):
		if len(self.ManageTraineesTbl.selectedItems()) > 0:
			self.deleteTraineeBtn.show()
		else:
			self.deleteTraineeBtn.hide()

	def deleteTraineeClicked(self):
		if QMessageBox.question(self, 'Warning', "This action cannot be undone\nDo you want to delete this student?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:	
			selected_items = self.ManageTraineesTbl.selectedItems()
			trainee_id = selected_items[0].text()
			try:
				database = DatabaseManager()
				success = database.set_trainee_deleted(trainee_id)
				if success:
					AlertDialog(self,"success","Successfully Deleted Trainee!")
					self.populate_manage_traines_table()
					self.populateDeletedTable()
			except Exception as e:
				raise e

	def populate_userSideCompletedTaskTable(self,state):
		database = DatabaseManager()
		tasks = database.get_trainee_completed_tasks(state)
		if tasks:
			self.userSideCompletedTaskTable.setRowCount(len(tasks))
			for index,obj in enumerate(tasks):
				self.userSideCompletedTaskTable.setItem(index,0,QTableWidgetItem(obj.title))
				self.userSideCompletedTaskTable.setItem(index,1,QTableWidgetItem(obj.description))

	def backButton_2Clicked(self):
		self.state = None
		self.stackedWidget_3.setCurrentIndex(0)
		self.backButton_2.hide()
		self.backButton.show()
		self.RegisterNewBtn.show()


	def change_admin_credentials(self):
		database = DatabaseManager()
		success = database.change_admin_login_credentials(self.changeUsernameField.text().strip(),self.changePasswordField.text(),self.adminState.data)
		if success:
			AlertDialog(self,"success","Admin Credentials Changed Successfully!").exec()
			self.changeUsernameField.setText("")
			self.changePasswordField.setText("")

	def saveChangesChangeCredentialsBtnClicked(self):
		if QMessageBox.question(self,"Confirm","Confirm Changes?",QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
			self.change_admin_credentials()
			self.stackedWidget.setCurrentIndex(0)
			self.adminState = None

	def changeCompanyNameBtnClicked(self):
		self.companyNameInput.setReadOnly(False)
		self.companyNameInput.setFocus()
	def regTimeInBtnClicked(self):
		self.regTimeIn.setReadOnly(False)
		self.regTimeIn.setFocus()

	def regTimeOutBtnClicked(self):
		self.regTimeOut.setReadOnly(False)
		self.regTimeOut.setFocus()
	def autoLogOutBtnClicked(self):
		self.autoLogOut.setReadOnly(False)
		self.autoLogOut.setFocus()
	def populate_general_settings_inputs(self):
		database = DatabaseManager()
		company = database.get_company_name()
		reg_time_in_str = database.get_reg_time_in()
		reg_time_out_str = database.get_reg_time_out()
		auto_log_out = str(database.get_force_logout_timestamp())
		print(auto_log_out)
		hour, minute, second = map(int, auto_log_out.split(':'))

		# Create a QTime object using the extracted values
		auto_out = QTime(hour, minute)

		
		reg_time_in_time = datetime.datetime.strptime(reg_time_in_str,"%H:%M:%S")
		reg_time_in_formatted = reg_time_in_time.strftime("%I:%M %p")		

		reg_time_out_time = datetime.datetime.strptime(reg_time_out_str,"%H:%M:%S")
		reg_time_out_formatted = reg_time_out_time.strftime("%I:%M %p")
		time_in = QTime.fromString(reg_time_in_formatted, "hh:mm AP")
		time_out = QTime.fromString(reg_time_out_formatted, "hh:mm AP")
		
		# formatted_time = time_obj.strftime("%-I:%M %p")
		print(reg_time_in_formatted)

		if company:
			self.companyNameInput.setText(company.upper())
		if reg_time_in_str:
			self.regTimeIn.setTime(time_in)
		if reg_time_out_str:
			self.regTimeOut.setTime(time_out)
		if auto_log_out:
			self.autoLogOut.setTime(auto_out)


	def saveGeneralSettingsClicked(self):
		new_reg_in = self.regTimeIn.time().toString("HH:mm:ss")
		new_reg_out = self.regTimeOut.time().toString("HH:mm:ss")
		new_company = self.companyNameInput.text().lower()
		database = DatabaseManager()
		database.save_new_auto_log_out(self.autoLogOut.time().toString("h:mm AP"))
		database.save_new_reg_time_in(new_reg_in)
		database.save_new_reg_time_out(new_reg_out)
		database.save_new_company_name(new_company)
		self.populate_general_settings_inputs()
		AlertDialog(self,"success","Saving Changes Successful!").exec()

	def selectAllListWidget(self,checkbox,listWidget):
		if checkbox.isChecked():
			for i in range(listWidget.count()):
				listWidget.item(i).setCheckState(Qt.Checked)
		else:
			for i in range(listWidget.count()):
				listWidget.item(i).setCheckState(Qt.Unchecked)

	def restore_trainee(self):
		if QMessageBox.question("Confirm","Do you want to restore this trainee?",QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
			selected = self.DeletedTable.selectedItems()
			if selected:
				trainee_id = selected[0].text()
				try:
					database = DatabaseManager()
					restored = database.restore_trainee(trainee_id)
					if restored:
						AlertDialog(self,"success","Trainee Restored Successfully!").exec()
						self.populateDeletedTable()
						self.populate_manage_traines_table()
					else:
						AlertDialog(self,"error","Restoring Trainee Failed!").exec()
				except Exception as e:
					raise e

	def confirmPasswordEnterClicked(self):
		database = DatabaseManager()
		password = database.get_admin_password(self.adminState.data)
		if self.confirmPasswordLine.text() == password:
			self.frame_97.show()
		else:
			AlertDialog(self,"error","Wrong Password...").exec()

	def add_new_admin(self):
		database =DatabaseManager()
		fname = self.newAdminFirstname.text().lower().strip()
		lname = self.newAdminLastname.text().lower().strip()
		username = self.newAdminUsername.text()
		password = self.newAdminPassword.text()
		if fname and lname and username and password:
			response = database.add_new_admin([fname,lname,username,password])
			if response:
				AlertDialog(self,"success","Admin Successfully Added!").exec()
				self.frame_127.hide()
				self.frame_97.hide()
			else:
				AlertDialog(self,"error","Error Adding Admin Account").exec()
		else:
			AlertDialog(self,"error","All Fields Are Required").exec()

	def restore_all(self):
		if QMessageBox.question(self,"Confirm","Proceed Restoring All Trainees?",QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
			database = DatabaseManager()
			response = database.restore_all()
			if response:
				AlertDialog(self,"success","All Trainees Restored Successfully! ").exec()
				self.populate_manage_traines_table()
				self.populateDeletedTable()
			else:
				AlertDialog(self,"error","There is an error restoring all trainees")
	def clear_deleted(self):
		if QMessageBox.question(self,"Confirm","This action cannot be undone.\nAll deleted trainees will be permanently deleted.",QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
			database = DatabaseManager()
			response = database.clear_all()
			if response:
				AlertDialog(self,"success","Delete Trainees Cleared").exec()
				self.populate_manage_traines_table()
				self.populateDeletedTable()
			else:
				AlertDialog(self,"error","There is an error clearing all deleted trainees")


	def toggle_password_visibility(self):

		if self.toolButton_2.isChecked():
			self.adminPassword.setEchoMode(QLineEdit.Normal)
			self.toolButton_2.setIcon(QIcon(":/icons/icons/eye.png"))
			
		else:
			self.adminPassword.setEchoMode(QLineEdit.Password)
			self.toolButton_2.setIcon(QIcon(":/icons/icons/icons8-closed-eye-48.png"))
	def populateActiveTable(self):
		database = DatabaseManager()
		active = database.get_active()
		if active:
			self.ActiveTable.setRowCount(len(active))
			for index,obj in enumerate(active):
				self.ActiveTable.setItem(index,0,QTableWidgetItem(obj[0]))
				self.ActiveTable.setItem(index,1,QTableWidgetItem(obj[1]))
				self.ActiveTable.setItem(index,2,QTableWidgetItem(obj[2]))
				self.ActiveTable.setItem(index,3,QTableWidgetItem(obj[3]))
				self.ActiveTable.setItem(index,4,QTableWidgetItem("Active"))

	def populateMissedTaskTable(self,trainee_id):
		database = DatabaseManager()
		missed = database.get_trainee_missed_task(trainee_id)
		if missed:
			self.userSideMissedTaskTable.setRowCount(len(missed))
			for index,obj in enumerate(missed):
				self.userSideMissedTaskTable.setItem(index,0,QTableWidgetItem(obj[2]))
				self.userSideMissedTaskTable.setItem(index,1,QTableWidgetItem(obj[3]))
				self.userSideMissedTaskTable.setItem(index,2,QTableWidgetItem(str(obj[4])))
				self.userSideMissedTaskTable.setItem(index,3,QTableWidgetItem("Missed"))


			













			




	




















