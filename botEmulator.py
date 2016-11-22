#!/usr/bin/python

# This is designed to emulate a bot that is part of the Mirai botnet.
# The hope is that it can capture the commands that are sent to begin
# a denial of service

import socket
import sys
from threading import Thread
from datetime import datetime

def writeBotLog(r, ip, port):
	r = r.strip()
	flog = open("bot.log", "a")
	info = "T:" + str(datetime.now()) + "IP:" + str(ip) + "|PORT:" + str(port) + "|C:" + str(r) + "\n"
	flog.write(info)
	flog.close()


def connectClient(ipA, portN):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ipA, int(portN)))
	except:
		writeBotLog("Failed to connect.", ipA, portN)
		sys.exit()
	recv = s.recv(1024)
	writeBotLog(recv, ipA, portN)
	while 1:
		recv = s.recv(1024)
		if recv:
			if "PING" in recv:
				s.send("PONG")
			writeBotLog(recv, ipA, portN)


def main():
	f = open("listCnC.txt", "r")
	for line in f:
		items = line.split(':')
		ipAddr = items[0]
		portNum = items[1].strip()
		#print ipAddr + " " + str(portNum)	
		t = Thread(target=connectClient, args=(ipAddr, portNum))
		t.start()



if __name__ == "__main__":
	main()


