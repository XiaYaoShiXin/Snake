import numpy as np;
import time;
import os;
import matplotlib.pyplot as plt
from pynput.keyboard import Key, Listener

class Node:

    def __init__(self,init_direction,init_x,init_y):
        self.direction = init_direction
        self.parent = None
        self.child = None;
        self.x = init_x;
        self.y = init_y;

    def Append(self,child_node):
        self.child = child_node;
        child_node.parent = self;
        child_node.ReverseMove();

    def Move(self):
        if(self.direction%2==0):
            self.y += (self.direction-3)
        else:
            self.x += (2-self.direction)
    
    def ReverseMove(self):
        if(self.direction%2==0):
            self.y -= (self.direction-3)
        else:
            self.x -= (2-self.direction)


#  1向下 2向左 3向上  4向右
#  坐标系：x轴向下，y轴向右
#
#
class Snake:

    def __init__(self,init_direction,init_x,init_y):
        self.head = Node(init_direction,init_x,init_y);
        self.tail = self.head;
        self.parent = None;
        self.x = init_x;
        self.y = init_y;
        self.direction = init_direction;
        self.alive = True;
    
    def Append(self):#应该在每回合的Tick之后执行，否则末尾节点不能正常更新
        cursor = self.head;
        while(cursor.child is not None):
            cursor = cursor.child;
        self.tail = Node(cursor.direction,cursor.x,cursor.y)
        cursor.Append(self.tail);

    def Tick(self,map):
        #头部
        self.head.Move()
        self.x = self.head.x
        self.y = self.head.y
        self.alive = self.IsAlive(map)
    
        #身体        
        cursor = self.tail;
        while(cursor.parent is not None):
            cursor.Move();
            cursor.direction = cursor.parent.direction;
            cursor = cursor.parent;

    def TurnLeft(self):
        self.direction -= 1;
        if(self.direction==0):
            self.direction = 4;
        self.head.direction = self.direction;
    
    def TurnRight(self):
        self.direction += 1;
        if(self.direction==5):
            self.direction = 1;
        self.head.direction = self.direction;

    def Control(self,input):
        if(input==0):
            pass;
        elif(input>0):
            self.TurnRight()
        elif(input<0):
            self.TurnLeft()

    def IsAlive(self,scene):
        if(self.direction==1):
            if(self.x>=scene.shape[0]):#碰到边界
                return False;
            if(scene[self.x,self.y]<0):#碰到障碍或自己的身体
                return False;
                
        if(self.direction==3):
            if(self.x<0):
                return False;
            if(scene[self.x,self.y]<0):
                return False;
                
        if(self.direction==2):
            if(self.y<0):
                return False;
            if(scene[self.x,self.y]<0):
                return False;
                
        if(self.direction==4):
            if(self.y>=scene.shape[1]):
                return False;
            if(scene[self.x,self.y]<0):
                return False;

        return True;

def GenerateFruit(scene):
    width = scene.shape[0]
    height = scene.shape[1]
    while(True):
        x = np.random.randint(0,width)
        y = np.random.randint(0,height)
        if(scene[x,y]==0):
            scene[x,y] = 1;
            print("[Fruit]"+str(x)+","+str(y))
            break;
        else:
            continue;

def UpdateScene(scene,agent):
    global score;
    scene = np.clip(scene,0,10)

    cursor = agent.head;
    while(cursor is not None):
        if(scene[cursor.x,cursor.y]>0):
            agent.Append()
            score+=1;
            GenerateFruit(scene)
        scene[cursor.x,cursor.y] = -1;
        cursor = cursor.child;
    return scene;


input = 0;
score = 0;

def Main():
    scene = np.zeros((13,13),dtype=np.int8)
    agent = Snake(4,6,6)
    GenerateFruit(scene)
    
    i = 0;
    plt.ion()

    global input
    def input_handler(key):
        global input;
        if key == Key.right:
            input = 1
        if key == Key.left:
            input = -1

    print("GAME START")
    while(True):
        #处理输入
        listener = Listener(on_press=input_handler)
        listener.start()

        #处理逻辑
        if(i%5==0):
            agent.Control(input)
            input = 0
            agent.Tick(scene);
            print("[player]"+str(agent.x)+","+str(agent.y))
            if(not agent.alive):
                print("GAME OVER")
                break;
            scene = UpdateScene(scene,agent)
            #可视化
            plt.clf()
            plt.imshow(scene)
            
        #
        plt.pause(0.1)
        plt.ioff()
        i+=1
        





Main()