import numpy as np
import matplotlib.pyplot as plt


figure, axis = plt.subplots(2, 2)

#time parameters
dt = 0.1
time_limit = 1000
num_steps = int(time_limit / dt)

###Simulate Vertical position
#Constants
g = 9.81
h = 2000000
C_d = 0.92
A = 0.071
m = 8321.8

colTime = 0

#Initialize arrays
time = np.linspace(0, time_limit, num_steps)
height = np.zeros(num_steps)
velocity = np.zeros(num_steps)

#Set intial conditions
height[0] = h
velocity[0] = 0

#Simulate motion
for i in range(1, num_steps):
    rho = np.abs(np.clip(((height[i-1]-44.3308)/-42.2665),0,0.140))**4.256
    F_d =  0.5 * C_d * rho * A * velocity[i-1]**2
    net_force = m * g - F_d
    a = net_force / m

    height[i] = height[i-1] - (velocity[i-1]*dt)
    if height[i] <=0:
        height[i] = 0
        if height[i-1] > 0:
            colTime = i*dt
    velocity[i] = velocity[i-1] + (a * dt)

#Plotting Variables
axis[0,0].plot(time, height / 1e3)  # Convert height to km for plotting
axis[0,0].set_title('Vertical Position Over Time')
axis[0,0].set_xlabel('Time / s')
axis[0,0].set_ylabel('Height / km')
axis[0,0].axvline(x=colTime, color='r', linestyle='--', label=f'{format(colTime, ".2f")}s')
axis[0,0].grid()
axis[0,0].legend()


###simulate horizontal position
#constants
s = 0
C_d = 0.69
A = 2.9
m = 8321.8

#Initialize arrays
height2 = np.zeros(num_steps)
velocity2 = np.zeros(num_steps)

#Set intial conditions
height2[0] = 0
velocity2[0] = 7800

#Simulate motion
for i in range(1, num_steps):
    rho = np.abs(np.clip(((height[i-1]-44.3308)/-42.2665),0,0.140))**4.256
    F_d =  0.5 * C_d * rho * A * velocity2[i-1]**2
    net_force = -F_d
    a = net_force / m

    height2[i] = height2[i-1] + (velocity2[i-1]*dt)
    velocity2[i] = np.clip(velocity2[i-1] + (a * dt),0,7800)

#plotting of values
axis[0,1].plot(time, height2 / 1e3)  # Convert height to km for plotting
axis[0,1].set_title('Horizontal Position Over Time')
axis[0,1].set_xlabel('Time / s')
axis[0,1].set_ylabel('Distance/ km')
axis[0,1].grid()
axis[0,1].axvline(x=colTime, color='r', linestyle='--', label=f'{format(colTime, ".2f")}s')
axis[0,1].legend()


###Plotting speed over time
tempVel = np.add(velocity, velocity2) / 1e3
tempVel.sort()
axis[1,0].plot(time,np.add(velocity,velocity2)/1e3)
axis[1,0].set_xlim(0, time[-1]*1.1)
axis[1,0].set_ylim(0, tempVel[-1]*1.1)
axis[1,0].set_title('Speed Over Time')#
axis[1,0].set_xlabel('Time / s')
axis[1,0].set_ylabel(r'Speed / km s$^{-1}$')
axis[1,0].grid()
axis[1,0].axvline(x=colTime, color='r', linestyle='--', label=f'{format(colTime, ".2f")}s')
axis[1,0].legend()

###Plotting motion path
tempX = height2
tempX.sort()

axis[1,1].plot(height2 / 1e3, height / 1e3)
axis[1,1].set_ylim(0,tempX[-1]/3/1e3)
axis[1,1].set_xlim(0,tempX[-1]/1e3)
axis[1,1].set_title('Path of Motion')
axis[1,1].set_xlabel('Distance / km')
axis[1,1].set_ylabel('Height / km')
axis[1,1].grid()

###ADjusting and displaying plots
for i in range(1,num_steps):
    if height[i] == 0:
        if height[i-1] > 0:
            print("Distance drifted", height2[i] / 1e3)
print("Final Velocity", tempVel[-1])

plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.3,hspace=0.35)

plt.show()
