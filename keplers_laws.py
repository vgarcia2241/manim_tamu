from manim import *
import numpy as np
import scipy.optimize as scipy

'''
me when mean anomaly..? eccentric anomaly.? me when its non trivial :(
'''

'''
x(t) = a*cos(t)-c
y(t) = b*sin(t)
c = a*e
e= -(b/a)**2 + 1

t = T/2*PI * (E-e*sin(E)) //needs to be numerically solved
M = 2*PI*t/T
=> num_solve: 0 = E - e*sin(E) - M, for M
'''

# to be fiddled with
mu = 1
a=6
b=3.25
T=1 # [sec] perhaps, set to one for sake of simplicity
e = -((b/a)**2) + 1
c = a*e

def planet_pos(t): #returns position for given time
    M= 2*PI*t / T
    func1 = lambda x: x - e*np.sin(x) - M
    E = (scipy.fsolve(func1, x0=3))[0]
    x = a*np.cos(E)
    y = b*np.sin(E)
    return np.array([x,y,0]) 

class s1(Scene):
    def construct(self):
        screen = Rectangle(color=WHITE, height=8, width=15)
        init_time1 = 0.1 #used as starting "times" of planets to have them at diff points in orbit
        init_time2 = 0.6
        time_tracker = ValueTracker(0) #takes ~T*1.0027 to actually loop...for some reason, numerical approx adding up?
        foci_pos = 2.3 #distance of foci
        orbit_size = [2*a,2*b]
        
        
        sun1 = Dot([foci_pos,0,0], color=YELLOW, radius=0.4).set_z_index(1).set_opacity(0.5)
        sun2 = Dot([foci_pos,0,0], color=YELLOW, radius=0.3).set_z_index(1)
        sun = VGroup(sun1, sun2)
        focus = Cross(stroke_color=GRAY, stroke_width=7, scale_factor=0.2).move_to([-foci_pos,0,0])
        orbit = Ellipse(orbit_size[0],orbit_size[1], color=WHITE).set_stroke(width=7)
        mask = Cutout(screen, orbit.copy().set_fill(color=BLACK, opacity=1), color=BLACK, fill_opacity=1)
        planet1 = always_redraw(
            lambda: Dot(planet_pos(time_tracker.get_value() + init_time1), color=BLUE_D, radius=0.2).set_z_index(1)
        )
        planet2 = always_redraw(
            lambda: Dot(planet_pos(time_tracker.get_value() + init_time2), color=RED, radius=0.2).set_z_index(1)
        )
        
        init_rad1 = planet1.get_center() - sun.get_center()
        init_rad1 = np.sqrt(init_rad1[0]**2 + init_rad1[1]**2)
        init_rad2 = planet2.get_center() - sun.get_center()
        init_rad2 = np.sqrt(init_rad2[0]**2 + init_rad2[1]**2)
        
        line1 = always_redraw(
            lambda: Line(sun.get_center(), planet_pos(init_time1-0.00001), color=WHITE)
        )
        line2 = always_redraw(
            lambda: Line(sun.get_center(), planet_pos(time_tracker.get_value()+init_time1), color=WHITE)
        )
        line3 = always_redraw(
            lambda: Line(sun.get_center(), planet_pos(init_time2-0.00001), color=WHITE)
        )
        line4 = always_redraw(
            lambda: Line(sun.get_center(), planet_pos(time_tracker.get_value()+init_time2), color=WHITE)
        )
        
        start_ang1 = angle_of_vector(planet_pos(init_time1) - sun.get_center())
        start_ang2 = angle_of_vector(planet_pos(init_time2) - sun.get_center())
        area1 = always_redraw(
            lambda: Sector(radius=14,
                           angle = Angle(line1, line2, other_angle=False).get_value()*(1+0.014), #small correction to angle which breaks down ~1.8*PI
                           color = BLUE_B
                           ).set_z_index(-1).rotate(angle = start_ang1, about_point=sun.get_center()).move_arc_center_to(sun.get_center()).set_opacity(0.5)
        )
        area2 = always_redraw(
            lambda: Sector(radius=14,
                           angle = Angle(line3, line4, other_angle=False).get_value() + 0.007, #small correction to angle
                           color = RED_B
                           ).set_z_index(-1).rotate(angle = start_ang2, about_point=sun.get_center()).move_arc_center_to(sun.get_center()).set_opacity(0.5)
        )
        
        ###################################################################################################
        g1 = VGroup(area1, area2, line1, line2, line3, line4)
        
        self.add(mask, sun, orbit, planet1, planet2, focus)
        self.wait()
        self.play(FadeIn(g1))
        self.wait()
        self.play(
            time_tracker.animate.increment_value(0.1),
            run_time=3, rate_func = rate_functions.linear
        )
        self.wait()
        