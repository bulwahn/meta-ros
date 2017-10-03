DESCRIPTION = "Python driver for MongoDB"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=2a944942e1496af1886903d274dedb13"
SRCNAME = "pymongo"

SRC_URI = "http://pypi.python.org/packages/source/p/pymongo/pymongo-${PV}.tar.gz"
SRC_URI[md5sum] = "70408f8115d7aa52fb6eef0e552834a6"
SRC_URI[sha256sum] = "f2018165823b341d83d398165d1c625e5db5cc779e7c44c107034407808463b6"

S = "${WORKDIR}/${SRCNAME}-${PV}"

inherit setuptools
