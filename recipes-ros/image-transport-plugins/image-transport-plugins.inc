SRC_URI = "https://github.com/ros-perception/${ROS_SPN}/archive/${PV}.tar.gz;downloadfilename=${ROS_SP}.tar.gz"
SRC_URI[md5sum] = "855253ebefbcf508d2af7dd3e8d5d15a"
SRC_URI[sha256sum] = "aed643f5a8306368456642b74d878875faf8e7b68d60818605ad921bbb7f7263"

S = "${WORKDIR}/${ROS_SP}/${ROS_BPN}"

inherit catkin

ROS_SPN = "image_transport_plugins"
