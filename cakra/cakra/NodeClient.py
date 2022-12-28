from rclpy.action import ActionClient

class NodeClient():
    def __init__(self,Action,name,this,contunious=False) -> None:
        self._action_client = ActionClient(this,Action,name)
        self.Action = Action
        self.action_name = name
        self.main_node = this
        self.layout = {
            'name':self.action_name,
            'client':self
        }
        self.contunious = contunious

    def send_goal(self,args=None):
        if self.check_dependencies(args) == False:
            return

        goal_msg = self.set_goal_msg(self.Action.Goal(),args)

        self.main_node.loop_nodes = [node for node in self.main_node.loop_nodes if node != self.action_name]

        if self.action_name not in self.main_node.active_nodes:
            return

        self._action_client.wait_for_server()
        
        self.send_goal_future = self._action_client.send_goal_async(goal_msg)
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self,future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.main_node.get_logger().info('Rejected goal')
            return
        self.main_node.get_logger().info(f'Goal accepted for {self.action_name}')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)
        
    def get_result_callback(self,future):
        if self.action_name not in self.main_node.active_nodes:
            return
        
        result = future.result().result
        self.main_node.get_logger().info(f'res of {self.action_name}: {result}')

        self.final(result)
                
        if (self.action_name in self.main_node.active_nodes) and self.contunious:
            self.main_node.loop_nodes.append(self.action_name)
                
        self.main_node.loop()
    
    # you can nest this function
    def set_goal_msg(self,goal_msg,args=None):
        """
        you can nest this function.
        you must set the goal_msg in this function.
        args is the state of the main node
        """
        return goal_msg
    
    # you can nest this function
    def final(self,result):
        """
        you can nest this function.
        you can access the properties of results while using result.<property_name>
        """
        return

    # you can nest this function
    def check_dependencies(self,args=None):
        """
        you can nest this function.
        args is the state of the main node
        
        return 'True' if dependencies are okay
        return 'False' if dependencies are not okay

        if you return 'False' client wont send request at this loop. but it will stay as active
        and it also will be on the next loop  
        """
        return True