# from robot import robot as r
from robot import bot1 as b1
from robot import bot2 as b2
from robot import bot3 as b3
from robot import bot4 as b4

def RobotGateway(botType):
    robot = None
    if botType == 1:
        robot = b1.Bot1()
    elif botType == 2:
        robot = b2.Bot2()
    elif botType == 3:
        robot = b3.Bot3()
    # if botType == 4:
    #     robot = b4.Bot4()
    else:
        raise ValueError(f"Invalid botType: {botType}")
    return robot