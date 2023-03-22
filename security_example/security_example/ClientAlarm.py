from action_security_interfaces.action import Alarm

from cakra.NodeClient import NodeClient

class ClientAlarm(NodeClient):
    def __init__(self,name,this) -> None:
        super().__init__(Alarm, name, this,False)
        # this client should not be contunious so pass False as last parameter.

    def final(self, result):
        # change state while using result.
        self.main_node.state['is_alarm_open'] = result.is_alarm_open

    def set_goal_msg(self, goal_msg, args=None):
        # set the goal message while using state. (args variable is the state)
        state=args
        goal_msg.is_secure=state['is_secure']
        return goal_msg


def main():
    print('Hi from security_example.')


if __name__ == '__main__':
    main()
