import platform
import subprocess

def logoff():
	print "Logging off..."
	if platform.system() == "Linux":
		subprocess.Popen( ["gnome-session-quit --logout --no-prompt"], shell = True )
	elif platform.system() == "Windows":
		subprocess.Popen( ["shutdown /l"], shell = True )
