#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Pose
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

class DarksideVisualizer:

    def __init__(self):
        self.goal_position = rospy.Publisher('/darkside_explorer/local_goal', MarkerArray, queue_size=1)
        self.marker_id = 0

    def make_marker(self, marker_pose, scale_=[0.1,0.1,0.1], color_=(0,1,0,1), lifetime_=30):
        marker_ = Marker()
        marker_.id = self.marker_id
        self.marker_id +=1
        marker_.header.frame_id = "/X1/map"
        # marker_.header.stamp = rospy.Time.now()
        marker_.type = marker_.SPHERE
        marker_.action = marker_.ADD

        marker_.pose = marker_pose

        marker_.lifetime = rospy.Duration.from_sec(lifetime_)

        marker_.scale.x = scale_[0]
        marker_.scale.y = scale_[1]
        marker_.scale.z = scale_[2]
        marker_.color.a = 0.5
        red_, green_, blue_, a_ = color_
        marker_.color.r = red_
        marker_.color.g = green_
        marker_.color.b = blue_
        marker_.color.a = a_
        return marker_

    def make_pose(self, robot_pose, point):
        pose_t = robot_pose
        pose_t.position.x, pose_t.position.y= point

        return pose_t

    def publish_markers(self, markers):
        #for marker in markers:
        self.goal_position.publish(markers)


def get_points(rpose):
    points = g.get_radial_points((rpose.position.x,rpose.position.y), radius=2, step_size=math.pi/2)
    print("POINTS : ", len(points))
    pose_array = [viz.make_pose(rpose, point ) for point in points]
    print("POSES : ", len(pose_array))
    markerArray = MarkerArray()
    for pose in pose_array:
        markerArray.markers.append(viz.make_marker(pose))
    return markerArray

def poseCallback(msg):
    markers = get_points(msg)
    print("MARKERS :", len(markers.markers))
    viz.publish_markers(markers)
    rospy.loginfo("Displaying marker")

if __name__ == '__main__':
    rospy.init_node('viz_manager', anonymous=True)
    from goal_sampler import GoalSampler
    g = GoalSampler()
    viz = DarksideVisualizer()
    rospy.Subscriber("/robot_pose", Pose, poseCallback)
    rospy.spin()