# Chaos Pendulum Simulator

A Python simulation of a double pendulum system that demonstrates chaotic behavior. Small changes in initial conditions can lead to dramatically different patterns over time.

## Description

This project simulates a double pendulum system using numerical integration of the equations of motion. The simulation features an interactive GUI that allows you to:
- Adjust initial angles, arm lengths, and masses using sliders
- Visualize the initial configuration with a polar angle dial
- Start the simulation with a button click
- Watch an animated visualization showing:
  - The movement of both pendulum arms
  - A trace of the path taken by the second pendulum bob
  - Real-time animation of the system's evolution

## Requirements

- Python 3.x
- NumPy
- SciPy
- Matplotlib

## Usage

Run the simulation using:
```bash
python main.py
```
An interactive window will appear. Use the sliders to set initial conditions and parameters, then click **Start Simulation** to view the animation.

## Customization

You can modify these parameters using the GUI sliders in `main.py`:

1. **Initial conditions (angles in degrees):**
   - `θ₁`: Initial angle of first pendulum
   - `θ₂`: Initial angle of second pendulum

2. **Physical parameters:**
   - `L₁`, `L₂`: Lengths of pendulum arms (meters)
   - `m₁`, `m₂`: Masses of pendulum bobs (kg)
   - `g`: Gravitational acceleration (fixed at 9.81 m/s²)

3. **Simulation parameters:**
   - The simulation runs for 20 seconds with 1000 time steps (modifiable in code if needed).

## Interesting Patterns

Try these slider settings to see different behaviors:

1. **Slightly different initial angles:**
   - Set `θ₁` and `θ₂` to values that differ by only 1 degree.

2. **Different arm lengths:**
   - Set `L₁` and `L₂` to unequal values (e.g., 1.0 and 2.0).

3. **Different masses:**
   - Set `m₁` and `m₂` to different values (e.g., 1.0 and 0.5).

The chaotic nature of the system means that even tiny changes in these values can produce vastly different patterns over time.

---