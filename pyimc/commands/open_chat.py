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

import subprocess

class OpenChatCommand(object):
	@staticmethod
	def desc():
		return "shows a menu to create a new buddy chat"

	def run(this, config, pidgin, skype, args):
		coll = {}
		if config.pidgin == 'True':
			coll.update(pidgin.lookup_friends())
		if config.skype == 'True':
			coll.update(skype.lookup_friends())

		menu = config.menu.split()
		p = subprocess.Popen(menu, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

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
