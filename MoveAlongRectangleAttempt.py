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

class OutputPoints(Scene):
    def construct(self):

        rate=0.1

        Rect1 = Rectangle(width=2,height=2).move_to([-1,0,0])
        #self.add(Rect1)

        new_emfdot = Dot(point=Rect1.point_from_proportion(0.75), color=RED)
        self.add(new_emfdot)

        for i in range(75):
            #print(i)
            print(Rect1.point_from_proportion(0.75-i/100))

            #Option 1 just assumes it is at an alpha and updates it. This works.
            #if 0.75-2*i/100 < 0.0:
            #    self.play(new_emfdot.animate.move_to(Rect1.point_from_proportion(0.0)),rate_func=linear,run_time=0.2)
            #else:
            #    self.play(new_emfdot.animate.move_to(Rect1.point_from_proportion(0.75-2*i/100)),rate_func=linear,run_time=0.2)
            
            #Option 2 gets current proportion from current point and then updates a new proportion value. This does not work.
            #currentprop = Rect1.proportion_from_point(new_emfdot.get_center())
            #if currentprop-2*i/100 < 0.0:
            #    newprop = 0.0
            #else:
            #    newprop = currentprop-2*i/100

            #self.play(new_emfdot.animate.move_to(Rect1.point_from_proportion(newprop)),rate_func=linear,run_time=0.2)

            #Option 3 is going to be like 2 but I'm going to calculate the alpha myself based on the position.
            #This seems to be working but really does not like that last spot. It doesn't seem to grasp that it is going to be negative 
            #leading to an alpha of -0.0100000000009 or something stupid like that. But I don't understand why the continuous around the circle 
            #works then.
            x = new_emfdot.get_center()[0]
            y = new_emfdot.get_center()[1]
            
            if abs(y+1)<0.01:
                currentprop = 0.5+0.25*(x+2.)/2
            elif abs(y-1)<0.01:
                currentprop = 0.25-0.25*(x+2.)/2
            else:
                currentprop = 0.5-0.25*(y+1.)/2
            
            if np.sign(currentprop-1./100) == -1.:
                newprop = 0.0
            else:
                newprop = currentprop-1./100

            print(currentprop)
            print(newprop)

            self.play(new_emfdot.animate.move_to(Rect1.point_from_proportion(newprop)),rate_func=linear,run_time=0.2)


                
        #emfdots1.add_updater(move_emfdots_along_path)

        self.wait(3)

        
class AddingNewDots(Scene):
    def construct(self):
        rate=0.1

        Rect1 = Rectangle(width=2,height=2).move_to([-1,0,0])
        #self.add(Rect1)

        emfdots1 = VGroup()
        new_emfdot = Dot(point=Rect1.point_from_proportion(0.75), color=RED)
        emfdots1.add(new_emfdot)
        self.add(emfdots1)
        #self.add(new_emfdot)

        

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
            if mob[ndots-1].get_center()[0]<-0.5: 
                new_dot = Dot(point=Rect1.point_from_proportion(0.75), color=RED)
                emfdots1.add(new_dot)
        emfdots1.add_updater(add_new_emfdots1)

        def move_emfdots_along_path1(mob, dt):
            for dot in mob:
                x = dot.get_center()[0]
                y = dot.get_center()[1]
            
                if abs(y+1)<0.01:
                    currentprop = 0.5+0.25*(x+2.)/2
                elif abs(y-1)<0.01:
                    currentprop = 0.25-0.25*(x+2.)/2
                else:
                    currentprop = 0.5-0.25*(y+1.)/2

                    
            
                if np.sign(currentprop-1./100) == -1.:
                    newprop = 0.0
                else:
                    newprop = currentprop-1./100

                dot.move_to(Rect1.point_from_proportion(newprop))
                
        emfdots1.add_updater(move_emfdots_along_path1)
        

        
        self.wait(10)