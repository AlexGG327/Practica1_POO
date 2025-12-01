cd ros2_jazzy
source /opt/ros/jazzy/setup.bash

ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py nav2:=true slam:=false localization:=true rviz:=true
