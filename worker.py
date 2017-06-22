from PySide import QtCore

class worker( QtCore.QThread ):
	
	def __init__( self, _fn ):
		QtCore.QThread.__init__( self )
		self.fn = _fn
		
	def __del__( self ):
		self.wait()
		
	def run( self ):
		self.fn()
		self.emit( QtCore.SIGNAL("run() complete") )
