from PySide import QtGui
from PySide import QtCore
import time

from enum import Enum
class taskStatus( Enum ):
	TASK_NOT_STARTED = 0
	TASK_STARTED = 1
	TASK_COMPLETED = 2
	
from command import *

class task( QtGui.QStandardItem ):
	
	def __init__( self, _name, _command ):
		super( task, self ).__init__()
		self.name = _name
		self.command = _command
		self.status = taskStatus.TASK_NOT_STARTED
		self.initUI()
		
	def initUI( self ):
		self.setBackground(QtGui.QColor("salmon"))
		
		self.setText( self.name )
		self.setCheckable( True )
		self.setCheckState( QtCore.Qt.Checked )
		
	def execute( self ):
		if self.status == taskStatus.TASK_COMPLETED:
			return
		self.status = taskStatus.TASK_STARTED
		self.command.execute()
		self.status = taskStatus.TASK_COMPLETED
