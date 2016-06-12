from Tkinter import *
import Graphics
import TaskClass

root = Tk()

root.withdraw()

progress = 0

def cleanUp():
	#Create pdf.
    root.destroy()

window = Toplevel(root)
window.wm_title("BigRep Printer Configuration")

window.protocol('WM_DELETE_WINDOW', cleanUp)
photo = PhotoImage(file="Logo.pgm").subsample(8)
def runWin():

	

	Label(window, image=photo).grid(row=0, column=1)

	Label(window, text="BigRep Configuration UI", font=Graphics.getBigRepFont(window, 40)).grid(row=0, column = 2)

runWin()

root.mainloop()


'''
from Tkinter import *
import Graphics
import TaskClass

root = Tk()

root.withdraw()

progress = 0

def cleanUp():
	#Create pdf.
    root.destroy()
def runWin():
	window = Toplevel(root)
	window.wm_title("BigRep Printer Configuration")

	window.protocol('WM_DELETE_WINDOW', cleanUp)

	photo = PhotoImage(file="Logo.pgm").subsample(8)

	Label(window, image=photo).grid(row=0, column=1)

	Label(window, text="BigRep Configuration UI", font=Graphics.getBigRepFont(window, 40)).grid(row=0, column = 2)

	tasks = TaskClass.tasks[progress:progress+TaskClass.groupSize]
	contentFields = []

	for r in range(len(tasks)):
		row = r+1
		label = Label(window, text=tasks[r].label).grid(row=row,column=1, sticky=W)
		content = Entry(window, width=40)
		content.grid(row=row, column=2, sticky=W)
		content.insert(0, tasks[r].content)
		contentFields += [content]
		#MainWin.rowconfigure(r, minsize=MainWin.winfo_height/len(tasks))
    	#MainWin.columnconfigure(1, minsize=MainWin.winfo_width/2)

	def onButtonClick():
		print 'Button clicked!'
		for num in range(0, TaskClass.groupSize-1):
			TaskClass.tasks[progress + num] = contentFields[num].get()
		window.destroy()
		runWin(progress+2)
	
	button = Button(window, text="Next", command=onButtonClick)
	button.grid(row=progress+TaskClass.groupSize+1, column=2, sticky = W)

runWin()

root.mainloop()
'''