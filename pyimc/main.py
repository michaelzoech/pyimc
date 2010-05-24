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

import modutils
from config import Config
from skype import SkypeWrapper
from pidgin import PidginWrapper
from help import usage

def main():
	config = Config()
	bus = dbus.SessionBus()

	pidgin = PidginWrapper(bus) if config.pidgin == 'True' else None
	skype = SkypeWrapper(bus) if config.skype == 'True' else None

	if len(sys.argv) <= 1:
		usage()
		return -1

	action = sys.argv[1]
	args = sys.argv[2:]

	mod = modutils.load_command_module(action)
	if mod == None:
		print "ERROR: Unknown command '%s'" % action
		usage()
		return -1

	mod.execute(config, pidgin, skype, args)

	return 0

