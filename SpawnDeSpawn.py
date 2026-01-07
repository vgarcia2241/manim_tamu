from manim import *
import numpy as np

#breaking downs scenes
'''
19x20 1080p
'''

#animation time

'''
Initial show of ramp and ball, v_0, forces, and coords
'''
current_frame = 0

class SpawnDeSpawn(Scene):
    def construct(self):

        rate=0.1

        Rect1 = Rectangle(width=2,height=2).move_to([-1,0,0])

        #emfpath1 = ParametricFunction(
        #    lambda t: np.array([2*( np.abs(np.cos(t))*np.cos(t) - np.abs(np.sin(t))*np.sin(t) ) - 2,
        #        -2*( np.abs(np.cos(t))*np.cos(t) + np.abs(np.sin(t))*np.sin(t) ) + 2,
        #        0
        #    ]),
        #    t_range=[0,3*PI/2,0.001],
        #    use_smoothing=False,
        #    color=BLUE
        #)

        #self.play(Create(emfpath1))

        # Create a list to hold the dots
        emfdots1 = VGroup()
        new_emfdot = Dot(point=Rect1.point_from_proportion(0.75), color=RED)
        emfdots1.add(new_emfdot)

        # Variable to control the creation of new dots
        dot_creation_timer = ValueTracker(0)
        time_text = always_redraw(
            lambda: MathTex(f"t={dot_creation_timer.get_value():.2f}")
        )
        time_text.move_to([0,0,0])
        self.add(time_text)

        def UpdateTime(mob,dt):
            dot_creation_timer.set_value(dot_creation_timer.get_value()+dt)

        emfdots1.add_updater(UpdateTime)

        # Add an updater to create new dots periodically
        def add_new_emfdots1(mob, dt):
            ndots = len(mob)
            if mob[ndots-1].get_center()[0]<-0.2: 
                new_dot = Dot(point=Rect1.point_from_proportion(0.75), color=RED)
                emfdots1.add(new_dot)
        emfdots1.add_updater(add_new_emfdots1)

        emfdots2 = VGroup()





        # Animate the movement of all dots along the path
        # This updater will apply to all dots in the 'dots' VGroup
        def move_emfdots_along_path1(mob, dt):
            for dot in mob:
                
                
                if Rect1.proportion_from_point(dot.get_center())-0.01<0.0:
                    dot.move_to(Rect1.point_from_proportion(0.0))
                    #emfdots2.add(dot)
                    emfdots1.remove(dot)
                else:
                    print(Rect1.proportion_from_point(dot.get_center()))
                    dot.move_to(Rect1.point_from_proportion(Rect1.proportion_from_point(dot.get_center())-0.01))

        #def move_emfdots_along_path2(mob,dt):
        #    for dot in mob:
        #        dot.move_to(emfpath2.point_from_proportion(emfpath2.proportion_from_point(dot.get_center())+0.01))

        emfdots1.add_updater(move_emfdots_along_path1)
        #emfdots2.add_updater(move_emfdots_along_path2)
        self.add(emfdots1)


        self.wait(20) # Wait for a duration to observe the continuous creation and movement



        

class ContinuousDotsOnPath(Scene):
    def construct(self):
        # Define the path
        path = ParametricFunction(
            lambda t: np.array([
                np.sin(t),
                np.cos(t),
                0
            ]),
            t_range=[0, 2 * PI],
            color=BLUE
        )
        self.play(Create(path))
        #self.add(path)

        # Create a list to hold the dots
        dots = VGroup()
        new_dot = Dot(point=path.get_start(), color=RED)
        dots.add(new_dot)
        

        # Variable to control the creation of new dots
        dot_creation_timer = ValueTracker(0)
        time_text = always_redraw(
            lambda: MathTex(f"t={dot_creation_timer.get_value():.2f}")
        )
        time_text.move_to([2,0,0])
        self.add(time_text)

        def UpdateTime(mob,dt):
            dot_creation_timer.set_value(dot_creation_timer.get_value()+dt)

        dots.add_updater(UpdateTime)


        # Add an updater to create new dots periodically
        def add_new_dot(mob, dt):
            ndots = len(mob)
            testline = Line(ORIGIN,mob[ndots-1].get_center())
            angle = testline.get_angle()
            
            if angle > 2*PI/3:
                new_dot = Dot(point=path.get_start(), color=RED)
                dots.add(new_dot)

            #this creates dots based on a time interval
            #dot_creation_interval = 1.0  # Time in seconds between new dots
            #if dot_creation_timer.get_value() >= dot_creation_interval:
            #    new_dot = Dot(point=path.get_start(), color=RED)
            #    dots.add(new_dot)
            #    dot_creation_timer.set_value(0)
            #else:
            #    dot_creation_timer.increment_value(dt)

        dots.add_updater(add_new_dot)

        # Animate the movement of all dots along the path
        # This updater will apply to all dots in the 'dots' VGroup
        def move_dots_along_path(mob, dt):
            for dot in mob:
                # Find the current position of the dot along the path's proportion
                # This is a simplified approach; a more precise one might involve
                # storing each dot's individual progress along the path.
                # For a continuous flow, a fixed speed is often desired.
                time = dot_creation_timer.get_value()
                current_proportion = path.proportion_from_point(dot.get_center())
                new_proportion = (current_proportion + dt * 0.5 * np.exp(-1.0*time/5.0) ) % 1 # Adjust 0.1 for speed
                dot.move_to(path.point_from_proportion(new_proportion))

        dots.add_updater(move_dots_along_path)
        self.add(dots)

        self.wait(15) # Wait for a duration to observe the continuous creation and movement
        #self.remove_updater(add_new_dot)
        #dots.remove_updater(move_dots_along_path)



class MovingCircle(Scene):
    def construct(self):
        circle = Circle().move_to([-4,0,0])
        self.add(circle)

        # Define an updater function
        def update_circle(mob, dt):
            mob.shift(RIGHT * dt * 2)  # Move 2 units to the right per second

        # Add the updater to the circle
        circle.add_updater(update_circle)

        # Play the animation for 5 seconds
        self.wait(5)

        # Remove the updater
        circle.remove_updater(update_circle)

class s4(Scene):
    def construct(self):

        emfpath1 = ParametricFunction(
            lambda t: np.array([2*( np.abs(np.cos(t))*np.cos(t) - np.abs(np.sin(t))*np.sin(t) ) - 2,
                -2*( np.abs(np.cos(t))*np.cos(t) + np.abs(np.sin(t))*np.sin(t) ) + 2,
                0
            ]),
            t_range=[0,3*PI/2],
            color=BLUE
        )

        self.play(Create(emfpath1))
        self.wait(3)

class RectangleAttempt(Scene):
    def construct(self):
        rect1 = Rectangle(width=2,height=1)
        dot1 = Dot().set_color(ORANGE)
        self.add(rect1,dot1)
        self.play(MoveAlongPath(dot1,rect1))

class SettingAsCorners(Scene):
    def construct(self):
        corners = (
            [0,0,0],
            [-2,0,0],
            [-2,2,0],
            [0,2,0]
        )

        vmob = VMobject(stroke_color=RED)
        vmob.set_points_as_corners(corners)
        self.play(Create(vmob))