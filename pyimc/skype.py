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

import dbus

class SkypeWrapper(object):
	def __init__(self, bus):
		try:
			self.proxy = bus.get_object('com.Skype.API', '/com/Skype')
			self.proxy.Invoke('NAME imcontrol')
			self.proxy.Invoke('PROTOCOL 8')
		except dbus.DBusException:
			self.proxy = None

	def lookup_friends(self):
		if self.proxy == None:
			return {}
		self.friends = {}
		accounts = {'skype': []}
		for friend in self.search_friends():
			name = self.get_name(friend)
			accounts['skype'].append({'name': name, 'on': self.is_online(friend)})
			self.friends[name] = friend
		return accounts

	def open_chat(self, name):
		friend = self.friends[name]
		res = self.proxy.Invoke('CHAT CREATE ' + friend)
		self.proxy.Invoke('OPEN CHAT ' + res.split()[1])

	def search_friends(self):
		res = self.proxy.Invoke('SEARCH FRIENDS')
		res = res.split(', ')
		res[0] = res[0].split()[1]
		return res

	def get_name(self, friend):
		res = self.proxy.Invoke('GET USER %s DISPLAYNAME' % friend)
		res = res.split()
		if len(res) == 3:
			res = self.proxy.Invoke('GET USER %s FULLNAME' % friend)
			res = res.split()
		if len(res) == 3:
			res += [friend]
		return ' '.join(res[3:])

	def is_online(self, friend):
		return self.proxy.Invoke('GET USER %s ONLINESTATUS' % friend).split()[3] != 'OFFLINE'

	def toggle_roster(self):
		state = self.proxy.Invoke('GET WINDOWSTATE').split()[1]
		self.proxy.Invoke('SET WINDOWSTATE ' + ('NORMAL' if state == 'HIDDEN' else 'HIDDEN'))

