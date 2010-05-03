#!/usr/bin/python

'''
Copyright 2010 Michael Zoech and Andreas Pieber. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY MICHAEL ZOECH AND ANDREAS PIEBER ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL MICHAEL ZOECH, ANDREAS PIEBER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of Michael Zoech or Andreas Pieber.
'''

import sys
import subprocess
import dbus
import os

from config import Config 
from skype import SkypeWrapper
from pidgin import PidginWrapper

def buildDmenuCmd(config):
	params = [] 
	params.append("dmenu")
	if config.incase == 'True': params.append("-i")
	if config.vertical == 'True':
		params.append("-l")
		params.append(config.list)
		params.append("-h")
		params.append(config.height)
	if config.resize == 'True': params.append("-rs")
	if config.indicator == 'True': params.append("-ni")
	if config.xmms == 'True': params.append("-xs")
	if config.bottom == 'True': params.append("-b")
	if config.defx == 'True':
		params.append("-x")
		params.append(config.x)
	if config.defy == 'True':
		params.append("-y")
		params.append(config.y)
	if config.defw == 'True':
		params.append("-w")
		params.append(config.w)
	if config.deffn == 'True':
		params.append("-fn")
		params.append(config.fn)
	params.append("-nb")
	params.append(config.nb)
	params.append("-nf")
	params.append(config.nf)
	params.append("-sb")
	params.append(config.sb)
	params.append("-sf")
	params.append(config.sf)
	return params

def main():
	config = Config()
	
	bus = dbus.SessionBus()
	coll = {}

	if config.pidgin == 'True':
		pidgin = PidginWrapper(bus)
		coll.update(pidgin.lookup_friends())

	if config.skype == 'True':	
		skype = SkypeWrapper(bus)
		coll.update(skype.lookup_friends())
	
	dmenu = buildDmenuCmd(config)
	p = subprocess.Popen(dmenu, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	for proto, friends in coll.iteritems():
		for friend in friends:
			out = '%s on %s\n' % (friend['name'], proto.upper() if friend['on'] else proto)
			outencoded = out.encode("ascii", "replace")
			p.stdin.write(outencoded)

	wanted = p.communicate()[0]
	if wanted == "":
		return 0

	proto = wanted.split()[-1].lower()
	name = wanted[:wanted.rfind(' on ')]

	if proto == 'skype' and config.skype == 'True':
		skype.open_chat(name)
	else:
		pidgin.open_chat(proto, name)

	return 0

if __name__ == '__main__':
	sys.exit(main())

