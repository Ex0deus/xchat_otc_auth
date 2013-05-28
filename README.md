OTC Auth Tool for XChat2 IRC Client
========================================================================
This is the first version of this tool
updates are planned for the future.

In the current state of the tool, one simply need load the tool and do
"/otcauth eauth". 
The script makes the assumptions that you are using everything as
default. Assumes you use the gpghome as set by GPGs default settings.
It also makes use of the gpg-agent program should a password be needed.
And one last assumption... it also assumes that your otc auth nick is 
the very same as the nick your using.

Plans are in place to add some other functionality such as gpg
authentication via the clearsign method, and also a way to harness that
functionality for personal gpg based contracts.

Other future developements include "bauth".
BAUTH will be a bitcoin address authentication process that will be 
automated.

This script has a few python module dependencies.
- GnuPG python module. (gnupg.py)
- pycURL URL Handler. (pycurl.py)

Report errors and feature requests on github

Input is welcome.
