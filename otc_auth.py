# otc_auth.py
# Ex0's OTC Authentication Python Module for XChat
# ======================================================================
#  
#  Copyright 2013 Exodeus <exodeus@digitalfrost.net>
#  Version 0.1.4 completed 05.26.2013
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# ======================================================================
# CHANGE LOG
# ----------------------------------------------------------------------
# DATE Ver 0.1.4
# ----------------------------------------------------------------------
# * Fleshed out the help function a bit more and added some fixes
#	to the way help is displayed.
# * 
#
# ----------------------------------------------------------------------
# 05.26.2013 Ver 0.1.3
# ----------------------------------------------------------------------
# *	Updated the callback function to a proper xchat style
# * Changed License to GPL
# ----------------------------------------------------------------------
# 05.26.2013 Ver 0.1.2
# ----------------------------------------------------------------------
# * Fixed some errors.
# * Got rid of that nagging ":unknown command" in xchat.
# * Chaged the name of some functions and variables to
#	to better describe their purpose.
# * Prepended Ex0's to the tool title.
# * Removed some of the code for debug purposes.
# * Modified some functions for better error handling
# * Started polishing off the help section
# * Added this CHANGE LOG

import xchat
import gnupg
import pycurl
import cStringIO
from time import sleep

# Define our module.
__module_name__ = "Ex0's OTC Authentication Tool"
__module_version__ = "0.1.3"
__module_author__ = "Exodeus"
__module_description__ = "This is a handy tool for XChat2 IRC client used for OTC Authentication"

xchat.prnt("%s Ver. %s : LOADED" % (__module_name__, __module_version__))

# Print Version Information
def otcauth_ver():
	xchat.prnt("%s Version: %s By: %s" % (__module_name__, __module_version__, __module_author__))
	xchat.prnt(__module_description__)
	
	return xchat.EAT_NONE

# Print out the Help info
def otcauth_help(topic):
	if len(topic) < 2:
		switch = "basic"
	else:
		switch = topic[1]
		etc = "".join(topic[1])

	if switch == "basic":
		xchat.prnt("""/OTCAUTH  
=======================================
An OTC authentication script for XChat2
	OPTIONS:
		HELP
				Display help page
				or use help <topic>
				for more help about
				<topic>	

		AUTH
				Used to start the
				GPG Auth process.

		VERSION
				Returns the scripts
				version string.""")

	elif switch == "auth":
		xchat.prnt("/OTCAUTH auth \n\tAuth Help")
	elif switch == "version":
		xchat.prnt("/OTCAUTH version \n\tPrints out the current version of the tool")
	else:
		xchat.prnt("I don't know anything about topic: %s" % (str(etc)))
	
	return xchat.EAT_XCHAT

# Get our string to decrypt from gribble
def otcauth_get_auth(keyid):
	# Give gribble some time to create the new encrypted string
	# Need to eliminate the timer. Perhaps with a xchat server hook?
	sleep(3)
	
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
def otcauth_decrypt(encrypted_string):
	gpg = gnupg.GPG(use_agent=True)
	gpg.encoding = 'utf-8'
	auth_string = gpg.decrypt(encrypted_string)

	xchat.command("MSG gribble everify %s" % (str(auth_string)))
	return xchat.EAT_NONE

	
# The callback function to our hook that ties it all together	
def otcauth_cb(word, word_eol, userdata):
	if len(word) < 2:
		switch = "help"
	else:
		switch = str(word[1])
	
	if switch == "help":
		otcauth_help(word[1:])
	elif switch == "version":
		otcauth_ver()
	elif switch == "auth":
		nick = xchat.get_info('nick')
		xchat.command("MSG gribble eauth %s" % (nick))
		
		if len(word[2]) != 16:
			xchat.prnt("You need to supply a valid key id!")
		else:
			keyid = word[2]
			otcauth_decrypt(otcauth_get_auth(keyid))
	else:
		xchat.prnt("Invalid Option: %s not defined" % (word[1]))
	
	return xchat.EAT_XCHAT
	
# Hook our functions to the callback handler
xchat.hook_command("OTCAUTH", otcauth_cb, help="'/OTCAUTH help' for more help")
