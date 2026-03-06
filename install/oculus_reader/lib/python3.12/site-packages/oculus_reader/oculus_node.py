import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import tf2_ros

class OculusReaderNode(Node):
    def __init__(self):
        super().__init__('oculus_reader')
        self.get_logger().info('Oculus Reader Node started')
        self.pose_sub = self.create_subscription(
            PoseStamped,
            '/oculus/pose',
            self.pose_callback,
            10)
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

    def pose_callback(self, msg):
        self.get_logger().info(f'Received pose: {msg.pose.position.x}, {msg.pose.position.y}, {msg.pose.position.z}')

def main(args=None):
    rclpy.init(args=args)
    node = OculusReaderNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
