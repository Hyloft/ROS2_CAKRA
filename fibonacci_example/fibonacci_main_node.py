import rclpy

from fibonacci_example.DecreaseClient import DecreaseClient
from fibonacci_example.FibonacciClient import FibonacciClient
from cakra.MainNode import MainNode

class FibonacciMainNode(MainNode):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self.decrease_client = DecreaseClient('decrease',self)
        self.fibonacci_client = FibonacciClient('fibonacci',self)
        self.all_nodes = [self.decrease_client,self.fibonacci_client]
        self.state = {
            'last_number':10
        }
        self.prepare()

    def before_loop(self):
        if self.state['last_number'] < 4:
            rclpy.shutdown()
            return True
        
def main(args=None):
    rclpy.init(args=args)
    
    main_node = FibonacciMainNode()

    main_node.loop()

    rclpy.spin(main_node)

if __name__ == '__main__':
    main()

