from fibonacci_example_interface.action import Decrease

from cakra.NodeClient import NodeClient

class DecreaseClient(NodeClient):
    def __init__(self,name,this) -> None:
        super().__init__(Decrease, name, this,False)

    def final(self, result):
        self.main_node.state['last_number'] = result.new_number

    def set_goal_msg(self, goal_msg, args=None):
        goal_msg.number=args['last_number']
        return goal_msg