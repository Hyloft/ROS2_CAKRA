# ROS2 CAKRA
<p align='center'>
<img src='./cakra/image.png' width='550px'/>
</p>

## What is cakra?
Cakra is basically the ros2 architecture written for a self-driving car named 'çaka'. <br>Cakra have 2 modules called ***MainNode*** and ***NodeClient***.<br>
Main purpose of this architecture is using multiple server nodes asynchronously without any trouble.
<br>

### Setup:
- [setting up cakra for your ros2 workspace](#setup-cakra)


### Basic explaination of cakra modules:
- [main node](#mainnode)
- [node client](#nodeclient)


### Basic usage of cakra modules:
- [main node example](#usage-example)
- [node client example](#example-usage)

<br><br>

## Setup Cakra:

First of all, go to your *ros2 workspace* file.
```bash
cd ~/ros2_ws
```
Than, unzip this file into *src* file in your *ros2 workspace* dir.
```bash
unzip <install_dir>/ROS2_CAKRA.zip -d ~/ros2_ws/src
cp -a ~/ros2_ws/src/ROS2_CAKRA-master/. ~/ros2_ws/src/
rm -r ~/ros2_ws/src/ROS2_CAKRA-master
```
After that, build it with colcon.
```bash
colcon build
```
Lastly, complete the setup.
```bash
. install/setup.bash
```

## MainNode:
***MainNode*** is **ros2 node** that can handle multiple requests while using ***NodeClient***'s. 

First of all, you can import the *MainNode* like this:

```python
from cakra.MainNode import MainNode
```

#### Properties:
`state` you have to define a dictinary to store all the data you will send to servers. You will be able to decide which part of the state will go as response to which server.
<br>
`loop_nodes` is the node names that will run into next loop.
<br>
`active_nodes` is the node names that can run and change something.
<br>
`node_clients` is the dictinary list. The dictinaries are layouts of the clients.
<br>
you have to define it in your new class as well.
<br><br>
`before_loop(self)`
- that will run before the loop function begun.
- you can nest this function and edit it like you want.
- this function must return `boolean` to decide loop will run or not. you can return `False` to prevent the loop run.
<br>

`after_loop(self)`
- that will run after loop function ends.
- you can nest this function and edit it like you want.

`activate_node(self,name)`
- you can run this code with the name of the client you want to activate.
- the client will be **active** and will be in the `loop_nodes` again. So it will run into next loop.

`deactivate_node(self,name)`
- you can run this code with the name of the client you want to deactivate.
- the client won't be **active** and will be deleted in the `loop_nodes` again. So it won't run into next loop.

`prepare(self)`
- you **must** run this code into end of the `def __init__` function.
- it will prepare the `loop_nodes`,`_clients` and `active_nodes` for you.

#### Usage Example:

```python
class ExampleMainNode(MainNode):
    def __init__(self):
        super().__init__('name_of_node')
        # you must create clients like this
        self.example_client = ExampleNodeClient('name_of_client',self)
        
        # you must also create array of clients you created 
        self.node_clients = [self.example_client]
        
        # define the state
        self.state = {
            'example_number':10
        }

        # finally call the prepare function
        self.prepare()

    def before_loop(self):
        # shutdown and break the loop if number lower than 4
        if self.state['example_number'] < 4:
            rclpy.shutdown()
            return True
    
    def after_loop(self):
        if self.state['example_number'] < 4:
            print('node will stop at next loop')
```

## NodeClient:

First of all, you can import the ***NodeClient*** like this:
```python
from cakra.NodeClient import NodeClient
```

#### Properties:
`_action_client` is the ***rclpy.action.ActionClient***.
<br>
`Action` is the action you passed.
<br>
`action_name` is the name of the action and also client.
<br>
`main_node` is the your main node.
<br>
`layout` is the dictinary. Dictinary's 'name' property is the ***action_name*** and 'client' is the ***self***.
<br>

`contunious`
- you have to decide that client should run into every loop or not.
- it must be `boolean` value.
<br><br>

`set_goal_msg(self,goal_msg_args=None)`
- you can nest this function.
- you must set the ***goal_msg*** and return it in this function.
- args is the state of the main node

`final(self,result)`
- you can nest this function.
- you can access the properties of results while using `result.<property_name>`

`check_dependencies(self,args=None)`
- you can nest this function.
- args is the state of the main node
- return `True` if dependencies are okay
- return `False` if dependencies are not okay
- if you return `False` client wont send request at this loop. but it will stay as active
- and it also will be on the next loop  

#### Example usage:

```python
from example_interface.action import ExampleAction

from cakra.NodeClient import NodeClient

class ExampleClient(NodeClient):
    def __init__(self,name,this) -> None:
        super().__init__(ExampleAction, name, this,False)
        # this client should not be contunious so pass False as last parameter.

    def final(self, result):
        # change state while using result.
        self.main_node.state['example_number'] = result.new_number

    def set_goal_msg(self, goal_msg, args=None):
        # set the goal message while using state. (args variable is the current state)
        goal_msg.number=args['example_number']
        return goal_msg
```
