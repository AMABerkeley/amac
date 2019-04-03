#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from math import sqrt, atan, pi

global x_velocity_from_cmd_vel
global y_velocity_from_cmd_vel
global steering_from_cmd_vel
global steering_ang_from_cmd_vel
x_velocity_from_cmd_vel = 0.0
y_velocity_from_cmd_vel = 0.0
steering_from_cmd_vel = 0.0
steering_ang_from_cmd_vel = 0.0
	
def callback(data): 
	
	global x_velocity_from_cmd_vel
	global y_velocity_from_cmd_vel
	global steering_from_cmd_vel
	global steering_ang_from_cmd_vel
	x_velocity_from_cmd_vel = data.linear.x
	y_velocity_from_cmd_vel = data.linear.y
	steering_from_cmd_vel = data.angular.z
	steering_ang_from_cmd_vel = atan(steering_from_cmd_vel) * .26*180/pi


def listener():

	rospy.init_node('twistToCmd', anonymous=True)
	twist_sub = rospy.Subscriber('cmd_vel', Twist, callback)

def convert():
	global x_velocity_from_cmd_vel
	global y_velocity_from_cmd_vel
	global steering_from_cmd_vel
	global steering_ang_from_cmd_vel

	vel_pub = rospy.Publisher('velocity_ms', Float32,  queue_size=10)
	turn_pub = rospy.Publisher('turning', Float32,  queue_size=10)

	rate = rospy.Rate(40)

	while not rospy.is_shutdown():
			
		rospy.loginfo("steering_ang_from_cmd_vel")
		rospy.loginfo(steering_ang_from_cmd_vel)
		turn_pub.publish(steering_ang_from_cmd_vel)

		velocity_from_cmd_vel = sqrt(x_velocity_from_cmd_vel**2 + y_velocity_from_cmd_vel**2)
		rospy.loginfo("velocity_from_cmd_vel")
		rospy.loginfo(velocity_from_cmd_vel)
		vel_pub.publish(velocity_from_cmd_vel)
		rate.sleep()


if __name__ == '__main__':
	try:
		listener()
		convert()
	except rospy.ROSInterruptException:
		pass

