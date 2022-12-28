import rclpy
from rclpy.node import Node

class MainNode(Node):
    def __init__(self,name,active_nodes =None,loop_nodes=None):
        super().__init__(name)
        self.active_nodes = active_nodes
        self.loop_nodes = loop_nodes
        self._clients = []
        
    def prepare(self):
        self._clients = [_c.layout for _c in self._clients]
        self.active_nodes = [c['name'] for c in self._clients] if self.active_nodes == None else self.active_nodes
        self.loop_nodes = [*self.active_nodes] if self.loop_nodes == None else self.loop_nodes
        
    def activate_node(self,name):
        """
        send node name and then it will be added into next loop and set it active
        """


        client_names = [c['name'] for c in self._clients]
        if name in client_names:
            self.active_nodes.append(name)
            self.active_nodes = [*set(self.active_nodes)]
            self.loop_nodes.append(name)
            self.loop_nodes = [*set(self.loop_nodes)]
        else:
            raise Exception(f'client not found "{name}" to active')

    def deactivate_node(self,name):

        """
        send node name and it will be deleted into next loop and set as deactive
        """

        client_names = [c['name'] for c in self._clients]
        if name in client_names and name in self.active_nodes:
            self.active_nodes = [n for n in self.active_nodes if n != name]
            self.loop_nodes = [n for n in self.active_nodes if n != name]
        else:
            raise Exception(f'client not found "{name}" to deactive')

    def before_loop(self):

        """
        you can nest this function.
        it will run before the loop
        """

        return False

    def after_loop(self):
        """
        you can nest this function.
        it will run after the loop
        """
        
        return

    def loop(self):
        
        r = self.before_loop()

        if r == True:
            return

        nodes_to_loop = [node for node in self._clients if node['name'] in self.loop_nodes]
        
        for node_client in nodes_to_loop:
            node_client['client'].send_goal(self.state)

        self.after_loop()