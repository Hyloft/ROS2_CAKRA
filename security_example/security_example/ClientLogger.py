from action_security_interfaces.action import Logger

from cakra.NodeClient import NodeClient

class ClientLogger(NodeClient):
    def __init__(self,name,this) -> None:
        super().__init__(Logger, name, this,True)
        # this client should not be contunious so pass False as last parameter.
        self.camera_image_last = ''

    def check_dependencies(self, args=None):
        state = args
        if self.camera_image_last == state['camera_image']:
            return False
        return True

    def final(self, result):
        # change state while using result.
        print(result.is_log_completed)
        if result.is_log_completed != True:
            Exception('error occured while logging')

    def set_goal_msg(self, goal_msg, args=None):
        # set the goal message while using state. (args variable is the state)
        state=args
        goal_msg.camera_image=state['camera_image']
        return goal_msg


def main():
    print('Hi from security_example.')


if __name__ == '__main__':
    main()
