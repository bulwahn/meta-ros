DESCRIPTION = "Low-level build system macros and infrastructure for ROS"
SECTION = "devel"
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://package.xml;beginline=7;endline=7;md5=d566ef916e9dedc494f5f793a6690ba5"

DEPENDS = "cmake ${PYTHON_PN}-empy-native ${PYTHON_PN}-pyparsing-native ${PYTHON_PN}-catkin-pkg-native"

SRC_URI = "https://github.com/ros/${ROS_SPN}/archive/${PV}.tar.gz;downloadfilename=${ROS_SP}.tar.gz"
SRC_URI[md5sum] = "c50589adde1d2783ab609772d83d9d11"
SRC_URI[sha256sum] = "a41d8bc889e9e5558d4c9688f6916f306e01a65edd5024fbcf42e7e357522786"

SRC_URI += "\
    file://0001-use-python-provided-by-environment-instead-of-the-ge.patch \
    file://0002-allow-proper-cross-compilation-with-catkin.patch \
    ${@'file://0003-python.cmake-look-for-python3-first.patch' if d.getVar('PYTHON_PN', True) == 'python3' else ''} \
    "

inherit catkin
