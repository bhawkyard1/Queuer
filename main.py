import sys
from PySide import QtGui
from task import *
from taskGenerator import *

if globals().has_key('init_modules'):
	for m in [x for x in sys.modules.keys() if x not in init_modules]:
		del(sys.modules[m]) 
else:
	init_modules = sys.modules.keys()

class mainWindow(QtGui.QWidget):
	
	def __init__(self):
		super( mainWindow, self ).__init__()
		self.initUI()
		self.taskList = []
		
	def initUI(self):
		self.setGeometry(32, 32, 256, 512)
		self.setWindowTitle('Queuer')
		self.setWindowIcon(QtGui.QIcon('icon.png')) 
		
		#Create the two main columns. Left is queue, right is buttons.
		self.columns = QtGui.QHBoxLayout( self )
		self.taskQueueWrapper = QtGui.QVBoxLayout()
		self.menu = QtGui.QVBoxLayout()
		
		self.columns.addLayout( self.taskQueueWrapper )
		self.columns.addLayout( self.menu )
		
		#Left column
		#a = QtGui.QFrame()
		#a.resize(128, 512)
		#a.setFrameStyle( QtGui.QFrame.Sunken )
		#self.taskQueueWrapper.addWidget(a)
		
		#Right column
		self.addTaskBtn = QtGui.QPushButton("Add Job/s")
		self.menu.addWidget( self.addTaskBtn )
		self.addTaskBtn.clicked.connect( self.taskDialog )
		
		self.clearBtn = QtGui.QPushButton("Clear")
		self.menu.addWidget( self.clearBtn )
		self.clearBtn.clicked.connect( self.clearTasks )
		
		self.execBtn = QtGui.QPushButton("Execute")
		self.menu.addWidget( self.execBtn )
		self.execBtn.clicked.connect( self.execute )
		
		self.quitBtn = QtGui.QPushButton("Quit")
		self.menu.addWidget( self.quitBtn )
		self.quitBtn.clicked.connect( self.close )
		
		#Task generator
		self.taskGen = taskGenerator()
		self.taskGen.addBtn.clicked.connect( self.addTask )
		   
		self.show()
		
	def taskDialog( self ):
		self.taskGen.show()
	
	#Adds one or more tasks to the queue, depending on the exact contents of self.taskGen
	def addTask( self ):
		for t in self.taskGen.getTasks():
			self.taskQueueWrapper.addWidget( t )
			self.taskList.append( t ) 
		self.taskGen.hide()
		
	#Empties the task queue
	def clearTasks( self ):
		for t in self.taskList:
			self.taskQueueWrapper.removeWidget( t )
			t.deleteLater()
			t = None
		self.taskList = []
	
	#Runs the tasks
	def execute( self ):
		for task in self.taskList:
			task.execute()
		
		

def main():
	app = QtGui.QApplication( sys.argv )
	win = mainWindow()
	sys.exit( app.exec_() )
	
if __name__ == "__main__":
	main()
