import sys
from PySide import QtGui
from PySide import QtCore
from task import *
from taskGenerator import *
import util
from worker import worker
from functools import partial

if globals().has_key('init_modules'):
	for m in [x for x in sys.modules.keys() if x not in init_modules]:
		del(sys.modules[m]) 
else:
	init_modules = sys.modules.keys()

class mainWindow(QtGui.QWidget):
	
	def __init__(self):
		super( mainWindow, self ).__init__()
		self.initUI()
		#Task index represents which task is the current 'active' one. Set to -1 here because we have no tasks yet.
		self.taskIndex = -1
		#All the tasks are stored in this list.
		self.taskList = []
		#The background thread responsible for running the tasks is persistent, and set to None here, since we have no tasks.
		self.taskQueueWorker = None
		
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
		
		#Right column
		self.addTaskBtn = QtGui.QPushButton("Add Job/s")
		self.menu.addWidget( self.addTaskBtn )
		self.addTaskBtn.clicked.connect( self.taskDialog )
		
		self.clearBtn = QtGui.QPushButton("Clear")
		self.menu.addWidget( self.clearBtn )
		self.clearBtn.clicked.connect( self.clearTasks )
		
		a = QtGui.QHBoxLayout()
		self.menu.addLayout( a )
		
		b = QtGui.QLabel( "On completion, " )
		a.addWidget( b )
		
		self.onCompletionCombo = QtGui.QComboBox()
		self.onCompletionCombo.addItem( "do nothing." )
		self.onCompletionCombo.addItem( "log off." )
		self.onCompletionCombo.addItem( "shut down." )
		a.addWidget( self.onCompletionCombo )
		
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
		self.executeTask()
	
	#Recusrive function, runs task at self.taskIndex on a seperate thread, then increments self.taskIndex and calls itself again.
	#Breaks when self.taskIndex is going to be out of bounds.
	def executeTask( self ):
		self.taskIndex += 1
		if self.taskIndex > 0:
			self.taskList[ self.taskIndex - 1 ].setStyleSheet( "background-color: green" )
		if self.taskIndex >= len( self.taskList ):
			self.executionComplete()
			return
		self.taskList[ self.taskIndex ].setStyleSheet( "background-color: orange" )
		self.taskQueueWorker = worker( self.taskList[ self.taskIndex ].execute )
		self.connect( self.taskQueueWorker, QtCore.SIGNAL("run() complete"), self.executeTask )
		self.taskQueueWorker.start() 
		self.taskList[ self.taskIndex ].setStyleSheet( "background-color: orange" )
		
	def executionComplete( self ):
		self.taskIndex = -1
		if str( self.onCompletionCombo.currentText() ) == "log off.":
			util.logoff()
		elif str( self.onCompletionCombo.currentText() ) == "shut down.":
			util.shutdown()

def main():
	app = QtGui.QApplication( sys.argv )
	win = mainWindow()
	sys.exit( app.exec_() )
	
if __name__ == "__main__":
	main()
