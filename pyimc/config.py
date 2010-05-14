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

import os
import ConfigParser
import sys

class Config(object):
	"""
	A object to wrap a dictionary for easier configuration access.

	Based on Storage in web.py (public domain)
	"""
	def __init__(self):
		self._config = {
			# general options
			'skype': 'True',
			'pidgin': 'True',
			# horicontal options
			'menu': 'dmenu'}
		config_file = os.path.expanduser('~/.pyimcrc')
		if os.path.lexists(config_file):
			try:
				parser = ConfigParser.SafeConfigParser()
				f = open(config_file)
				parser.readfp(f)
				self._config.update(dict(parser.items('DEFAULT', raw=True)))
			except (IOError, ConfigParser.ParsingError), e:
				print >> sys.stderr, "Configuration file can not be read %s\n%s" % (config_file, e)
				sys.exit(1)

	def get_config(self):
		''' Get the contained configuration.'''
		return self._config

	def __getattr__(self, key):
		try:
			return self._config[key]
		except KeyError, k:
			raise AttributeError, k

	def __setattr__(self, key, value):
		if key == '_config':
			object.__setattr__(self, key, value)
		else:
			self._config[key] = value

	def __delattr__(self, key):
		try:
			del self._config[key]
		except KeyError, k:
			raise AttributeError, k

	# For container methods pass-through to the underlying config.
	def __getitem__(self, key):
		return self._config[key]

	def __setitem__(self, key, value):
		self._config[key] = value

	def __delitem__(self, key):
		del self._config[key]

	def __repr__(self):
		return '<Storage ' + repr(self._config) + '>'

