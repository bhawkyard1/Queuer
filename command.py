import subprocess
import time

from enum import Enum
class execType( Enum ):
	EXEC_BASH = 0
	EXEC_PYTHON = 1

class command:
	
	def __init__( self, _type, _body ):
		self.cmdType = _type
		self.body = _body
		
	def execute( self ):
		if self.cmdType == execType.EXEC_BASH:
			subprocess.Popen( [ self.body ], shell = True ).wait()
		elif self.cmdType == execType.EXEC_PYTHON:
			exec( self.body )
	
