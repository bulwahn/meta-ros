SRC_URI = "https://github.com/ros-perception/${ROS_SPN}/archive/${PV}.tar.gz;downloadfilename=${ROS_SP}.tar.gz"
SRC_URI[md5sum] = "18e99b77d2954788a8e3ec44786eca2c"
SRC_URI[sha256sum] = "37a7d85de5217d29689c7b18efdacb273fdc411176350bafff378f974d29def2"

S = "${WORKDIR}/${ROS_SP}/${ROS_BPN}"

inherit catkin

ROS_SPN = "vision_opencv"
