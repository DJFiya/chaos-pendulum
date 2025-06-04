import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
g = 9.81 
L1, L2 = 1.0, 1.0 
m1, m2 = 1.0, 1.0 

init_state = [np.pi / 2, 0, np.pi / 2 + 0.01, 0]
t = np.linspace(0, 20, 1000)

def derivs(state, t):
    theta1, omega1, theta2, omega2 = state
    delta = theta2 - theta1

    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta)**2
    den2 = (L2 / L1) * den1

    dtheta1 = omega1
    dtheta2 = omega2

    domega1 = ((m2 * L1 * omega1**2 * np.sin(delta) * np.cos(delta) +
             m2 * g * np.sin(theta2) * np.cos(delta) +
             m2 * L2 * omega2**2 * np.sin(delta) -
             (m1 + m2) * g * np.sin(theta1)) / den1)

    domega2 = ((-m2 * L2 * omega2**2 * np.sin(delta) * np.cos(delta) +
             (m1 + m2) * g * np.sin(theta1) * np.cos(delta) -
             (m1 + m2) * L1 * omega1**2 * np.sin(delta) -
             (m1 + m2) * g * np.sin(theta2)) / den2)

    return [dtheta1, domega1, dtheta2, domega2]

sol = odeint(derivs, init_state, t)

x1 = L1 * np.sin(sol[:, 0])
y1 = -L1 * np.cos(sol[:, 0])
x2 = x1 + L2 * np.sin(sol[:, 2])
y2 = y1 - L2 * np.cos(sol[:, 2])

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_title("Double Pendulum (Chaotic System)")

line, = ax.plot([], [], 'o-', lw=2)
trace, = ax.plot([], [], '-', lw=1, color='blue', alpha=0.5)
trace_x, trace_y = [], []

def update(i):
    line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])

    trace_x.append(x2[i])
    trace_y.append(y2[i])
    trace.set_data(trace_x, trace_y)

    return line, trace

ani = FuncAnimation(fig, update, frames=len(t), interval=20, blit=True)

plt.show()