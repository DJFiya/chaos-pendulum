import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation

# Constants
g = 9.81
DEG2RAD = np.pi / 180

# Initial parameters
init_params = {
    'theta1': 90 * DEG2RAD,
    'theta2': 91 * DEG2RAD,
    'L1': 1.0,
    'L2': 1.0,
    'm1': 1.0,
    'm2': 1.0
}

fig_cfg, ax_cfg = plt.subplots(figsize=(7, 6))
fig_cfg.patch.set_facecolor('#f5f5f5')
plt.subplots_adjust(left=0.25, bottom=0.45)
ax_cfg.axis('off')
ax_cfg.set_title("Double Pendulum Configuration", fontsize=14, fontweight='bold')

# Angle Dial
angle_ax = plt.axes([0.05, 0.55, 0.15, 0.15], polar=True, facecolor="#eaeaea")
angle_ax.set_theta_offset(-np.pi / 2)  
angle_ax.set_yticklabels([])
angle_ax.set_xticks(np.linspace(0, 2 * np.pi, 12, endpoint=False))
angle_ax.set_title("Initial Angles", fontsize=10)
angle_line1, = angle_ax.plot([0, init_params['theta1']], [0, 1], lw=2, label="θ1", color='darkblue')
angle_line2, = angle_ax.plot([0, init_params['theta2']], [0, 1], lw=2, label="θ2", color='darkorange')
angle_ax.legend(loc='lower right', fontsize=8, frameon=False)

slider_axes = {
    'theta1': plt.axes([0.25, 0.35, 0.65, 0.025], facecolor='#e0e0e0'),
    'theta2': plt.axes([0.25, 0.30, 0.65, 0.025], facecolor='#e0e0e0'),
    'L1':     plt.axes([0.25, 0.25, 0.65, 0.025], facecolor='#e0e0e0'),
    'L2':     plt.axes([0.25, 0.20, 0.65, 0.025], facecolor='#e0e0e0'),
    'm1':     plt.axes([0.25, 0.15, 0.65, 0.025], facecolor='#e0e0e0'),
    'm2':     plt.axes([0.25, 0.10, 0.65, 0.025], facecolor='#e0e0e0')
}

slider_labels = {
    'theta1': 'Initial θ₁ (degrees)',
    'theta2': 'Initial θ₂ (degrees)',
    'L1': 'Length L₁ (m)',
    'L2': 'Length L₂ (m)',
    'm1': 'Mass m₁ (kg)',
    'm2': 'Mass m₂ (kg)'
}

sliders = {}
for key, ax in slider_axes.items():
    if 'theta' in key:
        sliders[key] = Slider(ax, slider_labels[key], 0, 360,
                              valinit=np.round(init_params[key] / DEG2RAD),
                              valstep=1)
        sliders[key].valtext.set_text(f"{int(sliders[key].val)}°")
    else:
        sliders[key] = Slider(ax, slider_labels[key], 0.1, 5,
                              valinit=np.round(init_params[key] * 10) / 10,
                              valstep=0.1)

def update_angle(val):
    deg1 = sliders['theta1'].val
    deg2 = sliders['theta2'].val
    rad1 = deg1 * DEG2RAD
    rad2 = deg2 * DEG2RAD

    angle_line1.set_data([0, rad1], [0, 1])
    angle_line2.set_data([0, rad2], [0, 1])
    sliders['theta1'].valtext.set_text(f"{int(deg1)}°")
    sliders['theta2'].valtext.set_text(f"{int(deg2)}°")
    fig_cfg.canvas.draw_idle()

sliders['theta1'].on_changed(update_angle)
sliders['theta2'].on_changed(update_angle)

# Start Simulation Button
button_ax = plt.axes([0.4, 0.02, 0.2, 0.05])
start_button = Button(button_ax, '▶ Start Simulation', color='#1976D2', hovercolor='#1565C0')
start_button.label.set_fontsize(10)
start_button.label.set_color('white')

ani_ref = None  

def simulate(event):
    global ani_ref

    theta1 = sliders['theta1'].val * DEG2RAD
    theta2 = sliders['theta2'].val * DEG2RAD
    L1 = sliders['L1'].val
    L2 = sliders['L2'].val
    m1 = sliders['m1'].val
    m2 = sliders['m2'].val

    init_state = [theta1, 0, theta2, 0]
    t = np.linspace(0, 20, 1000)

    def derivs(state, t):
        th1, w1, th2, w2 = state
        delta = th2 - th1
        den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta)**2
        den2 = (L2 / L1) * den1

        dth1 = w1
        dth2 = w2

        dw1 = ((m2 * L1 * w1**2 * np.sin(delta) * np.cos(delta) +
                m2 * g * np.sin(th2) * np.cos(delta) +
                m2 * L2 * w2**2 * np.sin(delta) -
                (m1 + m2) * g * np.sin(th1)) / den1)

        dw2 = ((-m2 * L2 * w2**2 * np.sin(delta) * np.cos(delta) +
                (m1 + m2) * g * np.sin(th1) * np.cos(delta) -
                (m1 + m2) * L1 * w1**2 * np.sin(delta) -
                (m1 + m2) * g * np.sin(th2)) / den2)

        return [dth1, dw1, dth2, dw2]

    sol = odeint(derivs, init_state, t)

    x1 = L1 * np.sin(sol[:, 0])
    y1 = -L1 * np.cos(sol[:, 0])
    x2 = x1 + L2 * np.sin(sol[:, 2])
    y2 = y1 - L2 * np.cos(sol[:, 2])

    fig_sim, ax_sim = plt.subplots(figsize=(6, 6))
    fig_sim.patch.set_facecolor('#fafafa')
    ax_sim.set_aspect('equal')
    ax_sim.set_xlim(-2 * (L1 + L2), 2 * (L1 + L2))
    ax_sim.set_ylim(-2 * (L1 + L2), 2 * (L1 + L2))
    ax_sim.set_title("🌀 Double Pendulum Simulation", fontsize=14, fontweight='bold')

    line, = ax_sim.plot([], [], 'o-', lw=3, color='black')
    trace, = ax_sim.plot([], [], '-', lw=1.5, color='dodgerblue', alpha=0.4)
    trace_x, trace_y = [], []

    def update(i):
        line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
        trace_x.append(x2[i])
        trace_y.append(y2[i])
        trace.set_data(trace_x, trace_y)
        return line, trace

    ani_ref = FuncAnimation(fig_sim, update, frames=len(t), interval=20, blit=True)
    plt.show()

start_button.on_clicked(simulate)
plt.show()
