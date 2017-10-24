SRC_URI = "https://github.com/ros-industrial/${ROS_SPN}/archive/${PV}.tar.gz;downloadfilename=${ROS_SP}.tar.gz"
SRC_URI[md5sum] = "5c8b1f5d417d61e19c4ed78b25ca2ba2"
SRC_URI[sha256sum] = "c5b1665a17ca5f10253f113e1f0e478921f6fbbf00c0a380aacb8164becce457"

S = "${WORKDIR}/${ROS_SPN}-${PV}/${ROS_BPN}"

inherit catkin

ROS_SPN = "ros_canopen"
