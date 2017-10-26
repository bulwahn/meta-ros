DESCRIPTION = "Low-level build system macros and infrastructure for ROS"
SECTION = "devel"
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://package.xml;beginline=7;endline=7;md5=d566ef916e9dedc494f5f793a6690ba5"

DEPENDS = "cmake-native ${PYTHON_PN}-empy-native ${PYTHON_PN}-catkin-pkg-native"

SRC_URI = "https://github.com/ros/${ROS_SPN}/archive/${PV}.tar.gz;downloadfilename=${ROS_SP}.tar.gz"
SRC_URI[md5sum] = "f958ca71ba921db6855821de2a6df70c"
SRC_URI[sha256sum] = "468725aadfd6b615cd7d7a75fca37777db987b6ad63f73062c3273bd96d380d6"

SRC_URI += "\
    file://0001-CATKIN_WORKSPACES-Don-t-require-.catkin-file.patch \
    file://0001-use-python-provided-by-environment-instead-of-the-ge.patch \
    file://0001-avoid-using-host-s-paths-when-cross-compiling.patch \
    file://0001-relocate-dependency-s-headers-to-current-sysroot.patch \
    ${@'file://0001-python.cmake-look-for-python3-first.patch' if d.getVar('PYTHON_PN', True) == 'python3' else ''} \
    "

inherit catkin

FILES_${PN}-dev += "\
    ${ros_datadir}/eigen/cmake \
    ${ros_datadir}/ros/cmake \
    ${ros_datadir}/.catkin \
    ${ros_prefix}/.catkin \
    ${ros_prefix}/.rosinstall \
    ${ros_prefix}/_setup_util.py \
    ${ros_prefix}/env.sh \
    ${ros_prefix}/setup.* \
    "

