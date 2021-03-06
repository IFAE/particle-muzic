"""OSC Test Script
Written by Aaron Chamberlain Dec. 2013
The purpose of this script is to make a very simple communication structure to the popular 
application touchOSC. This is achieved through the pyOSC library. However, since the pyOSC 
documentation is scarce and only one large example is included, I am going to strip down 
the basic structures of that file to implement a very simple bi-directional communication.
"""
#!/usr/bin/env python
#http://mcdeltat.tumblr.com/post/80890564578/tutorial-1-pyosc-touchosc-tutorial

import socket, OSC, re, time, threading, math

receive_address = '172.16.4.21', 7000 #Mac Adress, Outgoing Port  IFAE
send_address = '172.16.4.30', 9000 #iPhone Adress, Incoming Port  IFAE

class PiException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

##########################
#	OSC
##########################

# Initialize the OSC server and the client.
s = OSC.OSCServer(receive_address)
c = OSC.OSCClient()
c.connect(send_address)

s.addDefaultHandlers()

# define a message-handler function for the server to call.
def test_handler(addr, tags, stuff, source):
	print "---"
	print "received new osc msg from %s" % OSC.getUrlStr(source)
	print "with addr : %s" % addr
	print "typetags %s" % tags
	print "data %s" % stuff
	msg = OSC.OSCMessage()
	msg.setAddress(addr)
	msg.append(stuff)
	c.send(msg)
	print "return message %s" % msg
	print "---"

def moveStop_handler(add, tags, stuff, source):
	addMove(0,0)

def moveJoystick_handler(add, tags, stuff, source):
	print "message received:"
	msg = OSC.OSCMessage()
	msg.setAddress(addr)
	msg.append(stuff)
	c.send(msg)
	print "X Value is: " 
	print stuff[0] 
	print "Y Value is: " 
	print stuff[1]  #stuff is a 'list' variable

def handler(addr, tags, data, client_address):
    txt = "OSCMessage '%s' from %s: " % (addr, client_address)
    txt += str(data)
    print(txt)


# adding my functions
s.addMsgHandler("/basic/stop", moveStop_handler)
s.addMsgHandler("/basic/joystick", moveJoystick_handler)
s.addMsgHandler('/1/faderA', test_handler)


# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
	print addr

# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()

# Loop while threads are running.
try :
	while 1 :
		time.sleep(10)
 
except KeyboardInterrupt :
	print "\nClosing OSCServer."
	s.close()
	print "Waiting for Server-thread to finish"
	st.join()
	print "Done"