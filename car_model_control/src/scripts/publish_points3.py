#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

def data_provider():
	
	rospy.init_node('publish_points3',anonymous=True)
	rospy.Subscriber("/scan",LaserScan,callback)
	rospy.spin()

def callback(SensorData):
	flag = False
	counter=0
	client.wait_for_server()
	goal_pose = MoveBaseGoal()
	goal_pose.target_pose.header.frame_id = 'base_footprint'
	goal_pose.target_pose.pose.orientation.x = 0
	goal_pose.target_pose.pose.orientation.y = 0
	goal_pose.target_pose.pose.orientation.z = 0
	goal_pose.target_pose.pose.orientation.w = 1
	for m in range (150,250):
		if(SensorData.ranges[m]<3):
			flag = True
			break
	if(flag==True):
		counter1=0
		counter2=0		
		for j in range (1,200):
			if(SensorData.ranges[j]<3):
				counter1=counter1+1				
		for k in range (200,400):
			if(SensorData.ranges[k]<3):
				counter2=counter2+1
		if (counter1>counter2):	
			client.cancel_all_goals()
			goal_pose.target_pose.pose.position.x = 0.5
			goal_pose.target_pose.pose.position.y = 0.05
			goal_pose.target_pose.pose.position.z = 0
			client.send_goal(goal_pose)
		elif (counter1<counter2):
			client.cancel_all_goals()
			goal_pose.target_pose.pose.position.x = 0.5
			goal_pose.target_pose.pose.position.y = -0.05
			goal_pose.target_pose.pose.position.z = 0
			client.send_goal(goal_pose)
		else:
			client.cancel_all_goals()
			goal_pose.target_pose.pose.position.x = 0.3
			goal_pose.target_pose.pose.position.y = 0.2
			goal_pose.target_pose.pose.position.z = 0
			client.send_goal(goal_pose)
	else:	
		client.cancel_all_goals()	
		goal_pose.target_pose.pose.position.x = 0.5
		goal_pose.target_pose.pose.position.y = 0
		goal_pose.target_pose.pose.position.z = 0
		client.send_goal(goal_pose)
			
	
	
if __name__ == '__main__':
	rospy.sleep(10.)
	while(True):
		try:data_provider()
		except rospy.ROSInterruptException: pass
			
		
		
				
