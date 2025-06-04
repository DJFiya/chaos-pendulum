# Chaos Pendulum Simulator

A Python simulation of a double pendulum system that demonstrates chaotic behavior. Small changes in initial conditions can lead to dramatically different patterns over time.

## Description

This project simulates a double pendulum system using numerical integration of the equations of motion. The simulation creates an animated visualization showing:
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

## Customization

You can modify these parameters in `main.py` to create unique patterns:

1. Initial conditions (angles and velocities):
```python
init_state = [theta1, omega1, theta2, omega2]
# Default: [np.pi/2, 0, np.pi/2 + 0.01, 0]
```
- `theta1`: Initial angle of first pendulum (radians)
- `omega1`: Initial angular velocity of first pendulum
- `theta2`: Initial angle of second pendulum (radians)
- `omega2`: Initial angular velocity of second pendulum

2. Physical parameters:
```python
L1, L2 = 1.0, 1.0  # Lengths of pendulum arms
m1, m2 = 1.0, 1.0  # Masses of pendulum bobs
g = 9.81           # Gravitational acceleration
```

3. Simulation parameters:
```python
t = np.linspace(0, 20, 1000)  # Time array (duration, number of points)
```

## Interesting Patterns

Try these modifications to see different behaviors:

1. Slightly different initial angles:
```python
init_state = [np.pi/2, 0, np.pi/2 + 0.001, 0]  # Very similar initial conditions
```

2. Different arm lengths:
```python
L1, L2 = 1.0, 2.0  # Unequal pendulum lengths
```

3. Different masses:
```python
m1, m2 = 1.0, 0.5  # Lighter second mass
```

The chaotic nature of the system means that even tiny changes in these values can produce vastly different patterns over time.