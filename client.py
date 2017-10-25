#!/usr/bin/python

from Queue import Queue
from threading import Thread
from threading import RLock
from wordSpoiler import translate
import socket
import sys
import time

from message import formatMessage, smbMessage
from downloadImage import downloadImage, showImage

port = 6667
server = "irc.freenode.org"
channel = "#spbnet"
botnick = "qwwert"
botdescription = "This is a fun bot!"
bufsize = 2040
output = Queue()


def init():
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output.put ("connecting to:"+server)
    irc.connect((server, port))                                                       
    irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :"+ botdescription +"\n")
    irc.send("NICK "+ botnick +"\n")                            
    irc.send("PRIVMSG nickserv :iNOOPE\r\n")    
    irc.send("JOIN "+ channel +"\n")      
    return irc

def isPing(irc, text):
    if text.find('PING') != -1:                          #check if 'PING' is found
      irc.send('PONG ' + text.split() [1] + '\r\n')
      return True
    return False

#gets messages from server
def listen(irc, output):
    while True:
      text=irc.recv(bufsize) 
      if text != '':
         if not isPing(irc, text):
           #print text
           formatedmsg, isMsg, msg = formatMessage(text)
           output.put ('|\n'+ formatedmsg)
           if isMsg:
              say(irc, output,  msg)   
              whatIs(irc, output,  msg)                

def say(irc, output,  msg):
     if (msg.find ('say ') == 0):
         _, msg = msg.split(' ', 1)
         str = translate(msg)
         send (irc, str)
         output.put(smbMessage(botnick, str))


def whatIs(irc, output,  msg):
     if (msg.find ('whatis ') == 0  ):
         _, msg = msg.split(' ', 1)
         
         imageName = '1.jpg'
         if msg.find ('.jpg') ==-1 or not downloadImage(msg, imageName) :
             str = 'Bad url'
             send (irc, str)
             output.put(smbMessage(botnick, str))
         else:
             time.sleep(10)
             res = showImage(imageName)
             i = 0  
             for str in res:
                  send (irc, str)
                  output.put(smbMessage(botnick, str))
                  time.sleep(0.5)
                  i += 1
                  if (i == 4):
                      i = 0
                      time.sleep(1)
                      

#write total output to console
def writeOutput(output):
    while True:    
       if not output.empty():
         #writeLock.acquire()
         print output.get()
         #writeLock.release()
def send (irc, msg):
    irc.send("PRIVMSG " + channel + " :" + msg + "\n")

def consoleRead(irc, output):
  while True: 
     #writeLock.acquire()
     str = raw_input()
     if (str != ""):
         send (irc, str)
         output.put(smbMessage(botnick, str))
     #writeLock.release()
       
irc = init()

listener = Thread(target=listen, args=(irc,output,))
writer = Thread(target=writeOutput, args=(output,))
consoleReader = Thread(target=consoleRead, args=(irc,output,))

listener.daemon = True
writer.daemon = True
consoleReader.daemon = True

listener.start()
writer.start()
consoleReader.start()


while True:
        try:
           pass
        except KeyboardInterrupt:
            print "Leaving now..."
            if not output.empty():
               print output.get()
            irc.send("QUIT :iNOOPE\n")
            irc.close()
            sys.exit()
            sock.close()
      # finally:
    #print >>sys.stderr, 'closing socket'



   
