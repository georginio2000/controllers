import numpy as np
import matplotlib.pyplot as plt
#PARAMETERS

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)    
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

192 168 1 118
class Stanley:
    def __init__(self):
        self.INITIAL_Y_ERROR = 10
        self.INITIAL_ΤΗΕΤΑ_ERROR= 0
        self.VELOCITY = 30
        self.K = 2 #control gain 
        self.max_steer = np.pi/6
    def stanley_correction( self,crosstrack_error,heading_error,velocity): #crosstrack in pixels
        desired_steering_angle = -heading_error - np.arctan(self.K*crosstrack_error/velocity)
        limited_steering_angle = np.clip(desired_steering_angle, -self.max_steer, self.max_steer)
        return limited_steering_angle


if __name__ == "__main__":
    s=Stanley() 
    result=[]
    x=[]
    for i in np.arange(-20,20,0.01):
        x.append(i)
        result.append(s.stanley_correction(i, s.INITIAL_ΤΗΕΤΑ_ERROR, s.VELOCITY))
    print(result)
    #plt.plot(x,normalize(result,-1,1))
    plt.plot(x,result)
    plt.show()
