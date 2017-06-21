from PySide import QtGui
from task import *
from functools import partial

class taskGenerator( QtGui.QWidget ):
	
	def __init__( self,  ):
		super( taskGenerator, self ).__init__()
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
		
	def getTask( self ):
		t = task( str( self.mainSelect.currentText() ) )
		return t
		
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
			
	def getRenderFile( self ):
		strings = QtGui.QFileDialog.getOpenFileName()
		st = ''
		for s in strings:
			st += s + ","
		self.contextItems[0].setText( st )
