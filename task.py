from PySide import QtGui

from enum import Enum
class taskStatus(Enum):
	TASK_NOT_STARTED = 0
	TASK_STARTED = 1
	TASK_COMPLETED = 2

class task( QtGui.QFrame ):
	
	def __init__( self, _type ):
		super( task, self ).__init__()
		self.type = _type
		self.command = ""
		self.status = taskStatus.TASK_NOT_STARTED
		self.initUI()
		
	def initUI( self ):
		self.resize( 128, 64 )
		self.setStyleSheet( "background-color: salmon" )
		
		self.typeLabel = QtGui.QLabel( self.type, self )
		self.typeLabel.move( 4, 4 )
