DESCRIPTION = "The control toolbox contains modules that are useful across all controllers."
SECTION = "devel"
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://package.xml;beginline=7;endline=7;md5=d566ef916e9dedc494f5f793a6690ba5"

DEPENDS = "rosconsole tf roscpp angles message-generation dynamic-reconfigure libtinyxml \
    realtime-tools message-filters control-msgs"

SRC_URI = "https://github.com/ros-controls/${ROS_SPN}/archive/${PV}.tar.gz;downloadfilename=${ROS_SP}.tar.gz"
SRC_URI[md5sum] = "3ad4d04d1ba3f09ed6078512a8466e55"
SRC_URI[sha256sum] = "2c15407db098d013d27bf9272a273170d19119cd1ed67c61ab78cb2ef95f662f"

S = "${WORKDIR}/${ROS_SP}"

inherit catkin
