DESCRIPTION = "yaml-cpp is a YAML parser and emitter in C++ matching the YAML 1.2 spec"
HOMEPAGE = "https://github.com/jbeder/yaml-cpp/"
SECTION = "libs"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://license.txt;md5=7c6a629da965ebdfba9f6fdb76ab8ab4"

DEPENDS = "boost"

PR = "r0"

S = "${WORKDIR}/yaml-cpp-release-${PV}"

SRC_URI = "https://github.com/jbeder/yaml-cpp/archive/release-${PV}.tar.gz"
SRC_URI[md5sum] = "96bdfa47d38711737d973b23d384d4f2"
SRC_URI[sha256sum] = "60d8ad7bdb925ed0b53529713ffe0271965870435f72bd196aed5a7e3f073ec2"

EXTRA_OECMAKE = "-DBUILD_SHARED_LIBS=ON"

inherit cmake
