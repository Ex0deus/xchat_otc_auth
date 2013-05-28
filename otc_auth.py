# otc_auth.py
# Ex0's OTC Authentication Python Module for XChat
# ======================================================================
#  
#  Copyright 2013 Exodeus <exodeus@digitalfrost.net>
#  Version 0.2.0 completed 05.28.2013
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
# 05.28.2013 Ver 0.2.0
# ----------------------------------------------------------------------
# * Renamed some functions to better suite purposes.
# * Major changes to some functions.
# * Need for timer.sleep removed.
# * Server hook to catch event when gribble sends the link for the auth
#	string.
# * New server hook function adapted with ideas from nanotubes eauth
# 	script. (Link to script on github - http://bit.ly/138FWvk )
# ----------------------------------------------------------------------
# 05.27.2013 Ver 0.1.4
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

# Define our module.
__module_name__ = "Ex0's OTC Authentication Tool"
__module_version__ = "0.2.0"
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

		EAUTH
				Used to start the
				GPG Auth process.

		VERSION
				Returns the scripts
				version string.""")

	elif switch == "eauth":
		xchat.prnt("/OTCAUTH eauth \n\tAuth Help")
	elif switch == "version":
		xchat.prnt("/OTCAUTH version \n\tPrints out the current version of the tool")
	else:
		xchat.prnt("I don't know anything about topic: %s" % (str(etc)))
	
	return xchat.EAT_XCHAT

# GPG Decryption Function.
# Use GPG to decrypt the string gribble gave us and send back the verify string
def otcauth_gpg_decrypt(encrypted_string):
	gpg = gnupg.GPG(use_agent=True)
	gpg.encoding = 'utf-8'
	auth_string = gpg.decrypt(encrypted_string)

	return auth_string

# Get our string to decrypt from gribble
def otcauth_gpg_auth(word, word_eol, userdata):
	if word[0] == ':gribble!~gribble@unaffiliated/nanotube/bot/gribble':
		# Get our url
		url = str(word[-1])
		buf = cStringIO.StringIO()
		# Check to make sure we got the proper link.
		if url[:-16] == "http://bitcoin-otc.com/otps/":
			# Link Good! cURL our string and decrypt.
			curl = pycurl.Curl()
			curl.setopt(curl.URL, url)
			curl.setopt(curl.USERAGENT, """Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)""")
			curl.setopt(curl.WRITEFUNCTION, buf.write)
			curl.perform()

			# Decrypt and message gribble back the verify string.
			auth_string = buf.getvalue()
			buf.close()
			xchat.command("MSG gribble everify %s" % otcauth_gpg_decrypt(auth_string))
	
	return xchat.EAT_NONE
# Hook the server event when gribble messages us.
xchat.hook_server("PRIVMSG", otcauth_gpg_auth)

	
# The callback function to our hook that ties it all together	
def otcauth_cb(word, word_eol, userdata):
	if len(word) < 2:
		switch = "help"
	else:
		switch = str(word[1]).lower()
	
	if switch == "help":
		otcauth_help(word[1:])
	elif switch == "version":
		otcauth_ver()
	elif switch == "eauth":
		nick = xchat.get_info('nick')
		xchat.command("MSG gribble eauth %s" % (nick))
	elif switch == "bauth":
		xchat.prnt("RESERVED FOR FUTURE FUNCTIONALITY")
	else:
		xchat.prnt("Invalid Option: %s not defined" % (word[1]))
	
	return xchat.EAT_XCHAT
	
# Hook our functions to the callback handler
xchat.hook_command("OTCAUTH", otcauth_cb, help="'/OTCAUTH help' for more help")
