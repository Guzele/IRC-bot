#!/usr/bin/python

from time import gmtime, strftime

commandsList = ['QUIT', 'JOIN', 'PART', 'PRIVMSG' ]
def transformMessage(message):
      message = message [1 :]
      accountName, message = message.split('!', 1)
      _, message = message.split(' ', 1) 
      command, tail_message = message.split(' ', 1) 

      return (accountName, command, tail_message)

def withCommand(message):
      for command in commandsList:
          if message.find(' ' + command + ' ') != -1:
               return True
      return False

indent = '   '

def formatMessage(message):   
      isMessage = False
      msg = ''  
 
      if not withCommand(message):
          formatedmsg =  time() + indent + message
          return (formatedmsg, isMessage, msg)
      #reciever not used
      accountName, command, tail_message = transformMessage(message)
      
      if command == 'PRIVMSG':
          reciever, message = tail_message.split(' ', 1) 
          message = message [1 :]
          formatedmsg = smbMessage (accountName, message)
          isMessage = True
          msg = message
          return (formatedmsg, isMessage, msg)
      else:
           end = tail_message.split(' ')
           reciever = end[0]

           if len (end) == 1:
               message = ''
           else:
               _, message = tail_message.split(' ', 1)


           formatedmsg = time() + indent + accountName + ' '  + command.lower() + 'ed' + indent + message

      return (formatedmsg, isMessage, msg)

def time():
    return strftime("%H:%M:%S", gmtime())

def smbMessage (account, message):
    return time()+indent+ account + indent + message


       
