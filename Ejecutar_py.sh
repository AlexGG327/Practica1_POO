source /opt/ros/jazzy/setup.bash
cd ~/turtlebot4_ws
colcon build --symlink-install --packages-select turtlebot4_python_tutorials
source install/local_setup.bash

ros2 run meshtastic_package meshtastic_node

