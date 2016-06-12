'''
The main file into which all relevant modules are imported and
from where they are called.
'''
from Tkinter import *
import sys

import TaskClass
import Graphics
import FadeOutNotification
import Encrypt as enc

# Create root Tk instance
root = Tk()

# Make sure that no window is drawn for the root Tk() instance.
root.withdraw()

# MARK: Authentication
# This section handles the authentication at the beginning of every session.

# Storage & encryption of the users password in Encrypt.py

# Password user enters
input = ""

# Function that is called when user enters password
# Checks if input matches user_password and either exits or
# shows FadeOutNotification
def submitPassword():
		input = passwordField.get()

		if enc.saltAndHash(input) == enc.user_password:
			isVerified = True
			print "Correct password entered."
			authWin.destroy()
			runWin()
		else:
			isVerified = False
			print "Password entered is incorrect."
			passwordField.delete(0, 'end')
			# TD: Implement without creating new Tk() instance
			FadeOutNotification.present(root, "The password you entered is incorrect. Try again.", 300)

# Called when user closes authentication window.
def cleanUp():
	#Create pdf.
    root.destroy()

authWin = Toplevel()

authWin.title("Authentication")
authWin.minsize(width=222, height=222)
welcomeLabel = Label(authWin, text="WELCOME TO THE BIGREP CONFIGURATION \n GRAPHICAL USER INTERFACE", font=Graphics.getBigRepFont(authWin, 30))
welcomeLabel.grid(row=0, column=0, sticky=N, columnspan=4, pady=20, padx=20)

passwordPrompt = Label(authWin, text="Input password to unlock: ")
passwordPrompt.grid(row=1, column=0, pady=50, sticky=W, padx=20)
passwordField = Entry(authWin, width=40)
#TD: Make entry secret
passwordField.grid(row=1, column=1, padx=10, pady=5)
submitButton = Button(authWin, text="Login", command=submitPassword)
submitButton.grid(row=1, column=3, sticky=W, padx= 20)
authWin.protocol('WM_DELETE_WINDOW', cleanUp)

Graphics.centerWindow(authWin)

# TD: Should submit when return key hit.
# authWin.bind("<Return>", submitPassword())
	
# How to save progress in case window closed, device crashes???
''' 
Save a text file with SOMENAME (like Backup or so) and date & time stamp.
When starting program, look for file with SOMENAME (and most recent date) 
and load data from there into UI.
'''
#This is the image of BigRep's logo that will be displayed in every window.
photo = PhotoImage(file="Logo.pgm").subsample(5)

# Create log of logins

def runWin(progress=0):

	MainWin = Toplevel(root)

	# Window setup
	MainWin.wm_title("BigRep Printer Configuration")

	#Makes window the size of the screen.
	MainWin.minsize(width=MainWin.winfo_screenwidth(), height=MainWin.winfo_screenheight())

	MainWin.protocol('WM_DELETE_WINDOW', cleanUp)

	Label(MainWin, image=photo).grid(row=0, column=1)

	Label(MainWin, text="Configuration UI", font=Graphics.getBigRepFont(MainWin, 50)).grid(row=0, column = 2)
	

	# Gets the configuration file by its name and updates the measurement value by its parameter. 
	# Should be called when doc is exported to pdf/process is completed. 
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

	tasks = TaskClass.tasks[progress:progress+TaskClass.groupSize]

	contentFields = []

	# Code to finish up progress when finished with all tasks.
	if len(tasks) == 0:
		print 'Done with tasks!'
		cleanUp()
		sys.exit()

	# Create window layout as grid
	for r in range(len(tasks)):
		row = r+1
		label = Label(MainWin, text=tasks[r].label).grid(row=row,column=1, sticky=W)
		content = Entry(MainWin, width=40)
		content.grid(row=row, column=2, sticky=W)
		content.insert(0, tasks[r].content)
		contentFields += [content]
		#MainWin.rowconfigure(r, minsize=MainWin.winfo_height/len(tasks))
	    #MainWin.columnconfigure(1, minsize=MainWin.winfo_width/2)

	def onButtonClick():
		print 'Button clicked!'
		for num in range(0, TaskClass.groupSize-1):
			TaskClass.tasks[progress + num] = contentFields[num].get()
		MainWin.destroy()
		runWin(progress+2)
	
	button = Button(MainWin, text="Next", command=onButtonClick)
	button.grid(row=progress+TaskClass.groupSize+1, column=2, sticky = W)
	
	for c in range(2):
		MainWin.columnconfigure(c, minsize=100)
	
	Graphics.centerWindow(MainWin)

root.mainloop()