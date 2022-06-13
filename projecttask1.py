#! /usr/bin/env python

# Make the node an executable node
# chmod u+x ~/catkin_ws/src/beginner_tutorials/src/projecttask1.py

import rospy
import sys
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

move = Twist()
move.linear.x = 1
move.angular.z = 0.0
mindistance = 1
stopdistance = 0.4
stop = 0
obstacle = False
rounds = 0
movespeed = 1

nodeid = str(sys.argv[1])
nodename = 'robot_' + nodeid
rospy.init_node(nodename, anonymous=True)
pub = rospy.Publisher(nodename + '/cmd_vel', Twist, queue_size=10)
rate = rospy.Rate(10)

def callback(msg):
	global obstacle 
	obstacle = False
	size = len(msg.ranges)	

	for i in range(0, size):
		if float(msg.ranges[i]) < mindistance and float(msg.ranges[i]) != 0.0 :		
			#print(i, msg.ranges[i])			
			obstacle = True

		if float(msg.ranges[i]) <= stopdistance or rounds >= 4:
			stop = 1	
			move.linear.x = 0.0
			move.angular.z = 0.0
			pub.publish(move)

def rotatetask(speed,angle,clockwise,lspeed=0):
	angular_speed = speed * (math.pi / 180)
	relative_angle = angle * (math.pi / 180)

	move.linear.x = lspeed	
	move.angular.z = clockwise * angular_speed

	t0 = rospy.Time.now().to_sec()
	current_angle = 0

	while(current_angle < relative_angle):
		print("rotating");
		pub.publish(move)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed * (t1 - t0)
		rate.sleep()

	move.angular.z = 0.0
	pub.publish(move)

def moving(distance):
	
	move.linear.x= movespeed
	t0 = rospy.Time.now().to_sec()
	current_distance = 0

	while(current_distance < distance):
		pub.publish(move)
		print("moving")	
		t1 = rospy.Time.now().to_sec()
		current_distance = movespeed * (t1 - t0)
		rate.sleep()

	move.linear.x = 0.0
	move.angular.z = 0.0
	pub.publish(move)


def rotate(direciton):
	global obstacle
	global rounds
	while(obstacle != False):
		rotatetask(5.0,90.0,direciton)
		moving(1)
		rotatetask(5.0,90.0,direciton)
		rounds = rounds + 1

rounds=0
def movecontrol():
	global obstacle
	global rounds
	while obstacle != True:
		move.linear.x = movespeed
		move.angular.z = 0.0
		print("moving")	
		pub.publish(move)
		rate.sleep()

	if rounds == 0:
		if int(sys.argv[1])==0:
			rotate(1)
			movecontrol()
		else:
			rotate(-1)
			movecontrol()
	elif rounds ==1:
		if int(sys.argv[1])==0:
			rotatetask(5.0,90.0,-1)
			moving(1)
			rotatetask(5.0,90.0,-1)
			rounds=rounds + 1
			movecontrol()
		else:
			rotatetask(5.0,90.0,1)
			moving(1)
			rotatetask(5.0,90.0,1)
			rounds=rounds + 1
			movecontrol()
		
	elif rounds==2:
		if int(sys.argv[1])==0:
			rotate(1)
			moving(8)	
		else:
			rotate(-1)
			moving(8)	

sub = rospy.Subscriber(nodename+'/base_scan', LaserScan, callback)
movecontrol()
rospy.spin()
