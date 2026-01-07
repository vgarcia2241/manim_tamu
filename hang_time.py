from manim import *
import numpy as np
'''
outlining:

flat ground w circle and initial velocity, draw trajectory and max height, animate ball moving
to demonstrate hang time, present sub line for above h/2 and then sub line for below.


'''
class s1(Scene):
    '''
    Finds intersection points of a parabola and line
    '''
    def collision_points(self, a,b,c,m,d): #used to find where ball hits ramp for any angle
        coeff = [c-d, b-m, a]
        x_vals = np.polynomial.polynomial.polyroots(coeff)
        y_vals = m*x_vals + d
        return x_vals, y_vals
    
    '''
    Finds the path of a circular object given the initial conditions, is also able to give a partial trajectory
    which is mainly used for animation of the trajectory, in that case, the full trajectory is usually found first
    to provide a basis of the time range
    
    Determining t_col_ball for a clipped time is somewhat difficult, I'm thinking that since the ball is still
    travelling the same path, it's just now that we're simultaneously drawing the path, we can still use the original
    full ball trajectory as long as the ball and line are animating at the same rate. As such when clipping, only the
    t_col, x_col, y_col, and trajectory variables change from the unclipped case
    
    might be easier to set the start time always to t_col[0], but wanted to give the additional functionality
    of essentially being able to take any piece of the trajectory.
    '''
    def find_trajectory(self, horizontal_velocity, height, ball, ground, color, clipped = False, times = [0,0]):
        x_col, y_col = self.collision_points(-1/(2* horizontal_velocity ** 2), 0, height, 0, 0)
        x_col_ball, y_col_ball = self.collision_points(-1/(horizontal_velocity ** 2 * 2), 0, height - ball.radius, 0, 0)
        t_col, t_col_ball = x_col / horizontal_velocity, x_col_ball / horizontal_velocity
        
        #user requests full trajectory
        if(not clipped):
            times = t_col
        times_ball = t_col_ball
            
        trajectory = ParametricFunction((lambda t: #seen trajectory on screen
            (horizontal_velocity*t + ball.get_x(), 
             height +ground -(t**2)/2, 0)), t_range = (times[0], times[1]), fill_opacity = 0)
        trajectory.set_color(color)
        trajectory.set_stroke(width = 6)
        trajectory_ball = ParametricFunction((lambda t: #trajectory ball travels on (slightly shorter)
            (horizontal_velocity*t + ball.get_x(), 
             height + ground -(t**2)/2, 0)), t_range = (times_ball[0], times_ball[1]), fill_opacity = 0)
        trajectory_ball.set_color(color)
        trajectory_ball.set_stroke(width = 6)
        
        #if only partial trajectory, changing end points to be the collision points
        if(clipped):
            x_col, y_col = (trajectory.get_point_from_function(times[1]))[0], (trajectory.get_point_from_function(times[1]))[1]
        
        return [x_col, y_col, x_col_ball, y_col_ball, times, times_ball, trajectory, trajectory_ball]
    
    def construct(self):
        #initial and stylistic parameters
        stroke_width = 6
        label_buffer = 0.7
        MathTex.set_default(font_size = 60)
        horizontal_velocity = 0.005
        height = 5.5
        #g = 1
        
        ground = Rectangle(WHITE, 1, 15).move_to([0,-3.6,0]).set_stroke(width = stroke_width)
        #0.05 in ground_top acts as buffer for lineweight
        ground_top = ground.get_critical_point([0,1,0])[1] + 0.05
        ball = Circle(0.2, BLUE, fill_opacity = 1)

        #relevant labels for indexing return values
        '''
          0      1         2           3        4         5          6             7
        x_col, y_col, x_col_ball, y_col_ball, t_col, t_col_ball, trajectory, trajectory_ball
        '''
        t_0 = self.find_trajectory(horizontal_velocity, height, ball, ground_top, YELLOW)
        
        #finding the four distinct parts of the full trajectory
        t3 = np.sqrt(height)
        td = np.sqrt(2*height)
        t4 = td - t3
        
        t_1 = self.find_trajectory(horizontal_velocity, height, ball, ground_top, RED, clipped = True, times = [t_0[5][0], t_0[5][0] + t4])
        t_2 = self.find_trajectory(horizontal_velocity, height, ball, ground_top, YELLOW, clipped = True, times = [t_0[5][0] + t4, t_0[5][0] + td])
        t_3 = self.find_trajectory(horizontal_velocity, height, ball, ground_top, GREEN, clipped = True, times = [t_0[5][0] + td, t_0[5][0] + td + t3])
        t_4 = self.find_trajectory(horizontal_velocity, height, ball, ground_top, PURPLE, clipped = True, times = [t_0[5][0] + td + t3, t_0[5][1]])
        
        #labels for heights
        max_height = BraceLabel(t_0[6], "H", RIGHT, buff = label_buffer, font_size = 60)
        max_height.submobjects[1].set_color(YELLOW)
        height_above = BraceLabel(Line([(t_0[6].get_critical_point([-1,0,0])[0]), t_0[6].get_y(), 0], 
                                       [(t_0[6].get_critical_point([-1,0,0])[0]), (t_0[6].get_critical_point([-1,1,0]))[1], 0]), r"\frac{H}{2}", LEFT, buff = label_buffer, font_size = 60)
        height_below = BraceLabel(Line([(t_0[6].get_critical_point([-1,0,0])[0]), ground_top, 0],
                                       [(t_0[6].get_critical_point([-1,0,0])[0]), t_0[6].get_y(), 0]), r"\frac{H}{2}", LEFT, buff = label_buffer, font_size = 60)
        height_above.submobjects[1].set_color(YELLOW)
        height_below.submobjects[1].set_color(YELLOW)
        
        #setting up time tracking for ball and it's trajectory
        time_tracker = ValueTracker(t_0[5][0])
        trajectory_changing = always_redraw(
            lambda: ParametricFunction((lambda t: (horizontal_velocity*t + t_0[7].get_x(), height + ground_top - ((t)**2)/2, 0)),
            [t_0[5][0], time_tracker.get_value()], fill_opacity = 0).set_color(YELLOW)
        )
        ball_changing = always_redraw(
            lambda: Circle(0.2, BLUE).set_fill(BLUE, opacity = 50).move_to(t_0[7].get_point_from_function(time_tracker.get_value()))
        )
        
        #animations
        ################################################################################################################################
        ball_changing.set_z_index(1)
        ball.set_z_index(1)
        
        self.play(
            FadeIn(ground), 
            GrowFromCenter(ball_changing),
            run_time = 1.5
        )
        
        self.play(Wait(1))
        self.add(trajectory_changing)
        self.play(time_tracker.animate.set_value(t_0[5][1]), run_time = 1.5, rate_func = rate_functions.linear)
        self.play(Wait(1))
        self.play(
            Create(max_height), run_time = 1.5
        )
        self.play(Wait(1))
        self.play(
            Create(height_above),
            Create(height_below),
            run_time = 1
        )
        self.play(Wait(1))
        self.play(Succession(
            Indicate(height_above),
            Indicate(height_below),
            run_time = 2.5
        ))
        self.play(Wait(1))
        
        self.add(t_0[7])
        self.remove(trajectory_changing)
        ball.move_to(ball_changing.get_center())
        self.add(ball)
        self.remove(ball_changing)
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])
        '''
        The below call is the best visual for the ball and hang_time, but I'm unsure how
        to combine it with the live trajectory tracking. Either can be used, it just depends
        which aspect we more want to have
        '''
        #self.play(MoveAlongPath(ball,trajectory_ball), run_time = 2.0, rate_func = rate_functions.double_smooth)
        
class s2(Scene):
    def construct(self):
        text1 = Paragraph('Numeric \nAnswer', font_size = 60, alignment="center")
        text2 = Paragraph('Symbolic \nInformation', font_size = 60, alignment="center").set_color(YELLOW)
        text3 = MathTex(r"\Rightarrow", font_size = 180)
        group1 = Group(text1, text3, text2)
        
        self.play(FadeIn(text1))
        self.play(Wait(1))
        self.play(
            FadeIn(text2),
            FadeIn(text3),
            group1.animate.arrange(LEFT, buff = 1)
        )
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])
        
class s3(Scene):
    '''
    Finds intersection points of a parabola and line
    '''
    def collision_points(self, a,b,c,m,d): #used to find where ball hits ramp for any angle
        coeff = [c-d, b-m, a]
        x_vals = np.polynomial.polynomial.polyroots(coeff)
        y_vals = m*x_vals + d
        return x_vals, y_vals
    
    '''
    Finds the path of a circular object given the initial conditions, is also able to give a partial trajectory
    which is mainly used for animation of the trajectory, in that case, the full trajectory is usually found first
    to provide a basis of the time range
    
    Determining t_col_ball for a clipped time is somewhat difficult, I'm thinking that since the ball is still
    travelling the same path, it's just now that we're simultaneously drawing the path, we can still use the original
    full ball trajectory as long as the ball and line are animating at the same rate. As such when clipping, only the
    t_col, x_col, y_col, and trajectory variables change from the unclipped case
    
    might be easier to set the start time always to t_col[0], but wanted to give the additional functionality
    of essentially being able to take any piece of the trajectory.
    '''
    def find_trajectory(self, horizontal_velocity, height, ball, ground, color, clipped = False, times = [0,0], x_0 = 0):
        x_col, y_col = self.collision_points(-1/(2* horizontal_velocity ** 2), 0, height, 0, 0)
        x_col_ball, y_col_ball = self.collision_points(-1/(horizontal_velocity ** 2 * 2), 0, height - ball.radius, 0, 0)
        x_col += x_0
        x_col += x_0
        t_col, t_col_ball = x_col / horizontal_velocity, x_col_ball / horizontal_velocity
        
        #user requests full trajectory
        if(not clipped):
            times = t_col
        times_ball = t_col_ball
            
        trajectory = ParametricFunction((lambda t: #seen trajectory on screen
            (horizontal_velocity*t + ball.get_x() + x_0, 
             height +ground -(t**2)/2, 0)), t_range = (times[0], times[1]), fill_opacity = 0)
        trajectory.set_color(color)
        trajectory.set_stroke(width = 6)
        trajectory_ball = ParametricFunction((lambda t: #trajectory ball travels on (slightly shorter)
            (horizontal_velocity*t + ball.get_x() + x_0, 
             height + ground -(t**2)/2, 0)), t_range = (times_ball[0], times_ball[1]), fill_opacity = 0)
        trajectory_ball.set_color(color)
        trajectory_ball.set_stroke(width = 6)
        
        #if only partial trajectory, changing end points to be the collision points
        if(clipped):
            x_col, y_col = (trajectory.get_point_from_function(times[1]))[0], (trajectory.get_point_from_function(times[1]))[1]
        
        return [x_col, y_col, x_col_ball, y_col_ball, times, times_ball, trajectory, trajectory_ball]
    
    def construct(self):
        #initial and stylistic parameters
        stroke_width = 6
        label_buffer = 0.7
        MathTex.set_default(font_size = 60)
        horizontal_velocity = 0.005
        horizontal_velocity_extended = horizontal_velocity * 75
        height = 5.5
        #g = 1
        
        ground = Rectangle(WHITE, 1, 15).move_to([0,-3.6,0]).set_stroke(width = stroke_width)
        #0.05 in ground_top acts as buffer for lineweight
        ground_top = ground.get_critical_point([0,1,0])[1] + 0.05
        ball = Circle(0.2, BLUE, fill_opacity = 1)

        #relevant labels for indexing return values
        '''
          0      1         2           3        4         5          6             7
        x_col, y_col, x_col_ball, y_col_ball, t_col, t_col_ball, trajectory, trajectory_ball
        '''
        t_0 = self.find_trajectory(horizontal_velocity, height, ball, ground_top, YELLOW)
        
        #finding the four distinct parts of the full trajectory
        t3 = np.sqrt(height)
        td = np.sqrt(2*height)
        t4 = td - t3
        
        t_left_half = self.find_trajectory(horizontal_velocity, height, ball, ground_top, YELLOW, clipped = True, times = [t_0[4][0], t_0[4][0] + td])
        t_right_half = self.find_trajectory(horizontal_velocity, height, ball, ground_top, YELLOW, clipped = True, times = [t_0[4][0] + td, t_0[4][1]])
        
        t_1 = self.find_trajectory(horizontal_velocity_extended, height, ball, ground_top, MAROON, clipped = True, times = [t_0[4][0], t_0[4][0] + t4])
        t_2 = self.find_trajectory(horizontal_velocity_extended, height, ball, ground_top, ORANGE, clipped = True, times = [t_0[4][0] + t4, t_0[4][0] + td])
        t_3 = self.find_trajectory(horizontal_velocity_extended, height, ball, ground_top, GREEN_C, clipped = True, times = [t_0[4][0] + td, t_0[4][0] + td + t3])
        t_4 = self.find_trajectory(horizontal_velocity_extended, height, ball, ground_top, PURPLE, clipped = True, times = [t_0[4][0] + td + t3, t_0[4][1]])
        
        t_left_half_extended = self.find_trajectory(horizontal_velocity_extended, height, ball, ground_top, YELLOW, clipped = True, times = [t_0[4][0], t_0[4][0] + td])
        t_right_half_extended = self.find_trajectory(horizontal_velocity_extended, height, ball, ground_top, YELLOW, clipped = True, times = [t_0[4][0] + td, t_0[4][1]])
        
        #labels for heights
        max_height = BraceLabel(t_0[6], "H", RIGHT, buff = label_buffer, font_size = 60)
        max_height.submobjects[1].set_color(YELLOW)
        height_above = BraceLabel(Line([(t_0[6].get_critical_point([-1,0,0])[0]), t_0[6].get_y(), 0], 
                                       [(t_0[6].get_critical_point([-1,0,0])[0]), (t_0[6].get_critical_point([-1,1,0]))[1], 0]), r"\frac{H}{2}", LEFT, buff = label_buffer, font_size = 60)
        height_below = BraceLabel(Line([(t_0[6].get_critical_point([-1,0,0])[0]), ground_top, 0],
                                       [(t_0[6].get_critical_point([-1,0,0])[0]), t_0[6].get_y(), 0]), r"\frac{H}{2}", LEFT, buff = label_buffer, font_size = 60)
        height_above.submobjects[1].set_color(YELLOW)
        height_below.submobjects[1].set_color(YELLOW)
        
        #labels for separate parts of the ball's path
        text1 = MathTex(r"t1").next_to(t_1[6], LEFT).set_color(t_1[6].color)
        text2 = MathTex(r"t2").next_to(t_2[6], LEFT).set_color(t_2[6].color)
        text3 = MathTex(r"t3").next_to(t_3[6], RIGHT).set_color(t_3[6].color)
        text4 = MathTex(r"t4").next_to(t_4[6], RIGHT).set_color(t_4[6].color)
        
        #animations
        ################################################################################################################################
        ball.set_z_index(1)
        ball.move_to(t_0[7].get_point_from_function(t_0[5][1]))
        
        self.play(
            FadeIn(ground),
            FadeIn(ball),
            FadeIn(t_left_half[6]),
            FadeIn(t_right_half[6]),
            run_time = 1.5
        )
        self.play(Wait(1))
        self.play(
            Transform(t_left_half[6], t_left_half_extended[6]),
            Transform(t_right_half[6], t_right_half_extended[6]),
            ball.animate.move_to(t_right_half_extended[7].get_point_from_function(t_right_half_extended[5][1])),
            run_time = 1.5
        )
        self.play(Wait(1))
        self.play(Succession(
            Indicate(t_left_half[6], color = WHITE),
            Indicate(t_right_half[6], color = WHITE),
            run_time = 2
        ))
        
        self.play(Wait(1))
        height_above.set_x(t_left_half_extended[6].get_critical_point([-1,0,0])[0] - 2.5*label_buffer)
        height_below.set_x(t_left_half_extended[6].get_critical_point([-1,0,0])[0] - 2.5*label_buffer)
        self.play(Create(height_above), Create(height_below))
        
        self.play(Wait(1))
        self.play(Succession(Create(t_1[6]), Write(text1)))
        self.play(Wait(1))
        self.play(Succession(Create(t_2[6]), Write(text2)))
        self.play(Wait(1))
        self.play(Succession(Create(t_3[6]), Write(text3)))
        self.play(Wait(1))
        self.play(Succession(Create(t_4[6]), Write(text4)))
        
        self.remove(t_left_half[6])
        self.remove(t_right_half[6])
        
        self.play(Wait(1))
        self.play(Succession(Indicate(text1), Indicate(text4)), run_time = 2)
        self.play(Wait(1))
        self.play(Succession(Indicate(text2), Indicate(text3)), run_time = 2)
        self.play(Wait(1))
        
        group1 = Group()
        for i in self.mobjects:
            group1.add(i)
        group1.remove(ground)
        
        text5 = MathTex(r"\frac{t_2 + t_3}{t_1}").set_font_size(80)
        text5_a = MathTex(r"\frac{2t_3}{t_4}").set_font_size(80)
        
        text5.move_to([3.5,0,0])
        text5_a.move_to(text5)

        self.play(
            Write(text5),
            group1.animate.to_edge(LEFT, buff = 1.7),
            run_time = 1.5
        )
        self.play(Wait(1))
        
        #new trajectory with left shift, easier than trying to adjust the one we have
        t_0_extended = self.find_trajectory(horizontal_velocity_extended, height, ball, ground_top, YELLOW, x_0 = t_1[7].get_critical_point([-1,0,0])[0])
        #live tracking
        time_tracker = ValueTracker(t_0_extended[5][1])
        ball_changing = always_redraw(
            lambda: Circle(0.2, BLUE).set_fill(BLUE, opacity = 50).move_to(t_0_extended[7].get_point_from_function(time_tracker.get_value()))
        )
        self.add(ball_changing)
        self.remove(ball)
        
        self.play(time_tracker.animate.set_value(t_0_extended[5][0]), rate_func = rate_functions.linear)
        print(t_0_extended[5])
        print(t_1[4])
        self.play(Wait(1))
        self.play(time_tracker.animate.set_value(t_1[4][1]))
        self.play(Wait(1))
        self.play(time_tracker.animate.set_value(t_3[4][1]))
        self.play(Wait(1))
        self.play(TransformMatchingTex(text5, text5_a))
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])

class s4(Scene):
    def construct(self):
        #initial and stylistic parameters
        stroke_width = 6
        label_buffer = 0.6
        MathTex.set_default(font_size = 60)
        
        text1 = MathTex(r"t_3", font_size = 80)
        text2 = MathTex(r"v = 0")
        text3 = MathTex(r"a = -g")
        text4 = MathTex(r"y_0 = H")
        text5 = MathTex(r"y_f = \frac{H}{2}")
        group1 = Group(text2, text3, text4, text5).arrange(DOWN, buff = label_buffer)
        text1.to_edge(UP, buff = label_buffer)
        tx1_under = Underline(text1).next_to(text1, DOWN, buff = 0.1)
        
        text6 = MathTex(r"\frac{H}{2} = H - \frac{gt^2}{2}")
        text7 = MathTex(r"t_3 = \sqrt{\frac{H}{g}}")
        group2 = Group(text6)
        
        text8 = MathTex(r"\Rightarrow", font_size = 80)
        
        group3 = Group(group1, group2)
        
        self.play(FadeIn(text1), Write(tx1_under))
        self.play(Wait(1))
        self.play(Succession(
            Write(text2), 
            Write(text3), 
            Write(text4),
            Write(text5),
            run_time = 4
        ))
        self.play(Wait(1))
        self.play(
            Write(text6),
            group3.animate.arrange(RIGHT, buff = 2.5).set_x(0.7),
            Write(text8)
        )
        self.play(Wait(1))
        self.play(FadeOut(group3), FadeOut(text8))
        self.play(Write(text7))
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])
        
class s5(Scene):
    def construct(self):
        #initial and stylistic parameters
        stroke_width = 6
        label_buffer = 0.6
        MathTex.set_default(font_size = 60)
        
        text1 = MathTex(r"v(y = \frac{H}{2}) \Rightarrow t4")
        text2 = MathTex(r"t_d")
        text3 = MathTex(r"t_d = t_3 + t_4")
        text4 = MathTex(r"0 = H - \frac{gt_d^2}{2}")
        text5 = MathTex(r"t_d = \sqrt{\frac{2H}{g}}")
        text6 = MathTex(r"\Rightarrow", font_size = 80)
        
        group1 = Group(text3, text4)

        self.play(Write(text1))
        self.play(Wait(1))
        self.play(Unwrite(text1))
        self.play(Wait(1))
        self.play(Write(text2))
        self.play(Wait(1))
        self.play(TransformMatchingShapes(text2, text3))
        self.play(Wait(1))
        self.play(
            Write(text4), 
            group1.animate.arrange(RIGHT, buff = 2),
            Write(text6)
        )
        self.play(Wait(1))
        
        self.play(FadeOut(text3), FadeOut(text4), FadeOut(text6))
        self.play(Write(text5))
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])
        
class s6(Scene):
    def construct(self):
        #initial and stylistic parameters
        stroke_width = 6
        label_buffer = 0.6
        MathTex.set_default(font_size = 80)
        
        text1 = MathTex(r"\frac{2t_3}{t_4}")
        text2 = MathTex(r"\frac{2t_3}{t_d-t_3}")
        text3 = MathTex(r"\frac{2 \sqrt{H/g}}{\sqrt{2H/g} - \sqrt{H/g}}")
        text4 = MathTex(r"\frac{2}{\sqrt{2} - 1}")
        
        self.play(Write(text1))
        self.play(Wait(1))
        self.play(TransformMatchingTex(text1, text2))
        self.play(Wait(1))
        self.play(TransformMatchingTex(text2, text3))
        self.play(Wait(1))
        self.play(TransformMatchingShapes(text3, text4))
        self.play(Circumscribe(text4), run_time = 2)
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])
        
        
        