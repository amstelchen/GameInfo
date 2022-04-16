# Maintainer: Michael John <amstelchen at gmail dot com>

pkgname=gameinfo
_pkgname=GameInfo
pkgver=1.0.3
pkgrel=1
pkgdesc='A system info tool for gamers.'
arch=('any')
url="http://github.com/amstelchen/GameInfo"
license=('GPL')
packager=('Michael John')
depends=('python' 'tk' 'hicolor-icon-theme' 'python-pyxdg' 'python-ttkthemes')
optdepends=('')
makedepends=(python-build python-installer)
source=("${pkgname}_${pkgver}.tar.gz"::"https://github.com/amstelchen/GameInfo/archive/refs/tags/${pkgver}.tar.gz")
sha256sums=('21cf223534d94e5c0f3723a2a89336d06bf1df673cbdb24feabde97d9b594dd3')

#build() {
#    python -m build --wheel --no-isolation
#}

package() {
    python -m installer --destdir="$pkgdir" dist/*.whl
}
