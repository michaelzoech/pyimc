# Contributor: Michael Zoech <michi.zoech+arch at gmail>
# Contributor: Andreas Pieber <anpieber at gmail>
pkgname=pyimc
pkgver=0.2.0
pkgrel=1
pkgdesc="control Pidgin and Skype via command line"
arch=('any')
url="http://github.com/crazymaik/pyimc"
license=('BSD')
depends=('python')
optdepends=('skype' 'pidgin' 'dmenu')
makedepends=('setuptools')
install='pyimc.install'
source=(http://github.com/downloads/crazymaik/pyimc/$pkgname-$pkgver.zip)

build() {
  SRC=${srcdir}/"$pkgname-$pkgver"
  DOC='/usr/share/doc/pyimc/'

  echo "Installing pyimc"
  cd $SRC
  python setup.py build || return 1
  python setup.py install --root=${pkgdir} --optimize=1 || return 1

  echo "Installing docs"
  mkdir -p $DOC
  cp $SRC/CHANGELOG $DOC
  cp $SRC/LICENSE $DOC
  cp $SRC/README $DOC
}

md5sums=('d83e0e843956ac26b3db742968fb0d2e')

