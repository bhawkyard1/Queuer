import platform
import subprocess

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.parser import Parser

def logoff():
	print "Logging off..."
	if platform.system() == "Linux":
		subprocess.Popen( ["gnome-session-quit --logout --force --no-prompt"], shell = True )
	elif platform.system() == "Windows":
		subprocess.Popen( ["shutdown /l"], shell = True )
		
def shutdown():
	print "Shutting down..."
	if platform.system() == "Linux":
		subprocess.Popen( ["gnome-session-quit --power-off --force --no-prompt"], shell = True )
	elif platform.system() == "Windows":
		subprocess.Popen( ["shutdown /l"], shell = True )

#Sends an email using smtp given logon credentials. Apparently this is a bit of a dodgy way of doing things.
def sendEmail( _usr, _pwd, _address, _body ):
	msg = MIMEText( _body )
	msg['Subject'] = "Message from Queuer."
	msg['From'] = _usr
	msg['To'] = _address
	
	print "Sending email to " + _address + " : " + _body
	
	try:
		s = smtplib.SMTP("smtp.gmail.com:587")
		s.ehlo()
		s.starttls()
		s.login( _usr, _pwd )
		
		s.sendmail(msg['From'], msg['To'], _body)
		s.quit()
	except Exception, e:
		print "Error! Unable to send mail : " + str( e )
