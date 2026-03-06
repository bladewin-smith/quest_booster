import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from tf_transformations import euler_from_quaternion
import numpy as np
import os
from arm_ik import Arm_IK

def create_transformation_matrix(x, y, z, roll, pitch, yaw):
    import math
    transformation_matrix = np.eye(4)
    A = np.cos(yaw)
    B = np.sin(yaw)
    C = np.cos(pitch)
    D = np.sin(pitch)
    E = np.cos(roll)
    F = np.sin(roll)
    DE = D * E
    DF = D * F
    transformation_matrix[0, 0] = A * C
    transformation_matrix[0, 1] = A * DF - B * E
    transformation_matrix[0, 2] = B * F + A * DE
    transformation_matrix[0, 3] = x
    transformation_matrix[1, 0] = B * C
    transformation_matrix[1, 1] = A * E + B * DF
    transformation_matrix[1, 2] = B * DE - A * F
    transformation_matrix[1, 3] = y
    transformation_matrix[2, 0] = -D
    transformation_matrix[2, 1] = C * F
    transformation_matrix[2, 2] = C * E
    transformation_matrix[2, 3] = z
    return transformation_matrix

class IKNode(Node):
    def __init__(self):
        super().__init__('ik_node')

        # URDF路径，请根据实际路径修改
        urdf_path = os.path.expanduser('~/ros2_ws/src/piper_description/urdf/piper_description.urdf')

        self.ik_solver = Arm_IK(urdf_path)

        self.create_subscription(PoseStamped, '/target_pose', self.pose_callback, 10)

    def pose_callback(self, msg: PoseStamped):
        x = msg.pose.position.x
        y = msg.pose.position.y
        z = msg.pose.position.z
        roll, pitch, yaw = euler_from_quaternion([
            msg.pose.orientation.x,
            msg.pose.orientation.y,
            msg.pose.orientation.z,
            msg.pose.orientation.w
        ])

        target_pose = create_transformation_matrix(x, y, z, roll, pitch, yaw)

        q_sol, success = self.ik_solver.solve_ik(target_pose)

        if success:
            self.get_logger().info(f'IK解: {q_sol}')
            # 这里你可以发布关节角度消息，控制机械臂
        else:
            self.get_logger().warn('IK求解失败')

def main(args=None):
    rclpy.init(args=args)
    node = IKNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
