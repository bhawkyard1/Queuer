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
		self.previousTask = None
		#All the tasks are stored in this list.
		self.taskList = []
		#The background thread responsible for running the tasks is persistent, and set to None here, since we have no tasks.
		self.taskQueueWorker = None
		
	def initUI(self):
		self.setGeometry(32, 32, 512, 512)
		self.setWindowTitle('Queuer')
		self.setWindowIcon(QtGui.QIcon('icon.png')) 
		
		#Create the two main columns. Left is queue, right is buttons.
		self.columns = QtGui.QHBoxLayout( self )
		
		#Create the task queue
		self.taskQueue = QtGui.QListView()
		self.taskQueue.setMinimumSize( 256, 512 )
		self.taskQueueModel = QtGui.QStandardItemModel( self.taskQueue )
		self.taskQueue.setModel( self.taskQueueModel )
		#self.taskQueue.
		
		self.columns.addWidget( self.taskQueue )
		
		#Create the menu
		self.menu = QtGui.QVBoxLayout()
		self.columns.addLayout( self.menu )
		
		#Right column
		self.addTaskBtn = QtGui.QPushButton("Add Job/s")
		self.menu.addWidget( self.addTaskBtn )
		self.addTaskBtn.clicked.connect( self.taskDialog )
		
		self.clearBtn = QtGui.QPushButton("Clear")
		self.menu.addWidget( self.clearBtn )
		self.clearBtn.clicked.connect( self.clearTasks )
		
		self.delBtn = QtGui.QPushButton("Delete")
		self.menu.addWidget( self.delBtn )
		self.delBtn.clicked.connect( self.delTasks )
		
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
		  
		self.taskQueue.show()
		self.show()
		
	def taskDialog( self ):
		self.taskGen.show()
	
	#Adds one or more tasks to the queue, depending on the exact contents of self.taskGen
	def addTask( self ):
		for t in self.taskGen.getTasks():
			self.taskQueueModel.appendRow( t )
			self.taskList.append( t ) 
		self.taskGen.hide()
		
	#Empties the task queue
	def clearTasks( self ):
		for i in reversed( xrange( len( self.taskList ) ) ):
			self.taskQueueModel.removeRow( i )
		self.taskList = []
		
	def delTasks( self ):
		for i in reversed( xrange( len( self.taskList ) ) ):
			if self.taskList[i].checkState() == QtCore.Qt.Checked:
				self.taskQueueModel.removeRow( i )
				del self.taskList[ i ]
				
	
	#Runs the tasks
	def execute( self ):
		self.executeTask()
	
	#Recusrive function, runs task at self.taskIndex on a seperate thread, then increments self.taskIndex and calls itself again.
	#Breaks when self.taskIndex is going to be out of bounds.
	def executeTask( self ):
		
		#Increment the active index
		self.taskIndex += 1
		print "Executing task " + str( self.taskIndex )
		
		#Set last completed task to green
		if not self.previousTask is None:
			self.previousTask.setBackground(QtGui.QColor("green"))
		
		#Break out if we are at the end of the list.
		if self.taskIndex >= len( self.taskList ):
			self.executionComplete()
			return
		
		#Skip if the task is unchecked
		if self.taskList[ self.taskIndex ].checkState() != QtCore.Qt.Checked:
			self.executeTask()
			return
		else:
			self.previousTask = self.taskList[ self.taskIndex ]
		
		#Set up the worker thread
		self.taskQueueWorker = worker( self.taskList[ self.taskIndex ].execute )
		#Connect to this function
		self.connect( self.taskQueueWorker, QtCore.SIGNAL("run() complete"), self.executeTask )
		#Run thread
		self.taskQueueWorker.start() 
		#Set this task to colour orange
		self.taskList[ self.taskIndex ].setBackground(QtGui.QColor("orange"))
		
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
