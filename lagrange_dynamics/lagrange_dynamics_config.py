import numpy as np


# simulation parameters
dt   = 7200
N    = 87600
skip = 100

# gravitational constant
G = 6.67430e-11

#  masses
m_star = 1.989e30
m_1    = 5.972e24
m_2    = 5.972e24

# distance from star
R = 1.496e11

# angular velocity
omega = np.sqrt(G*m_star/R**3)

# degrees (L4 = 60, L5 = -60)
theta = np.radians(60)

# positions
r_star = np.array([0.0, 0.0, 0.0])
r_1    = np.array([R, 0.0, 0.0])
r_2    = np.array([R*np.cos(theta), R*np.sin(theta), 0.0])

# orbital velocities
v_1 = np.array([0.0, omega*R, 0.0])
v_2 = np.array([-omega*R*np.sin(theta), omega*R*np.cos(theta), 0.0])
r0  = np.array([r_star, r_1, r_2])
v0  = np.array([[0.0, 0.0, 0.0], v_1, v_2])