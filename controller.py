import numpy as np


class Controller:
    def __init__(self, SPEED):
        if SPEED:
            self.control = np.load('mpc_fast.txt.npy')
        else:
            self.control = np.load('mpc_slow.txt.npy')
    def correction(self,pixel_error,degree_error):
        dist_index =round((pixel_error+320)/17.7)
        angle_index = round((degree_error+15)/3)
        print(dist_index)
        print(angle_index)
        return self.control[dist_index][angle_index]



if __name__ == "__main__":
    c = Controller(True)
    for i in range(-300,300,1):
        print(c.correction(i,0))
