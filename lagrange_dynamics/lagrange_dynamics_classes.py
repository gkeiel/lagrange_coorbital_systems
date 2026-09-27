import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
from lagrange_dynamics_config import G


# =====================================================
#  ThreeBody
# =====================================================
class ThreeBody:
    def __init__(self, m_star, m_1, m_2, r0, v0):
        self.m = np.array([m_star, m_1, m_2], dtype=float)
        self.r  = r0.copy()
        self.v  = v0.copy()
        
    def acceleration(self, r):

        a = np.zeros((3, 3))

        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                dr = r[j] -r[i]
                d  = np.linalg.norm(dr)
                a[i] += G*self.m[j]*dr/d**3
        return a
        
    def step(self, dt):
        
        # acceleration
        a      = self.acceleration(self.r)
        
        # numerical integration
        self.v = self.v +a*dt
        self.r = self.r +self.v*dt
        return self.r
       

# =====================================================
#  Animator
# =====================================================
class Animator:
    def __init__(self, r_data, m_star, m_1, m_2, theta, skip, r0, v0, dt, N, lim=2.0e11):
        self.r_data = np.array(r_data)[::skip]
        self.m_star = m_star
        self.m_1    = m_1
        self.m_2    = m_2
        self.theta  = theta
        self.skip   = skip
        self.r0     = r0.copy()
        self.v0     = v0.copy()
        self.dt     = dt
        self.N      = N
        self.lim    = lim
        
        self.fig      = plt.figure()
        self.ax       = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-lim, lim])
        self.ax.set_ylim([-lim, lim])
        self.ax.set_zlim([-lim, lim])
        
        self.ax.set_title("Three-body gravitational system")
        self.ax.set_xlabel("x [m]")
        self.ax.set_ylabel("y [m]")
        self.ax.set_zlabel("z [m]")

        # bodies
        self.star,   = self.ax.plot([], [], [], 'o', markersize=21, color='orange')
        self.body_1, = self.ax.plot([], [], [], 'o', markersize=7, color='blue')
        self.body_2, = self.ax.plot([], [], [], 'o', markersize=7, color='green')

        # trajectories
        self.line_star, = self.ax.plot([], [], [], '-', color='orange', alpha=0.5)
        self.line_1,    = self.ax.plot([], [], [], '-', color='blue', alpha=0.5)
        self.line_2,    = self.ax.plot([], [], [], '-', color='green', alpha=0.5)

        # sliders
        ax_slider_1   = self.fig.add_axes([0.20, 0.04, 0.60, 0.025])
        ax_slider_2   = self.fig.add_axes([0.20, 0.01, 0.60, 0.025])
        ax_slider_th  = self.fig.add_axes([0.20, 0.07, 0.60, 0.025])
        self.slider_1 = Slider(ax_slider_1, 'Body 1', 0.0001, 0.001, valinit=m_1/m_star, valstep=0.00001)
        self.slider_2 = Slider(ax_slider_2, 'Body 2', 0.0001, 0.001, valinit=m_2/m_star, valstep=0.00001)
        self.slider_th = Slider(ax_slider_th, 'Angle', 0, 180, valinit=np.degrees(theta), valstep=1)
        self.slider_1.on_changed(self.change_mass_1)
        self.slider_2.on_changed(self.change_mass_2)
        self.slider_th.on_changed(lambda value: None)
        
        # restart button
        ax_button   = self.fig.add_axes([0.82, 0.015, 0.12, 0.05])
        self.button = Button(ax_button, 'Reset')
        self.button.on_clicked(self.restart)
    
    def change_mass_1(self, value):
        self.m_1 = value*self.m_star
        self.body_1.set_markersize(7 +10000*value)

    def change_mass_2(self, value):
        self.m_2 = value*self.m_star    
        self.body_2.set_markersize(7 +10000*value)
        
    def update(self, i):
    
        r   = self.r_data[:i+1]
        
        # current positions
        rs = r[-1, 0]
        r1 = r[-1, 1]
        r2 = r[-1, 2]
        
        # centralize star
        self.ax.set_xlim([rs[0] -self.lim, rs[0] +self.lim])
        self.ax.set_ylim([rs[1] -self.lim, rs[1] +self.lim])
        self.ax.set_zlim([rs[2] -self.lim, rs[2] +self.lim])
        
        # star
        self.star.set_data([rs[0]], [rs[1]])
        self.star.set_3d_properties([rs[2]])

        # body 1
        self.body_1.set_data([r1[0]], [r1[1]])
        self.body_1.set_3d_properties([r1[2]])

        # body 2
        self.body_2.set_data([r2[0]], [r2[1]])
        self.body_2.set_3d_properties([r2[2]])

        # trajectories
        self.line_star.set_data(r[:, 0, 0], r[:, 0, 1])
        self.line_star.set_3d_properties(r[:, 0, 2])
        self.line_1.set_data(r[:, 1, 0], r[:, 1, 1])
        self.line_1.set_3d_properties(r[:, 1, 2])
        self.line_2.set_data(r[:, 2, 0], r[:, 2, 1])
        self.line_2.set_3d_properties(r[:, 2, 2])

        return (self.star, self.body_1, self.body_2, self.line_star, self.line_1, self.line_2)
    
    def update_trajectory(self):
        system = ThreeBody(self.m_star, self.m_1, self.m_2, self.r0, self.v0)
        r_data = []

        for k in range(self.N):
            r = system.step(self.dt)
            r_data.append(r.copy())
        self.r_data = np.array(r_data)[::self.skip]
        
    def restart(self, event):
        theta = np.radians(self.slider_th.val)
        R     = np.linalg.norm(self.r0[1])
        omega = np.linalg.norm(self.v0[1])/R
        
        self.r0[2] = [R*np.cos(theta), R*np.sin(theta), 0.0]
        self.v0[2] = [-omega*R*np.sin(theta), omega*R*np.cos(theta), 0.0]
        
        self.ani.event_source.stop()
        self.update_trajectory()
        self.ani = FuncAnimation(self.fig, self.update, frames=len(self.r_data), interval=20, blit=False)
    
    def animate(self, interval=20):       
        self.ani = FuncAnimation(self.fig, self.update, frames=len(self.r_data), interval=interval, repeat=False)
        self.ani.save("data/animation.gif", writer="pillow", fps=20)
        plt.show()