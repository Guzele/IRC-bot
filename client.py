#!/usr/bin/python

from Queue import Queue
import thread
import socket
import sys

port = 6667
server = "irc.freenode.org"
channel = "#train"
botnick = "qwwertyuui"
botdescription = "This is a fun bot!"
bufsize = 2040
output = Queue()

def init():
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output.put ("connecting to:"+server)
    irc.connect((server, port))                                                         #connects to the server
    irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :"+ botdescription +"\n") #user authentication
    irc.send("NICK "+ botnick +"\n")                            #sets nick
    irc.send("PRIVMSG nickserv :iNOOPE\r\n")    #auth
    irc.send("JOIN "+ channel +"\n")        #join the chan
    return irc

def isPing(text):
    if text.find('PING') != -1:                          #check if 'PING' is found
      irc.send('PONG ' + text.split() [1] + '\r\n')
      return True
    return False

def readChat(irc):
    text=irc.recv(bufsize)  #receive the text
    if not isPing(text):
      output.put (text)

irc = init()

while 1:    #puts it in a loop
   readChat(irc)
   if not output.empty():
       print output.get()
