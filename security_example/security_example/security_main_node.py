import rclpy
import cv2
import base64
from security_example.ClientSecurity import ClientSecurity
from security_example.ClientAlarm import ClientAlarm
from security_example.ClientLogger import ClientLogger
from cakra.MainNode import MainNode

def decode64(img):
    return base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()

class SecurityMainNode(MainNode):
    def __init__(self):
        super().__init__('main_node')
        self.client_alarm = ClientAlarm('alarm',self)
        self.client_secutity = ClientSecurity('security',self)
        self.client_logger = ClientLogger('logger',self)
        self.node_clients = [self.client_alarm,self.client_logger,self.client_secutity]
        self.state = {
            'camera_image':'',
            'is_secure':True
        }
        self.prepare()
        self.cam = cv2.VideoCapture()
        self.cam.open('http://192.168.0.30:8000/')

    def before_loop(self):
        if not self.cam.isOpened:
            print('cam port not working')
            rclpy.shutdown()
            return True
        result, image = self.cam.read()
        if not result:
            rclpy.shutdown()
            return True
        
        self.state['camera_image'] = decode64(image)
        
def main(args=None):
    rclpy.init(args=args)
    
    main_node = SecurityMainNode()

    main_node.loop()

    rclpy.spin(main_node)

if __name__ == '__main__':
    main()