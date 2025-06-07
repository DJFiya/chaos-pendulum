import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
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
fig_cfg.patch.set_facecolor('#1e1e1e')
plt.subplots_adjust(left=0.25, bottom=0.55)
ax_cfg.axis('off')
ax_cfg.set_title("\u2734 Double Pendulum Config", fontsize=16, fontweight='bold', color='white')

angle_ax = plt.axes([0.05, 0.55, 0.15, 0.15], polar=True, facecolor="#2e2e2e")
angle_ax.set_theta_offset(-np.pi / 2)
angle_ax.set_theta_direction(-1)
angle_ax.set_yticklabels([])
angle_ax.set_xticks(np.linspace(0, 2 * np.pi, 12, endpoint=False))
angle_ax.tick_params(colors='white')
angle_ax.set_title("Initial Angles", fontsize=10, color='white')
angle_line1, = angle_ax.plot([0, init_params['theta1']], [0, 1], lw=2, label="\u03b81", color='cyan')
angle_line2, = angle_ax.plot([0, init_params['theta2']], [0, 1], lw=2, label="\u03b82", color='magenta')
angle_ax.legend(loc='lower right', fontsize=8, frameon=False, labelcolor='white')

slider_face = '#444'
text_color = 'white'
slider_axes = {
    'theta1': plt.axes([0.25, 0.45, 0.65, 0.025], facecolor=slider_face),
    'theta2': plt.axes([0.25, 0.40, 0.65, 0.025], facecolor=slider_face),
    'L1':     plt.axes([0.25, 0.35, 0.65, 0.025], facecolor=slider_face),
    'L2':     plt.axes([0.25, 0.30, 0.65, 0.025], facecolor=slider_face),
    'm1':     plt.axes([0.25, 0.25, 0.65, 0.025], facecolor=slider_face),
    'm2':     plt.axes([0.25, 0.20, 0.65, 0.025], facecolor=slider_face)
}

slider_labels = {
    'theta1': 'Initial \u03b81 (degrees)',
    'theta2': 'Initial \u03b82 (degrees)',
    'L1': 'Length L1 (m)',
    'L2': 'Length L2 (m)',
    'm1': 'Mass m1 (kg)',
    'm2': 'Mass m2 (kg)'
}

sliders = {}
for key, ax in slider_axes.items():
    if 'theta' in key:
        sliders[key] = Slider(ax, slider_labels[key], 0, 360,
                              valinit=np.round(init_params[key] / DEG2RAD),
                              valstep=1, color='#03dac6')
        sliders[key].valtext.set_text(f"{int(sliders[key].val)}\u00b0")
        sliders[key].valtext.set_color(text_color)
        sliders[key].label.set_color(text_color)
    else:
        sliders[key] = Slider(ax, slider_labels[key], 0.1, 5,
                              valinit=np.round(init_params[key] * 10) / 10,
                              valstep=0.1, color='#bb86fc')
        sliders[key].valtext.set_color(text_color)
        sliders[key].label.set_color(text_color)

# Number of pendulums
angle_slider_ax = plt.axes([0.25, 0.15, 0.65, 0.025], facecolor=slider_face)
num_pendulum_slider = Slider(angle_slider_ax, 'Number of Pendulums', 1, 20, valinit=10, valstep=1, color='#ffb300')
num_pendulum_slider.valtext.set_color(text_color)
num_pendulum_slider.label.set_color(text_color)

# Offset type radio buttons
offset_type_ax = plt.axes([0.80, 0.58, 0.15, 0.18], facecolor='#2e2e2e')
offset_type_radio = RadioButtons(offset_type_ax,
                                 ('theta1', 'theta2', 'L1', 'L2', 'm1', 'm2'))
for label in offset_type_radio.labels:
    label.set_color('white')
    label.set_fontsize(8)
offset_type_ax.set_title("Offset Type", color='white', fontsize=9)

# Offset amount slider
offset_value_ax = plt.axes([0.25, 0.10, 0.65, 0.025], facecolor=slider_face)
offset_slider = Slider(offset_value_ax, 'Offset Amount', -10, 10, valinit=1, valstep=0.1, color='#ff4081')
offset_slider.label.set_color(text_color)
offset_slider.valtext.set_color(text_color)

def update_angle(val):
    deg1 = sliders['theta1'].val
    deg2 = sliders['theta2'].val
    rad1 = deg1 * DEG2RAD
    rad2 = deg2 * DEG2RAD
    angle_line1.set_data([0, rad1], [0, 1])
    angle_line2.set_data([0, rad2], [0, 1])
    sliders['theta1'].valtext.set_text(f"{int(deg1)}\u00b0")
    sliders['theta2'].valtext.set_text(f"{int(deg2)}\u00b0")
    fig_cfg.canvas.draw_idle()

sliders['theta1'].on_changed(update_angle)
sliders['theta2'].on_changed(update_angle)

button_ax = plt.axes([0.4, 0.02, 0.2, 0.05])
start_button = Button(button_ax, '\u25b6 Start Simulation', color='#03a9f4', hovercolor='#0288d1')
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

    t = np.linspace(0, 20, 1000)
    n_pendulums = int(num_pendulum_slider.val)

    offset_param = offset_type_radio.value_selected
    offset_amount = offset_slider.val
    offsets = np.linspace(0, offset_amount, n_pendulums)
    x_offsets = [0.0] * n_pendulums # Debug option if you want to distinguish pendulums by their x-offsets

    fig_sim, ax_sim = plt.subplots(figsize=(6, 6))
    fig_sim.patch.set_facecolor('#121212')
    ax_sim.set_aspect('equal')
    ax_sim.set_xlim(-2 * (L1 + L2), 2 * (L1 + L2))
    ax_sim.set_ylim(-2 * (L1 + L2), 2 * (L1 + L2))
    ax_sim.set_title("\U0001f300 Multiple Double Pendulums", fontsize=14, fontweight='bold', color='white')
    ax_sim.tick_params(colors='white')
    for spine in ax_sim.spines.values():
        spine.set_color('white')

    pendulum_lines = []
    traces = [[] for _ in range(n_pendulums)]
    trace_lines = []

    for _ in range(n_pendulums):
        line1, = ax_sim.plot([], [], 'o-', lw=2, alpha=0.7)
        line2, = ax_sim.plot([], [], 'o-', lw=2, alpha=0.7)
        trace_line, = ax_sim.plot([], [], '-', lw=1, alpha=0.4)
        pendulum_lines.append((line1, line2))
        trace_lines.append(trace_line)

    solutions = []
    for offset in offsets:
        mod_theta1 = theta1
        mod_theta2 = theta2
        mod_L1 = L1
        mod_L2 = L2
        mod_m1 = m1
        mod_m2 = m2

        if offset_param == 'theta1':
            mod_theta1 += offset * DEG2RAD
        elif offset_param == 'theta2':
            mod_theta2 += offset * DEG2RAD
        elif offset_param == 'L1':
            mod_L1 += offset
        elif offset_param == 'L2':
            mod_L2 += offset
        elif offset_param == 'm1':
            mod_m1 += offset
        elif offset_param == 'm2':
            mod_m2 += offset

        init_state = [mod_theta1, 0, mod_theta2, 0]

        def derivs(state, t, L1=mod_L1, L2=mod_L2, m1=mod_m1, m2=mod_m2):
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
        solutions.append((sol, mod_L1, mod_L2))

    def update(i):
        for idx, (sol, L1_used, L2_used) in enumerate(solutions):
            offset = x_offsets[idx]
            x1 = offset + L1_used * np.sin(sol[i, 0])
            y1 = -L1_used * np.cos(sol[i, 0])
            x2 = x1 + L2_used * np.sin(sol[i, 2])
            y2 = y1 - L2_used * np.cos(sol[i, 2])

            line1, line2 = pendulum_lines[idx]
            line1.set_data([offset, x1], [0, y1])
            line2.set_data([x1, x2], [y1, y2])

            traces[idx].append((x2, y2))
            tx, ty = zip(*traces[idx])
            trace_lines[idx].set_data(tx, ty)
        return [line for pair in pendulum_lines for line in pair] + trace_lines

    ani_ref = FuncAnimation(fig_sim, update, frames=len(t), interval=20, blit=True)
    plt.show()

start_button.on_clicked(simulate)
plt.show()
