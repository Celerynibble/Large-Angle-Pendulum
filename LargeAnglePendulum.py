import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

# Parameters
g = 9.8
dt = 10**(-5)
t = np.arange(0, 30, dt)  # Time array
n = len(t)  # Total number of steps

class LargeAngPend:
    def __init__(self, mass, leng):
        self.mass = mass
        self.leng = leng
    
    def run(self, initAng, initVel):
        
        # Preallocate arrays
        x = np.zeros(n)  # Angular displacement
        v = np.zeros(n)  # Angular velocity
        a = np.zeros(n)  # Angular acceleration
        
        # Initial conditions
        x[0] = initAng
        v[0] = initVel
        a[0] = -g*np.sin(x[0])
        
        # Time-stepping loop
        for i in range(n-1):
            v[i+1] = v[i]+a[i]*dt
            x[i+1] = x[i]+v[i]*dt
            a[i+1] = -(g/self.leng)*np.sin(x[i+1])
        
        self.position = x
        self.velocities = v
        self.acc = a
        
        # Zero-crossing detection
        self.T = []  # Reset T for each new simulation
        for i in range(1, n):
            if (x[i] > 0 and x[i-1] < 0):
                self.T.append(t[i])
        
    def getTimePeriod(self):
        if len(self.T)<2:
            print("hasn't finished a cycle yet")
            return None  # Not enough data for period calculation
        
        # Calculate the time period using the zero-crossing times
        TP = (self.T[len(self.T)-1] - self.T[0])/(len(self.T) - 1)
        return TP

initangles = np.linspace(0, np.pi/2, 20)

def calculate_period(init_ang):
    Pend = LargeAngPend(1, 1)
    Pend.run(init_ang, 0)
    return Pend.getTimePeriod()

# Run the simulations in parallel and get time periods
with ThreadPoolExecutor() as executor:
    T = list(executor.map(calculate_period, initangles))
    
plt.plot(initangles, T, marker='o')
plt.title('Time Period of Pendulum vs Initial Angle')
plt.xlabel('Initial Angle (radians)')
plt.ylabel('Time Period (seconds)')
plt.grid(True)
plt.show()