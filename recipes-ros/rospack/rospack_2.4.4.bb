DESCRIPTION = "ROS Package Tool"
SECTION = "devel"
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://package.xml;beginline=6;endline=6;md5=d566ef916e9dedc494f5f793a6690ba5"

DEPENDS = "boost cmake-modules ${PYTHON_PN}-rospkg-native libtinyxml"

SRC_URI = "https://github.com/ros/${ROS_SPN}/archive/${PV}.tar.gz;downloadfilename=${ROS_SP}.tar.gz \
           file://0001-Replaced-references-to-deprecated-Boost.TR1.patch \
           "
SRC_URI[md5sum] = "7911ea89c2e8f5b054db2684cbb9104e"
SRC_URI[sha256sum] = "68ff422777dad9e1237d6c774aa7d306bb222bb6ccfc4d1dda6b4124f2c3c0b0"

inherit catkin

RDEPENDS_${PN} = "${PYTHON_PN}-rosdep \
                  ${@'python-subprocess' if d.getVar('PYTHON_PN', True) == 'python' else ''}"
