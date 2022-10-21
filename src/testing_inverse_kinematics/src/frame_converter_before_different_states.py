#!/usr/bin/python3


import rospy

from geometry_msgs.msg import Point

#import tf2_ros
from tf2_msgs.msg import TFMessage
from fiducial_msgs.msg import FiducialTransformArray
from geometry_msgs.msg import Transform
from geometry_msgs.msg import TransformStamped
import numpy as np
import std_msgs.msg as msg
import tf2_ros
from geometry_msgs.msg import Pose
import geometry_msgs.msg


def trans(t: Transform):

    # Get homegeneous transformation matrix from Transform (camera to aruco tag)

    w = t.Quaternion.w

    x = t.Quaternion.x

    y = t.Quaternion.y

    z = t.Quaternion.z

    T_C2A = np.array([[2*((w^2)+(x^2))-1, 2*(x*y-w*z), 2*(x*z+w*y), t.Vector3.x],

    [2*(x*y+w*z), 2*((w^2)+(y^2))-1, 2*(y*z-w*x), t.Vector3.y],

    [2*(x*z-w*y), 2*(y*z+w*x), 2*((w^2)+(z^2))-1, t.Vector3.z],

    [0, 0, 0, 1]])

 

    # Measured distances between centre of aruco tag and centre of robot base (initially set to 0)

    # Assuming exactly zero rotation between aruco tag and robot base (will need to be very precise or

    # change this, as it will fuck us up)



    # Multiply transformation matrix by translation from aruco tag to robot base

    T_A2R = np.array([1,0,0,x_dist],[0,1,0,y_dist],[0,0,1,z_dist],[0,0,0,1]) 
    return np.matmul(T_C2A, T_A2R)

state=2


def store_state(i):
    global state
    state = i.data


# id for the camera
#info_camera.header.frame_id = std::string("ximea_") + serial;

loop_count = 0
def T_C2R( p):
    print('converter')
    # maybe use fiducial vertices to get colour?????????????
    global camera_to_robot_base
    global pub
    global loop_count
    global listener
    global sub_transform
    global tfBuffer
    global msg,state
    
    #print('hi1')
    transform_array = []
    k=0
    
    if (p.transforms != []) and (state==2):
        print('in converter loop')
        for i,j in enumerate(p.transforms):
            #transform_array.append(j)
            #w = j.transform.rotation.w
            #x = j.transform.rotation.x
            #y = j.transform.rotation.y
            #z = j.transform.rotation.z
            #transform_array.append(np.array([
            #    [2*((w**2)+(x**2))-1, 2*(x*y-w*z), 2*(x*z+w*y), j.transform.translation.x],
            #    [2*(x*y+w*z), 2*((w**2)+(y**2))-1, 2*(y*z-w*x), j.transform.translation.y],
            #    [2*(x*z-w*y), 2*(y*z+w*x), 2*((w**2)+(z**2))-1, j.transform.translation.z],
            #    [ 0, 0, 0, 1]
            #]))

            j_id = j.fiducial_id

            if (j_id == 1) and (loop_count==0):
                camera_to_robot_base =  np.array([
                    [0 ,1 , 0, j.transform.translation.x],
                    [1 ,0 , 0, j.transform.translation.y],
                    [0 ,0 , -1, j.transform.translation.z],
                    [ 0, 0, 0, 1]
                ])
                loop_count=1
            else:
                transform_array.append(np.array([
                    [0 ,1 , 0, j.transform.translation.x],
                    [1 ,0 , 0, j.transform.translation.y],
                    [0 ,0 , -1, j.transform.translation.z],
                    [ 0, 0, 0, 1]
                ]))


            print(transform_array)
            k +=1
            print(state)
            #print(j_id)
            #print(j_id,'\n',j.transform.translation)

        # id is 17

        #camera_to_robot = np.array([
        #        [0,1 , 0, x_dist],
        #        [1,0 , 0, y_dist],
        #        [0 ,0 , -1, z_dist],
        #        [ 0, 0, 0, 1]
        #    ])
        x_dist = -0.032
        y_dist = -0.02
        z_dist = -0.04
        robot_base_to_robot_joint = np.array([
                [1,0 , 0, x_dist],
                [0,1 , 0, y_dist],
                [0 ,0 , 1, z_dist],
                [ 0, 0, 0, 1]
        ])
        #print('cam to robot',camera_to_robot)
        camera_to_tag_1 = transform_array[0]
        #print('camner to tag',camera_to_tag_1)
        ##camera_to_tag_2 = transform_array[1]
        #camera_to_robot = 
        robot_base_to_tag_1 = np.matmul(np.linalg.inv(camera_to_robot_base),camera_to_tag_1)
        robot_to_tag_1 = np.matmul(np.linalg.inv(robot_base_to_robot_joint),robot_base_to_tag_1)
        ##print(robot_to_tag_1)


        msg = Pose()
        msg.position.x = robot_to_tag_1[0][3]
        msg.position.y =  robot_to_tag_1[1][3]
        msg.position.z = robot_to_tag_1[2][3]

        pub.publish(msg)
    elif state==4:
        
        transform_array.append(np.array([
            [0 ,1 , 0, 0],
            [1 ,0 , 0, -0.025],
            [0 ,0 ,-1, 0.25],
            [ 0, 0, 0, 1]
        ]))
        x_dist = -0.032
        y_dist = -0.02
        z_dist = -0.04
        robot_base_to_robot_joint = np.array([
                [1,0 , 0, x_dist],
                [0,1 , 0, y_dist],
                [0 ,0 , 1, z_dist],
                [ 0, 0, 0, 1]
        ])
        print(state)
        #print('cam to robot',camera_to_robot)
        camera_to_tag_1 = transform_array[0]
        #print('camner to tag',camera_to_tag_1)
        ##camera_to_tag_2 = transform_array[1]
        #camera_to_robot = 
        robot_base_to_tag_1 = np.matmul(np.linalg.inv(camera_to_robot_base),camera_to_tag_1)
        robot_to_tag_1 = np.matmul(np.linalg.inv(robot_base_to_robot_joint),robot_base_to_tag_1)
        #print(robot_to_tag_1)


        msg = Pose()
        msg.position.x = robot_to_tag_1[0][3]
        msg.position.y =  robot_to_tag_1[1][3]
        msg.position.z = robot_to_tag_1[2][3]
        pub.publish(msg)
    else:
        
        pub.publish(msg)


    #this is how to do it with tfmessage
    #print(p.transforms[0].child_frame_id,p.transforms[0].transform.translation)
    '''
    try:
        print('hi2')
        #trans = tfBuffer.lookup_transform("fiducial_12","ximea_31704051")
        #print(trans)
    except:
        d=1
    #'''


    
    #robot_frame_p = np.matmul(sub_transform, np.array([p.transforms.transform.translation.x],[p.transform.translation.y],[p.transform.translation.z],[1]))



    #msg = Point(robot_frame_p[0],robot_frame_p[1],robot_frame_p[2])
    #print(msg)
    #pub.publish(msg)


def main():
    global pub
    global listener
    global sub_transform,tfBuffer
    
    #tfBuffer = tf2_ros.Buffer()
    #listener = tf2_ros.TransformListener(tfBuffer)
    sub_transform = np.array([[1,0,0,0],[0,1,0,-0.3],[0,0,1,0.5],[0,0,0,1]])

    pub = rospy.Publisher('desired_position', Pose, queue_size=10)
    #sub_transform = rospy.Subscriber('tf', Transform, trans)
    sub = rospy.Subscriber(
        'state', # Topic name
        msg.Int16, # Message type
        store_state # Callback function (required)
    )
    #sub_point = rospy.Subscriber('tf',TFMessage, T_C2R)#replace placeholders with actual topics
    sub_point = rospy.Subscriber('fiducial_transforms',FiducialTransformArray, T_C2R)#replace placeholders with actual topics
    rospy.init_node('frame_converter')
    rospy.spin()


if __name__=='__main__':
    loop_count = 0
    main()          