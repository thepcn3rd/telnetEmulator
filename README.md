# telnetEmulator
Created this python script to emulate a telnet server and log an input username, password and commands that are entered. 
This script is probably not secure...

After executing this python program it will begin to listen on port 23.  Any username, password, or command that is entered
will appear in a log file called "outputInfo.txt".  You can then parse outputInfo.txt to find the IP, username, password and 
commands executed.

After identifying the commands executing, downloading the download script, then grabbing the binaries you can parse the binaries for the CnC servers IP and port.  Then this can be used with the botEmulator.py script to emulate a bot under the control of the CnC servers.  It logs the commands exchanged to bot.log.  It reads the CnC server list from listCnC.txt a file in the same directory.


