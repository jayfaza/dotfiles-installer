# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# Maintainer: Your Name <youremail@domain.com>
pkgname=dotfiles-installer
pkgver=1.0
pkgrel=1
pkgdesc="Jayfaza dotfiles installer"
arch=(x86_64)
url="https://github.com/jayfaza/dotfiles-installer"
license=('GPL3')
depends=('ncurses' 'systemd-libs')
makedepends=('systemd' 'git' 'python' 'python-pipx')
source=("${pkgname}-${pkgver}::git+https://github.com/jayfaza/dotfiles-installer.git")
sha256sums=('SKIP')


build() {
	cd "$pkgname-$pkgver"
  pipx install .
}

package() {
  cd "$pkgname-$pkgver"
}


