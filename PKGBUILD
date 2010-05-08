# Contributor: Michael Zoech <michi.zoech+arch at gmail>
# Contributor: Andreas Pieber <anpieber at gmail>
pkgname=pyimc
pkgver=0.1.0
pkgrel=1
pkgdesc="control Pidgin and Skype via command line"
arch=('any')
url="http://github.com/crazymaik/pyimc"
license=('BSD')
depends=('python')
optdepends=('skype' 'pidgin' 'dmenu')
makedepends=('setuptools')
source=(http://github.com/downloads/crazymaik/pyimc/$pkgname-$pkgver.zip)

build() {
  cd ${srcdir}/"$pkgname-$pkgver"
  python setup.py build || return 1
  python setup.py install --root=${pkgdir} --optimize=1 || return 1
}

md5sums=('160ce50904c71d723a0fd33ea1388a90')
