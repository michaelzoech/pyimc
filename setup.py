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

from setuptools import setup, find_packages

class UltraMagicString(object):
    ''' Stolen from http://stackoverflow.com/questions/1162338/whats-the-right-way-to-use-unicode-metadata-in-setup-py

    Catch-22:
    - if I return Unicode, python setup.py --long-description as well
      as python setup.py upload fail with a UnicodeEncodeError
    - if I return UTF-8 string, python setup.py sdist register
      fails with an UnicodeDecodeError
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value.decode('UTF-8')

    def __add__(self, other):
        return UltraMagicString(self.value + str(other))

    def split(self, *args, **kw):
        return self.value.split(*args, **kw)

setup(name='pyimc',
      version = '0.1.0',
      description = 'Provide command line control over a wide range of different instant messanger, such as skype or pidgin.',
      maintainer = 'Michael Zoech, Andreas Pieber',
      maintainer_email = 'anpieber at gmail dot com, maik at 0x2a dot at',
      url = 'http://github.com/crazymaik/pyimc',
      classifiers = [f.strip() for f in """
        Development Status :: 5 - Production/Stable
        Environment :: Console
        Operating System :: OS Independent
        Programming Language :: Python
        Programming Language :: Python :: 2.6
        Intended Audience :: Developer/Desktop
        License :: OSI Approved :: BSD  
        Topic :: Tools :: Development :: Version Management
        """.splitlines() if f.strip()],
      license = 'BSD',
      install_requires = [ ],
      packages = find_packages(),
      entry_points = {'console_scripts': [ 'pyimc = pyimc.pyimc:main']}
     )

