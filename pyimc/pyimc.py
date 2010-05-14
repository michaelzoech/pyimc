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
import dbus

from config import Config
from skype import SkypeWrapper
from pidgin import PidginWrapper
from commands.open_chat import OpenChatCommand
from commands.toggle_roster import ToggleRosterCommand

commands = {
	"openchat": OpenChatCommand,
	"toggle": ToggleRosterCommand
}

def usage():
	print 'USAGE: pyimc <command> [<args>]'
	print 'Supported commands:'
	for (k,v) in commands.iteritems():
		print '    %-10s %s' % (k,v.desc())

def main():
	args = sys.argv
	config = Config()
	bus = dbus.SessionBus()

	pidgin = PidginWrapper(bus) if config.pidgin == 'True' else None
	skype = SkypeWrapper(bus) if config.skype == 'True' else None

	if len(args) <= 1:
		usage()
		return -1

	if args[1] not in commands:
		print "ERROR: Unknown command '%s'" % args[1]
		usage()
		return -1

	cmd = commands[args[1]]()
	cmd.run(config, pidgin, skype, args[2:])

	return 0

if __name__ == '__main__':
	sys.exit(main())

