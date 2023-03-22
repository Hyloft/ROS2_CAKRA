import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

import cv2
import numpy as np
import mediapipe as mp
import io
import base64

from action_security_interfaces.action import Camera

def readb64(base64_string):
    jpg_original = base64.b64decode(base64_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img

class SecurityActionServer(Node):

    def __init__(self):
        super().__init__('security_action_server')
        self._action_server = ActionServer(
                self,
                Camera,
                'security',
                self.execute_callback)

        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils

    def execute_callback(self,goal_handle):
        self.get_logger().info('Executing goal...')
        goal_handle.succeed()
        imstr = goal_handle.request.camera_image
        is_secure = True
        img = readb64(imstr)
        with self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            if results.detections:
                is_secure = False

        result = Camera.Result()
        result.is_secure = is_secure
        return result

def main(args=None):
    rclpy.init(args=args)

    fibonacci_action_server = SecurityActionServer()

    rclpy.spin(fibonacci_action_server)

if __name__ == '__main__':
    main()