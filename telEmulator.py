#!/usr/bin/python

import socket
import sys
import thread
from datetime import datetime
	
host = ''
port = 23

def receiveInfo(c, cliInput):
	done = False
	cliInput = ''
	while (done == False):
		data = c.recv(1024)
		if (len(str(data)) == 1):
			charInput = data.encode('hex')
			cliInput += charInput
			c.send(data)
		elif (len(str(data)) <= 0):
			done = False
		else:
			charInput = data.encode('hex')
			if charInput == '0d00':
				done = True
			elif charInput == '0d0a':
				done = True
			elif charInput == 'fffd03':
				done = False
			elif charInput == 'fffe03':
				done = False
			elif charInput == 'fffd03fffb18fffb1ffffb20fffb21fffb22fffb27fffd05fffb23':
				done = False
			elif charInput == 'fffd03fffd01fffb1ffffa1f00500016fff0fffb18':
				done = False
			else:
				print data.encode('hex')
				cliInput = data.encode('hex')
				done = True
	return cliInput

def handleClient(c, addr):
	username = ''
	password = ''
	commands = ''
	allCommands = ''
	print "Connection: " + str(addr)
	# Robert Graham Preamble taken from telnetlogger
	msg = "\xff\xfb\x03"
	msg += "\xff\xfb\x01"
	msg += "\xff\xfd\x1f"
	msg += "\xff\xfd\x18"
	msg += "\r\nBCM96828 Broadband Router" 
	msg += "\r\nLogin: "
	c.send(msg)
	# Telnet will process a character at a time...
	username = receiveInfo(c, username) 
	print "Username: " + username.decode('hex')
	msg = "\r\nPassword: "
	c.send(msg)
	password = receiveInfo(c, password) 
	print "Password: " + password.decode('hex')
	loop = 0
	while loop < 10:
		msg = "\r\n# "
		c.send(msg)
		commands = receiveInfo(c, commands) 
		print "Command: " + commands.decode('hex')
		ipInfo = str(addr)
		f = open('outputInfo.txt', 'a')
		#f.write('IP:' + ipInfo + '|U:' + username[36:-4].decode('hex') + '|P:' + password.decode('hex') + '|C:' + commands.decode('hex') + '\n')
		f.write('T:' + str(datetime.now()) + '|IP:' + ipInfo + '|U:' + username[36:-4].decode('hex') + '|P:' + password.decode('hex') + '|C:' + commands.decode('hex') + '\n')
		f.close()
		loop += 1
	c.close()

def main():
	global host,port
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except:
		print "Failed to create socket."
		sys.exit()
	s.bind((host, port))
	s.listen(15) # Allows up to 15 connections at a time
	while 1:
		(client, address) = s.accept()
		thread.start_new_thread(handleClient, (client, address))
	s.close()


if __name__ == "__main__":
	main()
