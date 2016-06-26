from Tkinter import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

import task_class

import subprocess

def endConfiguration(root):
	print 'Finishing the configuration'
	# TD: Create pdf.
	# TD: How to save progress in case window closed, device crashes???
	root.destroy()

def getFirmwareVersion():

	# OI: (on implementation): uncomment when testing with correct hardware.
	# string = str(subprocess.check_output(["apt-cache", "policy" "bigrep-one"]))
	return subprocess.check_output(["sw_vers", "-productVersion"])

def saveAsPDF():

	id = str(task_class.tasks[0].content + task_class.tasks[1].content)
	c = canvas.Canvas(id + ".pdf")
	c.setLineWidth(0.3)
	c.setFont('Helvetica', 12)

	# TD: Add code to draw BigRep Header, title etc.

	for index in range(0, len(task_class.tasks)):

		c.drawString(50,900-16*index,task_class.tasks[index].label)
		c.drawString(200,900-16*index,task_class.tasks[index].content)

		# TD: Add code to check if process, then report true or not and error, add 
		# TD: Add current time, time stamp

	c.save()