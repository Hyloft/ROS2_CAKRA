import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from fibonacci_example_interface.action import Decrease

class DecreaseActionServer(Node):

    def __init__(self):
        super().__init__('decrease_action_server')
        self._action_server = ActionServer(
                self,
                Decrease,
                'decrease',
                self.execute_callback)
    
    def execute_callback(self,goal_handle):
        self.get_logger().info('Goal is handling..')
        goal_handle.succeed()

        res = Decrease.Result()
        res.new_number = goal_handle.request.number - 1

        return res
def main(args=None):
    rclpy.init(args=args)

    action_server = DecreaseActionServer()

    rclpy.spin(action_server)

if __name__ == '__main__':
    main()
