import os
from lagrange_dynamics_classes import ThreeBody, Animator
from lagrange_dynamics_config import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# instance objects and give arguments from lagrange_dynamics_config.py
system = ThreeBody(m_star, m_1, m_2, r0, v0)

# initialize data
r_data = []

for k in range(N):
    
    # orbit evolution
    r = system.step(dt)
       
    # store data    
    r_data.append(r.copy())
    
# 3D animation
animation = Animator(r_data, m_star, m_1, m_2, theta, skip, r0, v0, dt, N)
animation.animate()