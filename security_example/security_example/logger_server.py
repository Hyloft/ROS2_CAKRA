import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

import cv2
import numpy as np
from datetime import datetime
import base64

from action_security_interfaces.action import Logger

def readb64(base64_string):
    jpg_original = base64.b64decode(base64_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img

class LoggerActionServer(Node):

    def __init__(self):
        super().__init__('logger_action_server')
        self._action_server = ActionServer(
                self,
                Logger,
                'logger',
                self.execute_callback)


    def execute_callback(self,goal_handle):
        self.get_logger().info('Executing goal...')
        goal_handle.succeed()
        imstr = goal_handle.request.camera_image
        #convert str to img
        img = readb64(imstr)

        current_date = datetime.now()
        time = '-'.join([f'{x}' for x in [current_date.year,current_date.month,current_date.day,current_date.hour,current_date.minute,current_date.second,current_date.microsecond]])
        cv2.imwrite(f'./security_images/{time}.jpg',img)        
        

        result = Logger.Result()
        result.is_log_completed = True
        return result

def main(args=None):
    rclpy.init(args=args)

    logger_server = LoggerActionServer()

    rclpy.spin(logger_server)

if __name__ == '__main__':
    main()