from datetime import date

'''
This file handles the backend datastructure of tasks.
'''
groupSize = 2
class Task:

	label = ""

	content = ""
	'''
	rank = 1

	nextLocation = 1

	completeStatus = False

	def showInfo():
		# Display further information
		print("showInfo")

	def complete(self):
		# Animate checking of checkmark/ image replacement
		# 
		print("completing: %s with ID:" %self.label)
		print(self.rank)
	'''
	def __init__(self, label, content=''):
		self.label = label
		self.content = content

# All tasks are instances of the Task class and members of the tasks array:

tasks = [Task("Date", str(date.today()))]

tasks.append(Task("Mechanic"))

tasks.append(Task("Company Name"))
'''
tasks.append(Task("Printer Serial Number (SN)"))

tasks.append(Task("Switch Cabinet SN"))

tasks.append(Task("Left Extruder SN"))

tasks.append(Task("Right Extruder SN"))

tasks.append(Task("X-Y Frame SN"))

tasks.append(Task("Type"))

tasks.append(Task("Userinterface"))

tasks.append(Task("Software last updated on"))

tasks.append(Task("Firmware version"))
'''
