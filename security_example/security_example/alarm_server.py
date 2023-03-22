import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

import cv2
import numpy as np
from datetime import datetime
import base64

from action_security_interfaces.action import Alarm

class AlarmActionServer(Node):

    def __init__(self):
        super().__init__('alarm_action_server')
        self._action_server = ActionServer(
                self,
                Alarm,
                'alarm',
                self.execute_callback)


    def execute_callback(self,goal_handle):
        self.get_logger().info('Executing goal...')
        goal_handle.succeed()
        is_secure = goal_handle.request.is_secure
        if is_secure:
            result = Alarm.Result()
            result.is_alarm_open = False
            return result
        
        #convert str to img
        self.get_logger().info('ALARM ALARM')       
        

        result = Alarm.Result()
        result.is_alarm_open = True
        return result

def main(args=None):
    rclpy.init(args=args)

    alarm_server = AlarmActionServer()

    rclpy.spin(alarm_server)

if __name__ == '__main__':
    main()