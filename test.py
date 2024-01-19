import numpy as np
import matplotlib.pyplot as plt
from mpc import MPC
from stanley import Stanley
from stanley import normalize



TESTING_CROSSTRACK = False
s = Stanley()
m = MPC()

pretrained = np.zeros((37,11))
result_s=[]
result_m=[]
x=[]

if(TESTING_CROSSTRACK==True):
    for i in np.arange(-1.4,1.4,0.1):
        x.append(i)
        #results.append(s.stanley_correction(i,s.INITIAL_ΤΗΕΤΑ_ERROR , s.VELOCITY))
        #resultm.append(m.mpc_correction(i,m.INITIAL_ΤΗΕΤΑ_ERROR,m.VELOCITY))
        result_s.append(s.stanley_correction(-20, i, s.VELOCITY))
        result_m.append(m.mpc_correction(-20,i))
else:
    for i in np.arange(-20,20,0.5):
        x.append(i)
        result_s.append(s.stanley_correction(i,0 , s.VELOCITY))
        result_m.append(m.mpc_correction(i,0))
print(result_m)
print(result_s)

plt.plot(x,normalize(result_s,-1,1),'b')
plt.plot(x,normalize(result_m,-1,1),'r')
plt.title("blue=stanley red=mpc")
plt.show()



'''
for i in range(37):
    for j in range(11):
        pretrained[i][j]=57*round(m.mpc_correction(-9+i*0.5,-0.25+j*0.05),1)

np.save('mpc_slow.txt', pretrained)
'''