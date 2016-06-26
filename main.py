'''
The main file into which all relevant modules are imported and
from where they are called.
'''
from Tkinter import *
import sys
from copy import deepcopy

import task_class
import graphics
import fade_out_notification
import encrypt as enc
from file_editing import *
from datetime import date

# Create root Tk instance
root = Tk()

# Make sure that no window is drawn for the root Tk() instance.
root.withdraw()

# MARK: Authentication
# This section handles the authentication at the beginning of every session.

# Storage & encryption of the users password in Encrypt.py

# Password user enters
input = ""

# Called when user closes a window.
def cleanUp():
	task_class.saveAndCloseShelf()
	root.destroy()

# Function that is called when user enters password
# Checks if input matches user_password and either exits or
# shows fade out notification
def submitPassword():
		# Get the text inputted into the password field.
		input = passwordField.get()

		# Salt and hash the input and compare to the password
		# If password correct, destroy the window and begin the configuration process
		if enc.saltAndHash(input) == enc.user_password:
			isVerified = True
			print "Correct password entered."
			authWin.destroy()
			# print task_class.returnShelfForToday()
			if task_class.returnShelfForToday() != False and task_class.returnShelfForToday()['Mechanic'].content != '':
				shelfFile = task_class.returnShelfForToday()

				def loadTasks():
					for index in range(0, len(shelfFile)):
						task_class.tasks[index] = shelfFile[task_class.tasks[index].label]
					loadWin.destroy()
					runWin()

				def noLoad():
					loadWin.destroy()
					runWin()

				loadWin = Toplevel(root)
				loadWin.protocol('WM_DELETE_WINDOW', cleanUp)

				loadWin.title("Load Data from old sessions")
				loadWin.minsize(width=222, height=222)

				labelText = "Do you want to load %s's data from %s?" %(shelfFile['Mechanic'].content, shelfFile['Date'].content)
				label = Label(loadWin, text=labelText, font=graphics.getBigRepFont(loadWin, 15))
				label.grid(row=0, column=0, sticky=N, pady=20, padx=20)

				yesButton = Button(loadWin, text="Yes", command=loadTasks)
				yesButton.grid(row=1, column=0, pady=30, sticky=W, padx=20)
				noButton = Button(loadWin, text="No", command=noLoad)
				noButton.grid(row=1, column=1, pady=30, sticky=E, padx=20)

				graphics.centerWindow(loadWin)

				root.mainloop()
			else: runWin()
		# If password incorrect, show fade out notification and clear field.
		else:
			isVerified = False
			print "Password entered is incorrect."
			passwordField.delete(0, 'end')
			fade_out_notification.present(root, "The password you entered is incorrect. Try again.", 300)

globalProgress = 0

# Create the authenticatino window, title it and create label and input field.
authWin = Toplevel()

authWin.title("Authentication")
authWin.minsize(width=222, height=222)
welcomeLabel = Label(authWin, text="WELCOME TO THE BIGREP CONFIGURATION \n GRAPHICAL USER INTERFACE", font=graphics.getBigRepFont(authWin, 30))
welcomeLabel.grid(row=0, column=0, sticky=N, columnspan=4, pady=20, padx=20)

passwordPrompt = Label(authWin, text="Input password to unlock: ")
passwordPrompt.grid(row=1, column=0, pady=50, sticky=W, padx=20)
passwordField = Entry(authWin, width=40, show="*")
passwordField.grid(row=1, column=1, padx=10, pady=5)
passwordField.focus_set()
submitButton = Button(authWin, text="Login", command=submitPassword)
submitButton.grid(row=1, column=3, sticky=W, padx= 20)
authWin.protocol('WM_DELETE_WINDOW', cleanUp)

graphics.centerWindow(authWin)

# TD: Should submit when return key hit.
# authWin.bind("<Return>", submitPassword())

''' 
Save a text file with SOMENAME (like Backup or so) and date & time stamp.
When starting program, look for file with SOMENAME (and most recent date) 
and load data from there into UI.
'''
#This is the image of BigRep's logo that will be displayed in every window.
photo = PhotoImage(file="Logo.pgm").subsample(5)

# TD: Create log of logins

def runWin(progress=0):

	def cleanUpAndSave():
		saveAndClose()

		signWin = Toplevel(root)
		signWin.wm_title("Setup Process Completed")
		signWin.minsize(width=600, height=300)
		signWin.protocol('WM_DELETE_WINDOW', cleanUp)

		graphics.centerWindow(signWin)

		def finalize():
			# TD: Implement custom save for the initials and date.
			saveAsPDF()
			signWin.destroy()
			root.destroy()

			# TD: Save as pdf, send as email
			

		datePrompt = Label(signWin, text="Enter the date here: ")
		datePrompt.grid(row=2, column=1)

		dateEntry = Entry(signWin, width=20, text=str(date.today()))
		dateEntry.grid(row=2, column=2, padx=20, pady=20)

		signaturePrompt = Label(signWin, text="Sign your initials here: ")
		signaturePrompt.grid(row=1, column=1)

		signature = Entry(signWin, width=20)
		signature.grid(row=1, column=2, padx=20, pady=20)

		button = Button(signWin, text='Finish & Submit', width=50, command=finalize)
		button.grid(row=3, column=1, columnspan=2, padx=10, pady=20)

	globalProgress = progress

	# Creates the window.
	MainWin = Toplevel(root)

	#Makes window the size of the screen.
	MainWin.minsize(width=600, height=300)

	# Window setup
	MainWin.wm_title("BigRep Printer Configuration")

	# TD: Call endConfiguration (implemented in file_editing) when window closed.
	MainWin.protocol('WM_DELETE_WINDOW', cleanUp)
	# Put the BigRep Logo into the window.
	Label(MainWin, image=photo).grid(row=0, column=1, pady=20)

	# Go back to the previous page
	def goBack():
		saveAndClose()
		runWin(globalProgress-task_class.groupSize)

	if progress > 0:
		# Back button
		Button(MainWin, text="Back", command=goBack).grid(row=0, column=0)

	# Add the label to the window.
	Label(MainWin, text="Configuration UI", font=graphics.getBigRepFont(MainWin, 50)).grid(row=0, column = 2)
	'''
	# Gets the configuration file by its name and updates the measurement value by its parameter. 
	# TD: Should be called when doc is exported to pdf/process is completed. 
	# OR: Part of testing & needs to be called immediately?
	def updateValueInFile(value):

		filename = ""

		target = open(filename, 'r')

		contents = target.read()

		target.close()

		# Update with actual contents
		toFind = ""

		# Code to find & modify spot in file
		index = contents.find(toFind, beg=0, end=len(toFind))

		contents = contents[:index] + value + contents[index + len(toFind):]

		# Overwrite file
		target = open(filename, 'w')

		target.write(contents)
	'''
	# Gets current tasks
	tasks = task_class.tasks[progress:progress+task_class.groupSize]
	for task in tasks:
		print 'Current tasks are %s' %task.label

	contentFields = []

	def saveAndClose():
		entryIndex = 0
		for index in range(0, len(tasks)):
			if tasks[index].type == 'Entry':
				task_class.tasks[progress + index].content = contentFields[entryIndex].get()
				entryIndex += 1
		MainWin.destroy()

	# Code to finish up progress when finished with all tasks.
	if len(tasks) == 0:
		print 'Done with tasks!'
		print "Here's what I've noted down:"
		for task in task_class.tasks:
			if task.content != '':
				print '%s: %s' %(task.label, task.content)
			if hasattr(task, 'errorMessage'):
				print '%s: Error Message: %s' %(task.label, task.errorMessage)
			if hasattr(task, 'completionStatus'):
				print '%s: Task completed? %r' %(task.label, task.completionStatus)
		cleanUpAndSave()
		# sys.exit()

	# Create window layout as grid
	for r in range(len(tasks)):
		row = r+1
		label = Label(MainWin, text=tasks[r].label).grid(row=row,column=1, sticky=W)
		if tasks[r].type == 'Entry':
			content = Entry(MainWin, width=40)
			content.grid(row=row, column=2, sticky=W, padx=20)
			content.insert(0, tasks[r].content)
			contentFields += [content]
			
		elif tasks[r].type == 'Procedure':
			
			# Function that looks at the cmopletionStatus of the current
			# Task and changes it based on that.
			def changeCompletionStatus(index):
				print "index at beginning of changing completion status is %s" %index
				if tasks[index].completionStatus == True:
					task_class.tasks[progress+index].completionStatus = False
				else:
					task_class.tasks[progress+index].completionStatus = True

			if hasattr(tasks[r], 'function'):
				executeFunction = Button(MainWin, text="Begin testing", command=tasks[r].function)
				executeFunction.grid(row=row, column=2, sticky=W, padx=20)
			else:
				# Create label
				label = Label(MainWin, text="Check to complete:")
				label.grid(row=row, column=2, sticky=W, padx=20)
			
			# Creation of checkbox and set it based on completionStatus
			checkbox = Checkbutton(MainWin, command= lambda r=r: changeCompletionStatus(r))
			checkbox.grid(row=row, column=2, padx=20)
			if tasks[r].completionStatus == True:
				checkbox.select()

			#Function that creates the error button
			# and leads to error screen and propagates error back to task_class
			def registerError(index):
				print 'error index: %s' %index
				saveAndClose()
				# close screen
				MainWin.destroy()
				# create new screen that has text for error message
				newWin = Toplevel(root)
				# Window setup
				newWin.wm_title("Register Error")
				newWin.minsize(width=800, height=300)
				newWin.protocol('WM_DELETE_WINDOW', cleanUp)
				graphics.centerWindow(newWin)

				# get error message inputted and send back to task_class
				def propagateError():
					# create error message ettribute for task and get entered text
					task_class.tasks[progress+index].registerError(message.get(1.0,END))
					newWin.destroy()
					if hasattr(task_class.tasks[progress+index], 'errorFunction'):
						errorWin = Toplevel(root)
						errorWin.wm_title("Handling Error")
						errorWin.minsize(width=800, height=300)
						errorWin.protocol('WM_DELETE_WINDOW', cleanUp)
						graphics.centerWindow(errorWin)

						errorMessage = Label(errorWin, text="Thank you for registering that error. We will now proceed to mitigate it")
						errorMessage.grid(row=1, column=1, padx=20, pady=20)
					else: runWin(progress)

				# Cancel's the error and returns to 
				def cancelError():
					newWin.destroy()
					runWin(progress)

				label = Label(newWin, text='Enter the error message \n and any other details here:')
				label.grid(row=1, column=0, sticky=E, pady=20, padx=20)
				message = Text(newWin, width=50, height=5)
				message.grid(row=1, column=1, sticky=W, pady=20)
				message.focus_set()
				if hasattr(tasks[r], 'errorMessage'):
					message.insert(1.0, tasks[r].errorMessage)

				complete = Button(newWin, text='Finish', command=propagateError)
				complete.grid(row=1, column=2, sticky=E, pady=20)
				cancel = Button(newWin, text='Cancel', command=cancelError)
				cancel.grid(row=0, column=0, sticky=W)

			errorButton = Button(MainWin, text="Click if error", command= lambda r=r:registerError(r))
			errorButton.grid(row=row, column=2, sticky=E, padx=20)

	def onButtonClick():
		saveAndClose()
		for task in tasks:
			if task.checkContent() == False:
				errMess = "Your entry for '%s' is incorrect. Please review formatting and resubmit!" %task.label
				runWin(progress)
				fade_out_notification.present(root, errMess, 600)
				return
				print "We have a problem."
		runWin(progress + task_class.groupSize)
	
	button = Button(MainWin, text="Next", command=onButtonClick)
	button.grid(row=progress+task_class.groupSize+1, column=2, sticky = W, pady=20, padx=20)
	
	for c in range(2):
		MainWin.columnconfigure(c, minsize=100)
	
	graphics.centerWindow(MainWin)

root.mainloop()