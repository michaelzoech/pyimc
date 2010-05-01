#!/usr/bin/python

import sys
import subprocess
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
		self.proxy.PurpleConverstationPresent(conv)

	def is_online(self, friend):
		return self.proxy.PurpleBuddyIsOnline(friend)

def main():
	bus = dbus.SessionBus()
	pidgin = PidginWrapper(bus)
	skype = SkypeWrapper(bus)

	coll = skype.lookup_friends()
	coll.update(pidgin.lookup_friends())

	dmenu = ["dmenu","-i","-l","10","-rs","-ni","-xs","-x","680","-y","200","-w","240"
	        ,"-fn", "\"-*-verdana-medium-r-*-*-16-*-*-*-*-*-iso10646-1\""]
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

	if proto == 'skype':
		skype.open_chat(name)
	else:
		pidgin.open_chat(proto, name)

	return 0

if __name__ == '__main__':
	sys.exit(main())

