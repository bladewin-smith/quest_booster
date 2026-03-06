# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import rospy
# from sensor_msgs.msg import JointState
# # from piper_msgs.msg import PosCmd
# from std_msgs.msg import Header

# class PIPER:
#     def __init__(self):
        
#         # 发布控制piper机械臂话题
#         # self.pub_descartes = rospy.Publisher('pos_cmd', PosCmd, queue_size=10)
#         self.pub_joint = rospy.Publisher('/joint_states', JointState, queue_size=1)
#         self.left_pub_joint = rospy.Publisher('/left_joint_states', JointState, queue_size=1)
#         self.right_pub_joint = rospy.Publisher('/right_joint_states', JointState, queue_size=1)
#         # self.descartes_msgs = PosCmd()
        
#         # self.rate = rospy.Rate(80) # 10hz
#         self.target_joint_state = rospy.get_param('~target_joint_state', default=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        
#         # 订阅joint_states_single话题获取当前关节位置
#         rospy.Subscriber(f'joint_states_single', JointState, self.joint_states_callback, queue_size=1)
        
#         # 存储当前关节位置
#         self.current_joint_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
#         # 标记是否已获取到当前关节位置
#         self.joint_positions_received = False
        
#     # def init_pose(self):
#     #     joint_states_msgs = JointState()
#     #     joint_states_msgs.header = Header()
#     #     joint_states_msgs.header.stamp = rospy.Time.now()
#     #     joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
#     #     joint_states_msgs.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#     #     self.pub_joint.publish(joint_states_msgs)
#     #     # self.rate.sleep()
#     #     print("send joint control piper command")
    
#     def joint_states_callback(self, msg):
#         """
#         处理从joint_states_single话题接收到的关节状态数据
#         """
#         # 确保消息中包含关节位置数据
#         if len(msg.position) >= 7:
#             # 更新当前关节位置
#             self.current_joint_positions = list(msg.position[:7])
#             # 标记已接收到关节位置数据
#             self.joint_positions_received = True
#             # rospy.logdebug(f"接收到当前关节位置: {self.current_joint_positions}")
            
#     # 使用线性插值实现平滑过渡到初始位置
#     def init_pose(self):
#         # 目标关节位置
#         target_joint_state = self.target_joint_state
        
#         # 获取当前关节位置
#         # 如果已经接收到关节位置数据，使用实际的当前位置
#         # 否则会一步调整到位
#         if self.joint_positions_received:
#             current_positions = self.current_joint_positions
#             rospy.loginfo(f"使用实际的当前关节位置: {current_positions}")
            
#             # 设置过渡时间和控制频率
#             duration = 0.5  # 过渡持续时间(秒)
#             rate = 50  # 控制频率(Hz)
            
#             # 计算总步数
#             steps = int(duration * rate)
            
#             # 计算每一步的增量
#             increments = [(target - current) / steps for current, target in zip(current_positions, target_joint_state)]
            
#             # 创建ROS的Rate对象控制循环频率
#             rate_obj = rospy.Rate(rate)
            
#             # 记录开始时间（用于日志）
#             start_time = rospy.Time.now()
            
#             # 逐步移动到目标位置k
#             for step in range(steps + 1):
#                 # 计算当前步骤的位置
#                 interpolated_positions = [current + increment * step for current, increment in zip(current_positions, increments)]
                
#                 # 发布关节状态消息
#                 joint_states_msgs = JointState()
#                 joint_states_msgs.header = Header()
#                 joint_states_msgs.header.stamp = rospy.Time.now()
#                 joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
#                 joint_states_msgs.position = interpolated_positions
                
#                 # 发布消息
#                 self.pub_joint.publish(joint_states_msgs)
                
#                 # 按照指定频率控制循环
#                 rate_obj.sleep()
            
#             # 确保最后一帧是精确的目标位置
#             joint_states_msgs = JointState()
#             joint_states_msgs.header = Header()
#             joint_states_msgs.header.stamp = rospy.Time.now()
#             joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
#             joint_states_msgs.position = target_joint_state
#             self.pub_joint.publish(joint_states_msgs)
            
#             # 计算实际用时
#             elapsed_time = (rospy.Time.now() - start_time).to_sec()
#             # print(f"平滑移动到初始位置完成，用时: {elapsed_time:.2f}秒")
            
#         else:
#             start_time = rospy.Time.now()  # 获取当前时间
#             while (rospy.Time.now() - start_time).to_sec() < 0.5:  # 持续发送0.5秒
#                 joint_states_msgs = JointState()
#                 joint_states_msgs.header = Header()
#                 joint_states_msgs.header.stamp = rospy.Time.now()
#                 joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
#                 joint_states_msgs.position = target_joint_state
#                 self.pub_joint.publish(joint_states_msgs)
#             # print("send joint control piper command for 2 seconds")
#             # 使用默认的非零位置作为起始点
#             # current_positions = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
#             # rospy.loginfo("未接收到当前关节位置，使用默认初始位置")
            
        
        
#     def left_init_pose(self):
#         joint_states_msgs = JointState()
#         joint_states_msgs.header = Header()
#         joint_states_msgs.header.stamp = rospy.Time.now()
#         joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
#         joint_states_msgs.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#         self.left_pub_joint.publish(joint_states_msgs)
#         # self.rate.sleep()
#         print("send joint control piper command")
        
#     def right_init_pose(self):
#         joint_states_msgs = JointState()
#         joint_states_msgs.header = Header()
#         joint_states_msgs.header.stamp = rospy.Time.now()
#         joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
#         joint_states_msgs.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#         self.right_pub_joint.publish(joint_states_msgs)
#         # self.rate.sleep()
#         print("send joint control piper command")
        
#     def descartes_control_piper(self,x,y,z,roll,pitch,yaw,gripper):
#         self.descartes_msgs.x = x
#         self.descartes_msgs.y = y
#         self.descartes_msgs.z = z
#         self.descartes_msgs.roll = roll
#         self.descartes_msgs.pitch = pitch
#         self.descartes_msgs.yaw = yaw
#         self.descartes_msgs.gripper = gripper
#         self.pub_descartes.publish(self.descartes_msgs)
#         # print("send descartes control piper command")
    
#     def joint_control_piper(self,j1,j2,j3,j4,j5,j6,gripper):
#         joint_states_msgs = JointState()
#         joint_states_msgs.header = Header()
#         joint_states_msgs.header.stamp = rospy.Time.now()
#         joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
#         joint_states_msgs.position.append(j1)
#         joint_states_msgs.position.append(j2)
#         joint_states_msgs.position.append(j3)
#         joint_states_msgs.position.append(j4)
#         joint_states_msgs.position.append(j5)
#         joint_states_msgs.position.append(j6)
#         joint_states_msgs.position.append(gripper)
#         self.pub_joint.publish(joint_states_msgs)
#         # self.rate.sleep()
#         print("send joint control piper command")
    
#     def left_joint_control_piper(self,j1,j2,j3,j4,j5,j6,gripper):
#         joint_states_msgs = JointState()
#         joint_states_msgs.header = Header()
#         joint_states_msgs.header.stamp = rospy.Time.now()
#         joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
#         joint_states_msgs.position.append(j1)
#         joint_states_msgs.position.append(j2)
#         joint_states_msgs.position.append(j3)
#         joint_states_msgs.position.append(j4)
#         joint_states_msgs.position.append(j5)
#         joint_states_msgs.position.append(j6)
#         joint_states_msgs.position.append(gripper)
#         self.left_pub_joint.publish(joint_states_msgs)
#         # self.rate.sleep()
#         print("send joint control piper command")
        
    
#     def right_joint_control_piper(self,j1,j2,j3,j4,j5,j6,gripper):
#         joint_states_msgs = JointState()
#         joint_states_msgs.header = Header()
#         joint_states_msgs.header.stamp = rospy.Time.now()
#         joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
#         joint_states_msgs.position.append(j1)
#         joint_states_msgs.position.append(j2)
#         joint_states_msgs.position.append(j3)
#         joint_states_msgs.position.append(j4)
#         joint_states_msgs.position.append(j5)
#         joint_states_msgs.position.append(j6)
#         joint_states_msgs.position.append(gripper)
#         self.right_pub_joint.publish(joint_states_msgs)
#         # self.rate.sleep()
#         print("send joint control piper command")
    
    
     
# # test code
# # if __name__ == '__main__':
#     # piper = PIPER() 
#     # rospy.init_node('control_piper_node', anonymous=True)
#     # piper.control_piper(0.0,0.0,0.0,0.0,0.0,0.0,0.05)
#     # piper.init_pose()
#     # 保持节点运行并监听外部程序的调用
#     # rospy.spin()

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import time

class PIPER(Node):
    def __init__(self):
        super().__init__('piper_node')

        self.pub_joint = self.create_publisher(JointState, '/joint_states', 10)
        self.left_pub_joint = self.create_publisher(JointState, '/left_joint_states', 10)
        self.right_pub_joint = self.create_publisher(JointState, '/right_joint_states', 10)

        self.declare_parameter('target_joint_state', [0.0]*7)
        param = self.get_parameter('target_joint_state').get_parameter_value()
        # 兼容不同ROS2版本参数类型
        if hasattr(param, 'double_array_value'):
            self.target_joint_state = list(param.double_array_value)
        elif hasattr(param, 'float64_array_value'):
            self.target_joint_state = list(param.float64_array_value)
        else:
            self.target_joint_state = [0.0]*7

        self.create_subscription(JointState, 'joint_states_single', self.joint_states_callback, 10)

        self.current_joint_positions = [0.0]*7
        self.joint_positions_received = False

    def joint_states_callback(self, msg):
        if len(msg.position) >= 7:
            self.current_joint_positions = list(msg.position[:7])
            self.joint_positions_received = True
            self.get_logger().debug(f"Received current joint positions: {self.current_joint_positions}")

    def init_pose(self):
        target_joint_state = self.target_joint_state
        if self.joint_positions_received:
            current_positions = self.current_joint_positions
            self.get_logger().info(f"Using actual current joint positions: {current_positions}")

            duration = 0.5
            rate_hz = 50
            steps = int(duration * rate_hz)
            increments = [(target - current) / steps for current, target in zip(current_positions, target_joint_state)]

            rate = self.create_rate(rate_hz)
            for step in range(steps + 1):
                interpolated_positions = [current + increment * step for current, increment in zip(current_positions, increments)]
                joint_states_msgs = JointState()
                joint_states_msgs.header = Header()
                joint_states_msgs.header.stamp = self.get_clock().now().to_msg()
                joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
                joint_states_msgs.position = interpolated_positions
                self.pub_joint.publish(joint_states_msgs)
                rate.sleep()
        else:
            # 如果没收到关节位置，直接发布目标位置多次
            rate = self.create_rate(50)
            for _ in range(25):  # 0.5秒 * 50Hz = 25次
                joint_states_msgs = JointState()
                joint_states_msgs.header = Header()
                joint_states_msgs.header.stamp = self.get_clock().now().to_msg()
                joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
                joint_states_msgs.position = target_joint_state
                self.pub_joint.publish(joint_states_msgs)
                rate.sleep()

def main(args=None):
    rclpy.init(args=args)
    node = PIPER()
    node.init_pose()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
