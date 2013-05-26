#
# OTC Authentication Python Module for XChat
# =========================================================
# By: Exodeus
# Version 0.1.1 completed 05.26.2013
#

import xchat
import gnupg
import pycurl
import cStringIO
from time import sleep

# Define our module.
__module_name__ = "Ex0's OTC Authentication Tool"
__module_version__ = "0.1.1"
__module_author__ = "Exodeus"
__module_description__ = "This is a handy tool for XChat2 IRC client used for OTC Authentication"

xchat.prnt("%s Ver. %s : LOADED" % (__module_name__, __module_version__))

# Print Version Information
def otcauth_ver():
	xchat.prnt("%s Version: %s By: %s" % (__module_name__, __module_version__, __module_author__))
	xchat.prnt(__module_description__)
	
	return xchat.EAT_ALL

# Print out the Help info
def otcauth_help(topic):
	if topic == "basic":
		xchat.prnt(""" OTCAUTH Tool Help page not completed! """)
	else:
		xchat.prnt("I don't know anything about topic: %s" % topic)
	
	return xchat.EAT_ALL

# Get our string to decrypt from gribble
def get_auth(nick, keyid):
	xchat.command("MSG gribble eauth %s" % (nick))
	# Give gribble some time to create the new encrypted string
	sleep(6)
	
	# Get our url string and create a string buffer to write to
	url = "http://bitcoin-otc.com/otps/%s" % (str(keyid))
	buf = cStringIO.StringIO()
	
	# Grab our string to decrypt and return it
	curl = pycurl.Curl()
	curl.setopt(curl.URL, url)
	curl.setopt(curl.USERAGENT, """Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)""")
	curl.setopt(curl.WRITEFUNCTION, buf.write)
	curl.perform()
	
	result = buf.getvalue()
	buf.close()
	
	return result
	
# Use GPG to decrypt the string gribble gave us and send back the verify string
def otc_decrypt(encrypted_string):
	gpg = gnupg.GPG(use_agent=True)
	gpg.encoding = 'utf-8'
	auth_string = gpg.decrypt(encrypted_string)

	xchat.command("MSG gribble everify %s" % (str(auth_string))
	
	return xchat.EAT_ALL
	
# The callback function to our hook that ties it all together	
def otcauth_cb(*args):
	check = str(args[0][1])
	print args 	#FOR DEBUGGING PURPOSES
	if check == "help":
		otcauth_help(args[0][2:])
	elif check == "version":
		otcauth_ver()
	elif check == "auth":
		xchat.prnt("Got to auth") # For debugging purposes
		nick = xchat.get_info('nick')
		if len(args[0][2]) != 16:
			xchat.prnt("You need to supply a valid key id!")
		else:
			keyid = args[0][2]
			otc_decrypt(get_auth(nick, keyid))
	else:
		xchat.prnt("here at the else") # For debugging purposes
		otcauth_help("basic")
	
	return xchat.EAT_NONE
	
# Hook our functions to commands to make them usable
xchat.hook_command("OTCAUTH", otcauth_cb, help="Type /OTCAUTH help for more help")
