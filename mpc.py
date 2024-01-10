import numpy as np
import do_mpc
import matplotlib.pyplot as plt

#experiment  conditions

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)    
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

class MPC:
    def __init__(self):
        #experiment  conditions
        self.INITIAL_Y_ERROR = -20
        self.INITIAL_ΤΗΕΤΑ_ERROR=-1.5
        self.VELOCITY = 30
        self.TIME_STEP = 0.1
        self.HORIZON = 10

        self.model_type = 'continuous'
        self.model = do_mpc.model.Model(self.model_type)
        #Certain parameters
        self.L=20
        self.y_desired=0
        self.theta_desired=0
        self.w_n=1
        #x: state
        y = self.model.set_variable(var_type='_x', var_name='y', shape=(1,1))
        theta = self.model.set_variable(var_type='_x', var_name='theta', shape=(1,1))
        # Two states for the desired (set) position:
        delta = self.model.set_variable(var_type='_u', var_name='delta')
        '''
        #uncertain parameters
        velocity=model.set_variable('_p', 'velocity')
        y_desired
        theta_desired
        '''
        #differential equations
        self.model.set_rhs('y',self.VELOCITY*np.sin(theta))
        self.model.set_rhs('theta',self.VELOCITY*np.tan(delta)/self.L)

        self.model.setup()

        self.mpc=do_mpc.controller.MPC(self.model)

        #Configuring the MPC controller
        setup_mpc = {
            'n_horizon': self.HORIZON,
            't_step': self.TIME_STEP,
            'n_robust': 1,
            'store_full_solution': True,
        }
        self.mpc.set_param(**setup_mpc)

        mterm = self.w_n*((y-self.y_desired)**2 + (theta-self.theta_desired)**2)
        lterm = (y-self.y_desired)**2 + (theta-self.theta_desired)**2

        self.mpc.set_objective(mterm=mterm, lterm=lterm)

        self.mpc.set_rterm(
            delta=100
        )

        # Lower bounds:
        self.mpc.bounds['lower','_x', 'y'] = -15
        self.mpc.bounds['lower','_x', 'theta'] = -np.pi/3
        self.mpc.bounds['lower','_u', 'delta'] = -np.pi/6

        # Upper bounds on states
        self.mpc.bounds['upper','_x', 'y'] = 15
        self.mpc.bounds['upper','_x', 'theta'] = np.pi/3
        self.mpc.bounds['upper','_u', 'delta'] = np.pi/6

        #Scaling
        self.mpc.scaling['_x', 'y'] = 1
        self.mpc.scaling['_x', 'theta'] = 1

        '''
        #setting uncertain parameters(used if we want to follow trajectory for theta_desired_p, y_desired_p)
        mpc.set_uncertainty_values(velocity=np.array[2., 5., 10., 30.])
        '''

        #Configuring the Simulator
        self.mpc.setup()

        self.simulator = do_mpc.simulator.Simulator(self.model)
        self.simulator.set_param(t_step = self.TIME_STEP)

        self.simulator.setup()

        self.simulator_time = 0
    def mpc_correction(self,crosstrack_error,heading_error,velocity):
        self.VELOCITY=velocity
        x0=np.array([crosstrack_error, heading_error])
        self.simulator.x0 = x0
        self.mpc.x0 = x0
        self.mpc.set_initial_guess()
        return self.mpc.make_step(x0)[0][0]

if __name__ == "__main__":
    controller = MPC()
    result = []
    x=[]
    #creating control loop
    for i in np.arange(-1.4,1.4,0.01):
        x.append(i)
        result.append(controller.mpc_correction(controller.INITIAL_Y_ERROR,i,30))
    print(result)
    plt.plot(x,normalize(result,-1,1))
    plt.show()



""" 
import matplotlib.pyplot as plt
import matplotlib as mpl
# Customizing Matplotlib:
mpl.rcParams['font.size'] = 18
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['axes.grid'] = True

mpc_graphics = do_mpc.graphics.Graphics(mpc.data)
sim_graphics = do_mpc.graphics.Graphics(simulator.data)


# We just want to create the plot and not show it right now. This "inline magic" supresses the output.
fig, ax = plt.subplots(3, sharex=True, figsize=(16,9))
fig.align_ylabels()


for g in [sim_graphics, mpc_graphics]:
    g.add_line(var_type='_x', var_name='theta', axis=ax[0])
    g.add_line(var_type='_x', var_name='y', axis=ax[1])
    g.add_line(var_type='_u', var_name='delta', axis=ax[2])

ax[0].set_ylabel('θ(rad)')
ax[1].set_ylabel('y(cm)')
ax[2].set_ylabel('Correction(rad)')
ax[2].set_xlabel('time(s)')


mpc_graphics.pred_lines
mpc_graphics.pred_lines['_x', 'y']
for line_i in mpc_graphics.pred_lines['_x', 'y']: line_i.set_color('#1f77b4') 
for line_i in mpc_graphics.pred_lines['_x', 'theta']: line_i.set_color('#2ca02c') 
for line_i in mpc_graphics.pred_lines['_u', 'delta']: line_i.set_color('#ff7f0e')


u0 = np.array([[0]])
for i in range(50):
    simulator.make_step(u0)
    u0 = mpc.make_step(x0)


mpc_graphics.plot_predictions(t_ind=0)
mpc_graphics.reset_axes()

plt.suptitle('Experiment conditions: Velocity ' + str(VELOCITY) + 'cm/s, Initial Y error: '+ str(INITIAL_Y_ERROR) + 'cm, Initial Θ error: ' + str(INITIAL_ΤΗΕΤΑ_ERROR) + 'rad')
plt.figtext(0.7, 0.01,'Time step '+ str(TIME_STEP) + 's, Horizon: ' + str(HORIZON) + 'steps')
plt.show()
 """