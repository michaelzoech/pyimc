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

class PidginWrapper(object):
	def __init__(self, bus):
		try:
			obj = bus.get_object('im.pidgin.purple.PurpleService',
			                     '/im/pidgin/purple/PurpleObject')
			self.proxy = dbus.Interface(obj, 'im.pidgin.purple.PurpleInterface')
		except dbus.DBusException as e:
			self.proxy = None

	def lookup_friends(self):
		if self.proxy == None:
			return {}
		accounts = {}
		self.friends = {}
		self.accounts = {}
		for account in self.proxy.PurpleAccountsGetAllActive():
			proto = self.proxy.PurpleAccountGetProtocolName(account).lower()
			self.accounts[proto] = account
			self.friends[proto] = {}
			accounts[proto] = []
			for friend in self.proxy.PurpleFindBuddies(account, ''):
				name = self.proxy.PurpleBuddyGetAlias(friend)
				accounts[proto].append({'name': name, 'on': self.is_online(friend)})
				self.friends[proto][name] = friend
		return accounts

	def open_chat(self, proto, name):
		_name = self.proxy.PurpleBuddyGetName(self.friends[proto][name])
		conv = self.proxy.PurpleConversationNew(1, self.accounts[proto], _name)
		self.proxy.PurpleConversationPresent(conv)

	def is_online(self, friend):
		return self.proxy.PurpleBuddyIsOnline(friend)

	def toggle_roster(self):
		print 'WARNING: toggle of pidgin roster not implemented'
		None

