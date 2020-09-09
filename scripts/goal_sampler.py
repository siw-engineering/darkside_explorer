#!/usr/bin/env python
"""
samples radial goals with current position for robot as the center
"""

# NOTE :
# 1. Prune the radial samples according  to reachablity (straight line exists without obstacles?)
# 2. Prune again based on robot circumfrence , with pruned goals as centre
# 3. If not goals reduce / increase sampling radius by relaxation factor
# 4. consider distance from last goal and difference in yaw for scoring next goal

# import rospy
import math
# from geometry_msgs import Pose, Point, PoseStamped


class Goal:
    
    def __init__(self, gpose, gain):
        self.pose = gpose
        self.gain = gain


class GoalSampler:

    def __init__(self):
        self.angular_step_size = None # determines the number of samples
        self.radial_length = None # in meters
        self.radial_relaxation = None # distance to increase or decrease if no goal found in meters
        self.robot_origin = None

    def get_radial_points(self, origin, radius, step_size):
        
        ang = 0 
        radial_points = []
        x, y = origin
        while ang < math.pi*2:  
            print(ang)                      
            radial_points.append((x + radius*math.cos(ang),y + radius*math.sin(ang)))
            ang += step_size
        
        return radial_points

    def is_reachable_in_straight_line(self, start_pos, end_pos):
        pass


    def get_reachable_points(self, start_coordinates, radial_points):

        reachable_points = []
        for point in radial_points:
            #convert point to cell coordinates
            x,y = point
            x = int(x / 0.05) # divide by map_resolution
            y = int(y / 0.05)
            cell_coord = (x,y)
            if self.is_reachable_in_straight_line(start_coordinates, end_pos=cell_coord):
                reachable_points.append(point)

        return reachable_points

    

    def compute_sample_gain(self, reachable_points):
        # TODO : compute gain
        pass


if __name__ == '__main__':
    import rospy
    rospy.init_node('goal_manager', anonymous=True)
    g = GoalSampler()
    pts = g.get_radial_points((100,100), 10, math.pi/4)
    print(pts)


