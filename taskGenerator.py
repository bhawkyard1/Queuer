from PySide import QtGui
from task import *
from functools import partial

class taskGenerator( QtGui.QWidget ):
	
	def __init__( self,  ):
		super( taskGenerator, self ).__init__()
		#The number of tasks this will dispatch, ie the user can specify multiple files to be rendered.
		self.numTasks = 0
		self.initUI()
		
	def initUI( self ):
		self.setGeometry(256, 256, 512, 256)
		self.setWindowTitle('Create Job')
		self.setWindowIcon(QtGui.QIcon('icon.png')) 
		
		a = QtGui.QVBoxLayout( self )
		
		self.grid = QtGui.QGridLayout()
		a.addLayout( self.grid )
		
		self.mainLabel = QtGui.QLabel("I want to...")
		self.grid.addWidget( self.mainLabel, 0, 0 )
		
		self.mainSelect = QtGui.QComboBox( self )
		self.mainSelect.addItem("Render")
		self.mainSelect.addItem("Custom")
		self.mainSelect.currentIndexChanged.connect( self.updateContextualUI )
		
		self.grid.addWidget( self.mainSelect, 0, 1 )
		
		self.addBtn = QtGui.QPushButton( "Add" )
		a.addWidget( self.addBtn )
		
		self.contextItems = []
		
		self.updateContextualUI()
		
	def getTasks( self ):
		#Get whether we are rendering, etc
		taskName = str( self.mainSelect.currentText() )
		#Create an empty list of tasks
		tasks = []
		
		if taskName == "Render":
			paths = str( self.contextItems[0].text() ).split(',')
			tasks = [task( taskName + '\n' + i ) for i in paths]
			self.numTasks = len( paths )
		else:
			tasks.append( task( taskName ) )
			self.numTasks = 1
		 
		return tasks
		
	def updateContextualUI( self ):
		t = str( self.mainSelect.currentText() )
		
		for widget in self.contextItems:
			self.grid.removeWidget(widget)
			widget.deleteLater()
			widget = None
			
		self.contextItems = []
		
		if t == "Render":
			self.contextItems.append( QtGui.QLineEdit() )
			self.contextItems.append( QtGui.QPushButton( "Select Scene File" ) )
			self.contextItems[1].clicked.connect( self.getRenderFile )
			self.grid.addWidget( self.contextItems[0], 0, 2 )
			self.grid.addWidget( self.contextItems[1], 0, 3 )
		elif t == "Custom":
			self.contextItems.append( QtGui.QLineEdit() )
			self.contextItems[0].setText( "Add custom terminal commands here..." )
			self.grid.addWidget( self.contextItems[0], 0, 2 )
			
	def getRenderFile( self ):
		strings = QtGui.QFileDialog.getOpenFileNames()
		print "Files " + str(strings)
		st = ''
		for s in strings[0]:
			st += s + ","
		self.contextItems[0].setText( st )
