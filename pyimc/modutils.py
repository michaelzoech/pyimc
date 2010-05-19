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

import imp
import os
import sys

def get_available_commands():
	cmds = package_contents('commands')
	cmds.add('help')
	return cmds

def package_contents(pkgname):
	file, pathname, description = imp.find_module(pkgname)
	if file:
		raise ImportError('Not a package: %r', pkgname)
	modules = set([os.path.splitext(module)[0]
		for module in os.listdir(pathname)
		if module.endswith(('.py', '.pyc', '.pyo'))])
	modules.remove('__init__')
	return modules

def command_exists(cmdname):
	if (cmdname == 'help'):
		return True
	file, pathname, description = imp.find_module('commands')
	modpath = os.path.join(pathname, cmdname)
	return os.path.exists(modpath + '.py') or os.path.exists(modpath + '.pyc')

def load_command_module(modname):
	if modname != 'help':
		modname = 'commands.' + modname
	exec('import %s' % modname)
	return sys.modules[modname]

