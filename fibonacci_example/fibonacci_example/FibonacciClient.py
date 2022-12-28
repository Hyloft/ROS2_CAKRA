from fibonacci_example_interface.action import Fibonacci

from cakra.NodeClient import NodeClient

class FibonacciClient(NodeClient):
    def __init__(self,name,this) -> None:
        super().__init__(Fibonacci, name, this,True)
        self.last_number = None

    def check_dependencies(self,args=None):
        if self.last_number == args['last_number']:
            return False
        return True

    def final(self, result):
        self.main_node.activate_node('decrease')

    def set_goal_msg(self, goal_msg, args=None):
        goal_msg.order=args['last_number']
        self.last_number = goal_msg.order
        return goal_msg