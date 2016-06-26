from datetime import date
import re
import shelve

import file_editing

'''
This file handles the backend datastructure of tasks.
'''

# Open shelfFile
shelfFile = shelve.open('tasks')
# print list(shelfFile.keys())

def returnShelfForToday():
	if shelfFile["Date"].content == str(date.today()):
		print 'Found a shelf for today'
		return shelfFile
	else: return False

def saveAndCloseShelf():
	print 'Saving and closing shelf'
	for task in tasks:
		shelfFile[task.label] = task
	shelfFile.close()

# Maximum 4, otherwise update checkbox creation code in main.py
groupSize = 3

# The Task class
class Task:

	label = ""

	content = ""
	'''
	TD:
	def showInfo():
		# Display further information
		print("showInfo")
	'''
	def registerError(self, errorMessage=''):
		self.errorMessage = errorMessage
		if hasattr(self, 'errorFunction'):
			self.errorFunction()
		print 'Error registered.'

	def checkContent(self, contentChecker=0):
		if self.contentChecker != 0:
			return self.contentChecker(self)
		elif hasattr(self, 'completionStatus'):
			return isCompleted(self)
		else:
			return notEmpty(self)

	def __init__(self, label, content='', type='Entry', function=0, errorFunction=0, contentChecker=0):
		self.label = label
		self.type = type
		self.contentChecker = contentChecker

		self.content = content

		if self.type == 'Procedure':
			self.completionStatus = False

		if function != 0:
			self.function = function
		if errorFunction != 0:
			self.errorFunction = errorFunction		

# Here are all the content checking functions:
def notEmpty(task):
	print "Checking for not empty in the task %s's input:" %task.label
	print task.content

	if task.content == '':
		return False
	else: return True

def hasNumber(task):
	print "Checking for number in the task %s's input:" %task.label
	print task.content

	hasNumberRegex = re.compile(r'\d')
	if hasNumberRegex.match(task.content):
		return True
	else: return False

def onlyNumber(task):
	hasNumberRegex = re.compile(r'^(\d)*$')
	if hasNumberRegex.match(task.content):
		return True
	else: return False

def noNumber(task):
	print "Checking for no numbers in the task %s's input:" %task.label
	print task.content

	# Make sure entry isn't empty
	if notEmpty(task) == False:
		return False

	hasNumberRegex = re.compile(r'\d')
	if hasNumberRegex.search(task.content):
		return False
	else: return True

def hasDate(task):
	print "Checking for only date in the task %s's input:" %task.label
	print task.content

	hasNumberRegex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
	if hasNumberRegex.search(task.content):
		return True
	else: return False

def isCompleted(task):
	if hasattr(task, 'completionStatus'):
		return task.completionStatus
	# TD: Check completionstatus and return true if completed, else false

# All tasks are instances of the Task class and members of the tasks array:

tasks = [Task("Date", str(date.today()), contentChecker=hasDate)]

tasks.append(Task("Mechanic", contentChecker=noNumber))

tasks.append(Task("Company Name"))
'''
tasks.append(Task("Printer Serial Number (SN)", contentChecker=hasNumber))

tasks.append(Task("Switch Cabinet SN", contentChecker=))

tasks.append(Task("Left Extruder SN"))

tasks.append(Task("Right Extruder SN"))

tasks.append(Task("X-Y Frame SN"))

tasks.append(Task("Type"))

tasks.append(Task("Userinterface"))

tasks.append(Task("Software last updated on"))

tasks.append(Task("Firmware version", str(file_editing.getFirmwareVersion())))

tasks.append(Task("Turn printer on", type='Procedure'))

tasks.append(Task("Touchscreen works?", type='Procedure'))

tasks.append(Task("Calibrate touchscreen", type='Procedure'))

def testEndstops():
	print 'Testing the endtops in all dimensions, min & max'
	# Steps: G28 - homed alle Achsen
	# Next: G1 X1100 F5000 a G1 = Move command , dann fahre die in X auf 1100mm mit der geschwindigkeit F700 (f=vorschub in mm/min)
	# Die Bauraumgroesse ist fuer X,Y und Z 1005mm, um die endstops zu triggern muss man aber in x, Y und Z auf minimum 1100mm fahren.
 
	# -G1 X1100 F5000
	# -G1 Y1100 F5000
	# -G1 Z1100 F700

	# OI: Add code to test endstops in all dimensions, min & max

tasks.append(Task("Functional Test of Endstops", type='Procedure', function=testEndstops))

def testXPrecision():
	# T1, G1 X100 Y100 Z5
	# G1 X600 F5000
	print 'Testing Precision in X'

def testYPrecision():
	# T1, G1 X100 Y100 Z5
	# G1 Y600 F10000
	print 'Testing Precision in Y'

def testZPrecision():
	# T1, G1 X100 Y100 Z10
	# G1 Z510 F700
	print 'Testing Precision in Z'

def recalibrate():
	print 'recalibrating'
	
	# If difference after testing precision is less than 0,5mm, recalibrate.
	# Remember: X = Alpha , Y = Beta , Z = Gamma.
	# Formula for calculating new config value: new config value = result(in mm)/500mm
	# In order for the new config to be loaded, restart machine and touchscreen,
	# and wait 30 seconds before turning machine back on.
	
tasks.append(Task("Test Precision in X. (Listen for noise)", type='Procedure', function=testXPrecision, errorFunction=recalibrate))

tasks.append(Task("Measure dX, should be 500mm +/-0,5mm", type='Entry'))

tasks.append(Task("Test Precision in Y. (Listen for noise)", type='Procedure', function=testYPrecision))

tasks.append(Task("Measure dY, should be 500mm +/-0,5mm", type='Entry'))

tasks.append(Task("Test Precision in Z. (Listen for noise)", type='Procedure', function=testZPrecision))

tasks.append(Task("Measure dZ, should be 500mm +/-0,5mm", type='Entry'))

tasks.append(Task("Test printing platform. Time to heat up:"))

def calibrateTable():
	print "Calibrating Table"
	# angled table holder: 10mm U-U
	# straight table holder: 65mm U-U
	# Heat platform to 60 degrees
	# Move printer to absolute Z position: 6.5mm - 8mm 
	# Move table up or down until laser shows +4900 for positions x100y100 - x100y980 - x1000y100 - x1000y980, then confirm again

tasks.append(Task("Calibrate Table", type='Procedure', function=calibrateTable))

def switchMode(parameter):
	# Switch to pro mode by pressing 'down' button for 3 seconds. 
	# Chose and confirm option 'SenS'. 
	# Press 'up' and 'down' in the following menu to siwtch into '2 Komparativ Modus'(N2) and confirm that.
	# Press 'down' button for 3 seconds to quit the 'pro' mode.
	print "Switching into mode: %s" %parameter

tasks.append(Task("Switch laser into 'Komparativ 2' mode", type='Procedure', function=lambda: switchMode('Komparativ 2')))

def learnLaser():
	# Move to x100 und y100 fahren, keep Z-position from last step
	# Press 'teach' and move the printer 9,9mm (or 9.8mm if reduce error) beyond the current point
	# Press teach again - You should get a 'GooD' message 	
	print "Learning in laser"

tasks.append(Task("Learn in Laser", type='Procedure', function=learnLaser))
'''
def calibrateExtruder():
	# Heat platform to 60 degrees and both extruders to 220 degrees
	# Move to X100 and Y100
	# Move both extruder-heads to highest position with config-screws 
	# Choose 'T0'
	# Calibrate the height of the extruders - if the feelerspace is 0.5mm, move to absolute Z-Position of 0.5mm and calibrate.
	# Switch to 'T1', move to same coordinates and calibrate T1
	print "calibrating extruders."	

tasks.append(Task("Calibrate extruder height", type='Procedure', function=calibrateExtruder))

tasks.append(Task("Height profile WITHOUT G32 (d(MIN, MAX) =< 0.3mm):"))

tasks.append(Task("Height profile WITH G32 (d(MIN, MAX) =< 0.3mm):"))

def firstLayerAdhesionTest():
	# G-code adhesion test both extruders and checking of the 'Z-Probe-offsets'
	# Complete Firstlayer_adhession test (Beginning height of test = 0.2mm - use measuring slider)
	# If the extruder is too close, decrease the Z-test value - if it's too far away, increase Z-test value
	# Z-test represents offset - The printer drives down X-mm in Z-direction after the G32
	# If the Z-test value is too high, the Z-sensor might be triggered.	
	print "Testing adhesion"

tasks.append(Task("First layer adhesion test", type='Procedure', function=firstLayerAdhesionTest))

def enduranceTest():
	# 24 Hour endurance test - indication about potentially lost steps in the motors and continuos load on the x-motor.
	# After the endurance test, readjust the gears of the Z-axis with 5,6 NM
	# Check the belt tension again and readjust if necessary	
	print "Testing endurance"

tasks.append(Task("Endurance Test", type='Procedure', function=enduranceTest))