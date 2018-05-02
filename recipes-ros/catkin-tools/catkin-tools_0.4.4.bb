DESCRIPTION = "Command line tools for working with catkin"
HOMEPAGE = "http://catkin-tools.readthedocs.io"
SECTION = "devel/python"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=95183d79271344f1c8ade910eda4deb2"

ROS_SPN = "catkin_tools"

SRC_URI = "https://github.com/catkin/${ROS_SPN}/archive/${PV}.tar.gz"
SRCREV="a5db715ef4dd9176d079d2a01ae2f7a57f9c9536"
SRC_URI[md5sum] = "0946b54a708bfd638c936494e94bf7d4"
SRC_URI[sha256sum] = "5706c971790bca2ee8245b97fe744e4841053588c786ca604d17f81744e8c105"

S = "${WORKDIR}/${ROS_SPN}-${PV}"

RDEPENDS_${PN} = "python-catkin-pkg python-osrf-pycommon python-pyyaml python-trollius"
RDEPENDS_${PN}_class-nativesdk = "nativesdk-python-setuptools"

FILES_${PN} = " \
  ${bindir} \
  ${datadir} \
  ${sysconfdir} \
"

inherit setuptools

do_install_append_class-nativesdk () {
  sed -i 's|${SDKPATHNATIVE}||g' ${D}${bindir}/catkin
}

BBCLASSEXTEND = "native nativesdk"
FILES_${PN}_append_class-nativesdk = " ${SDKPATHNATIVE}"
