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
class s1(Scene):
    def construct(self):
        #initialization
        ramp_width = 8.75
        ramp_height = 5
        ramp_slope = -ramp_height / ramp_width
        ramp_diag = np.array([ramp_width,-ramp_height,0])
        ramp = Polygon([0,0,0], [ramp_width,0,0], [0,ramp_height,0], color = WHITE) #screen coords run -7,7 -4,4
        ramp.move_to([0,-1.2,0])
        ramp_top = ramp.get_critical_point([-1,1,0])
        
        ball_radius = 0.15
        ball = Circle(radius = ball_radius, color = ORANGE, fill_opacity = 1)
        
        t1 = MathTex(r"v_0", stroke_width = 1, font_size=60)
        t1.set_color(GREEN)
        t2 = MathTex(r"\theta", stroke_width = 1, font_size=60)
        t2.set_color(YELLOW)
        
        #some movement and further initializations
        ball_start = 0.1
        ball.move_to(ramp_top + [0,ball_radius + 0.07,0] + ball_start*ramp_diag)
        v_0 = Arrow(ball.get_center() + [ball_radius,0,0] , ball.get_center() + 1.5*RIGHT,color= GREEN, buff=0) 
        t1.next_to(v_0, RIGHT, buff = 0.2)
        t2.move_to(ramp.get_critical_point([1,-1,0]) + [-2,0.5,0])
        
        #label for distance, should more robustly define to fit actual trajectory
        l=Line(ramp_top + ball_start*ramp_diag, ramp_top + ball_start*ramp_diag + 0.47*ramp_diag, color = WHITE)  
        l_vec = l.get_end() - l.get_start()
        l_len = np.linalg.norm(l_vec)
        l_unit = l_vec / l_len
        new_direction = np.array([l_unit[1], -l_unit[0], 0])
        label1 = BraceLabel(l, text= "d", color= YELLOW, buff=0.1, brace_direction = new_direction, font_size = 60) 
        label1.submobjects[1].set_color(YELLOW), label1.submobjects[1].set_stroke(width = 1)
        
        #added some small pauses assuming speech will need to catch up, can adjust
        self.play(Create(ramp))
        self.play(Wait(1))
        self.play(
            Create(ball), Create(v_0), Write(t1), run_time=1.5
        )
        self.play(Wait(1))
        self.play(Write(t2))
        self.play(Wait(1))
        self.play(Create(label1.submobjects[0]), run_time = 1)
        self.play(Wait(1))
        self.play(Write(label1.submobjects[1]))
        self.play(Wait(1))
        self.play(
            FadeOut(l), FadeOut(label1), FadeOut(t2)
        )
        #Ending initial setup
        
        #showing forces and coordinates
        gravity = Arrow(ball.get_center() + [0,-ball_radius,0] , ball.get_center() + 1.5*DOWN,color= BLUE, buff=0)
        drag = Arrow(ball.get_center() + [-ball_radius,0,0] , ball.get_center() + 1.5*LEFT,color= RED, buff=0)
        t3 = MathTex(r"F_{gravity}", stroke_width = 1, font_size=60)
        t3.set_color(BLUE)
        
        t4 = MathTex(r"F_{drag}", stroke_width = 1, font_size=60)
        t4.set_color(RED)
        t3.next_to(gravity, LEFT, buff = 0.1)
        t4.next_to(drag, UP)
    
        self.play(
            Create(gravity), Create(drag), Write(t3), Write(t4), run_time=3
        )
        self.play(Wait(1))
        self.play(FadeOut(drag), FadeOut(t4))
        self.play(Wait(1))
        #ending forces, moving to coords
        
        #non altered cartesian coords
        axis_origin = ramp.get_critical_point([-1,-1,0]) + [0.87,0.7,0]
        x_axis = Arrow(axis_origin, axis_origin + 1.5*RIGHT,color= WHITE, buff=0)
        y_axis = Arrow(axis_origin, axis_origin + 1.5*UP,color= WHITE, buff=0)
        t5 = MathTex("x", stroke_width = 1, font_size=60)
        t6 = MathTex("y", stroke_width = 1, font_size=60)
        t5.next_to(x_axis, DOWN, buff = 0.1)
        t6.next_to(y_axis, LEFT, buff = 0.1)
        
        self.play(
            Create(x_axis), Create(y_axis), Create(t5), Create(t6), run_time = 2
        )
        self.play(Wait(1))
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])
        
        
'''
equations with inital conditions and subsequent simplifications
'''
class s2(Scene):
    def construct(self):
        MathTex.set_default(font_size = 70)
        buff_size = 0.5
        
        eq1 = MathTex(r"x(t) = x_0 +v_xt")
        eq2 = MathTex(r"y(t) = y_0 +v_{0,y}t - \frac{g}{2}t^2")
        eq3 = MathTex(r"v_y = v_{0,y} -gt")
        eq4 = MathTex(r"v_y^2 = v_{0,y}^2 - 2g \Delta y")
        g1 = VGroup(eq1, eq2, eq3, eq4)
        g1.arrange(DOWN, buff = buff_size)
        
        self.play(
            Write(eq1), Write(eq2), Write(eq3), Write(eq4)
        )
        self.play(Wait(1))
        
        eq1_2 = MathTex(r"x = x_0 + v_0t")
        eq2_2 = MathTex(r"y = y_0 -\frac{g}{2}t^2")
        eq3_2 = MathTex(r"v_y = -gt")
        eq4_2 = MathTex(r"v_y^2 = -2gy")
        g2 = VGroup(eq1_2,eq2_2,eq3_2,eq4_2)
        g2.arrange(DOWN, buff = 0.49)
        
        #should replace original eq with eq_2 version
        self.play(
            FadeTransform(eq1,eq1_2),
            FadeTransform(eq2,eq2_2),
            FadeTransform(eq3,eq3_2),
            FadeTransform(eq4, eq4_2)
        )
        self.play(Wait(1))
        
        eq1_3 = MathTex(r"x = v_0t")
        eq2_3 = MathTex(r"y = -\frac{g}{2}t^2")
        eq3_3 = MathTex(r"v_y = -gt")
        eq4_3 = MathTex(r"v_y^2 = -2gy")
        g3 = VGroup(eq1_3,eq2_3,eq3_3,eq4_3)
        g3.arrange(DOWN, buff = buff_size)
        
        #should replace original eq_2 with eq_3 version
        self.play(
            FadeTransform(eq1_2,eq1_3),
            FadeTransform(eq2_2,eq2_3),
            FadeTransform(eq3_2,eq3_3),
            FadeTransform(eq4_2,eq4_3)
        )
        self.play(Wait(1))
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])
        
'''
showing ball motion
'''
class s3(Scene):
    def collision_points(self, a,b,c,m,d): #used to find where ball hits ramp for any angle
        coeff = [c-d, b-m, a]
        x_vals = np.polynomial.polynomial.polyroots(coeff)
        y_vals = m*x_vals + d
        return x_vals, y_vals
    
    def construct(self):
        #initialization
        MathTex.set_default(font_size = 60)
        
        ramp_width = 8.75
        ramp_height = 5
        ramp_slope = -ramp_height / ramp_width
        ramp_diag = np.array([ramp_width,-ramp_height,0])
        ramp = Polygon([0,0,0], [ramp_width,0,0], [0,ramp_height,0], color = WHITE) #screen coords run -7,7 -4,4
        ramp.move_to([0,-1.2,0])
        ramp_top = ramp.get_critical_point([-1,1,0])
        
        ball_radius = 0.15
        ball = Circle(radius = ball_radius, color = ORANGE, fill_opacity = 1)
        
        horizontal_velocity = 3 #changable parameter
        ramp_slope = -ramp_height/ramp_width #changable parameter
        
        t1 = MathTex(r"v_0", stroke_width = 1)
        t1.set_color(GREEN)
        t2 = MathTex(r"\theta", stroke_width = 1)
        t2.set_color(YELLOW)
        
        #some movement and further initializations
        ball_start = 0.1
        ball.move_to(ramp_top + [0,ball_radius + 0.07,0] + ball_start*ramp_diag)
        v_0 = Arrow(ball.get_center() + [ball_radius,0,0] , ball.get_center() + 0.5*horizontal_velocity*RIGHT,
                    color= GREEN, buff=0, max_stroke_width_to_length_ratio= 10, max_tip_length_to_length_ratio= 1) 
        t1.next_to(v_0, RIGHT, buff = 0.2)
        t2.move_to(ramp.get_critical_point([1,-1,0]) + [-2,0.5,0])
        
        #altered cartesian coords (ball_centered)
        axis_origin = ball.get_center()
        x_axis = Arrow(axis_origin, axis_origin + 1.5*RIGHT,color= WHITE, buff=0)
        y_axis = Arrow(axis_origin, axis_origin + 1.5*UP,color= WHITE, buff=0)
        t5 = MathTex("x", stroke_width = 1)
        t6 = MathTex("y", stroke_width = 1)
        t5.next_to(x_axis, DOWN, buff = 0.1)
        t6.next_to(y_axis, LEFT, buff = 0.1)
        
#########################################################################################
        
        #drawing trajectory
        #gravity is set to 1 since it should be static
        
        '''
        defined the ramp and ball motion as functions in the form y=mx+b and ax^2+c = y, and used those
        coefficients to find their intersection points, x and y should each have two vals, only interested in 2nd.
        two collision times, one for the line, and one for the ball 
        '''
        x_col, y_col = self.collision_points(-1/(horizontal_velocity ** 2), 0, ball_radius, ramp_slope, 0)
        x_col_ball, y_col_ball = self.collision_points(-1/(horizontal_velocity ** 2), 0, 0, ramp_slope, 0)
        t_col = x_col[1] / horizontal_velocity     
        t_col_ball = x_col_ball[1] / horizontal_velocity
        
        trajectory = ParametricFunction((lambda t: #seen trajectory on screen
            (horizontal_velocity*t + ball.get_x(), 
             -(t**2) + ball.get_y(), 0)), t_range = (0,t_col), fill_opacity = 0)
        trajectory.set_color(ORANGE)
        trajectory.set_stroke(width = 6)
        trajectory_ball = ParametricFunction((lambda t: #trajectory ball travels on (slightly shorter)
            (horizontal_velocity*t + ball.get_x(), 
             -(t**2) + ball.get_y(), 0)), t_range = (0,t_col_ball), fill_opacity = 0)
        trajectory_ball.set_color(ORANGE)
        trajectory_ball.set_stroke(width = 6)   
        
#########################################################################################
        #lines for x and y displacement
        ball_end = trajectory_ball.get_critical_point([1,-1,0])
        delta_x = Line(ball.get_center(), [ball_end[0], ball.get_y(), 0]).set_color(YELLOW)
        delta_y = Line([ball_end[0], ball.get_y(), 0], ball_end).set_color(YELLOW)
        delta_x.set_stroke(width = 6)
        delta_y.set_stroke(width = 6)
        t7 = MathTex(r"\Delta x").set_color(YELLOW)
        t8 = MathTex(r"\Delta y").set_color(YELLOW)
        t7.next_to(delta_x, UP)
        t8.next_to(delta_y, RIGHT)
        
        #arrow showing y_0 and y_f
        y_change = Arrow([ball_end[0] + ball_radius + 1.5, ball.get_y(), 0], [ball_end[0] + ball_radius, ball.get_y(), 0],
                         buff = 0.1, color = WHITE)

        #label for distance, should more robustly define to fit actual trajectory
        l=Line(ramp_top + ball_start*ramp_diag, ball_end - [0, ball_radius + 0.1, 0], color = WHITE)  
        l_vec = l.get_end() - l.get_start()
        l_len = np.linalg.norm(l_vec)
        l_unit = l_vec / l_len
        new_direction = np.array([l_unit[1], -l_unit[0], 0])
        label1 = BraceLabel(l, text= "d", color= YELLOW, buff=0.1, brace_direction = new_direction, font_size = 60) 
        label1.submobjects[1].set_color(YELLOW), label1.submobjects[1].set_stroke(width = 1)
        
#########################################################################################
        ball.set_z_index(1)
        
        #animations
        self.play(Wait(1))
        self.play(
            FadeIn(ramp), FadeIn(ball),
            FadeIn(v_0), FadeIn(t1),
            FadeIn(t2), run_time = 2
        )
        self.play(FadeIn(label1.submobjects[0]), Write(label1.submobjects[1]))
        self.play(Wait(1))
        
        self.play(Wait(1))
        #can also sub in trajectory_ball if don't want overhanging line
        self.play(Create(trajectory_ball)) 
        self.play(
            FadeOut(v_0), 
            FadeOut(t1)
        )
        self.play(Wait(1))
        #self.add(trajectory_ball)
        self.play(MoveAlongPath(ball,trajectory_ball), run_time = 1.5)
        self.play(Wait(1))
        self.play(
            Create(delta_x), Create(delta_y),
            Write(t7), Write(t8)
        )
        self.play(Wait(1))
        self.play(
            Indicate(t7), Indicate(t8),
            run_time = 1.5
            )
        self.play(Wait(1))
        self.play(FadeOut(trajectory_ball))
        self.play(Wait(1))
        self.play(Create(y_change), run_time = 0.7)
        self.play(Wait(1))
        self.play(y_change.animate.move_to([y_change.get_x(), ball_end[1], 0]), run_time = 1.2)
        self.play(Wait(1))
        self.play(Indicate(t7, color = WHITE), run_time = 1.5)
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])
        
'''
Further simplifying equations from s2 including highlighting
'''        
class s4(Scene):
    def construct(self):
        #intializing MathTex from where we left off in s2
        MathTex.set_default(font_size = 70)
        buff_size = 0.5
        
        t1 = MathTex(r"d = \sqrt{x^2 + y^2}")
        t2 = MathTex(r"x = v_0t")
        t3 = MathTex(r"y = -\frac{g}{2}t^2")
        t4 = MathTex(r"v_y = -gt")
        t5 = MathTex(r"v_y^2 = -2gy")
        group1 = VGroup(t2, t3, t4, t5)
        #possible positions for the equations to be
        positions = np.array([[[-3,2.25,0], [3,2.25,0]],
                             [[-3,0.75,0], [3,0.75,0]],
                             [[-3,-0.75,0], [3,-0.75,0]],
                             [[-3,-2.25,0], [3,-2.25,0]]])
        dividing_line = Line([0,3.5,0], [0,-3.5, 0]).set_stroke(width = 4)

        t2.move_to(positions[0][0])
        t3.move_to(positions[1][0])
        t4.move_to(positions[2][0])
        t5.move_to(positions[3][0])

        #animation
        self.play(Write(t1))
        self.play(Wait(1))
        self.play(
            t1.animate.move_to(positions[0][1]),
            FadeIn(group1),
            Create(dividing_line)
        )
        self.play(Wait(1.0))
        self.play(
            Indicate(t2),
            run_time = 1.5
        )
        self.play(Wait(1))
        self.play(
            t2.animate.move_to(positions[1][1]),
            t3.animate.move_to(positions[0][0]),
            t4.animate.move_to(positions[1][0]),
            t5.animate.move_to(positions[2][0])
        )
        self.play(Wait(1))
        self.play(Succession(
            Indicate(t3, color = WHITE),
            Indicate(t5, color = WHITE),
            run_time = 3
        ))
        self.play(Wait(1))
        self.play(Indicate(t5), run_time = 1.5)
        self.play(Wait(1))
        self.play(Indicate(t3), run_time = 1.5)
        self.play(Wait(1))
        self.play(
            t3.animate.move_to(positions[2][1]),
            t4.animate.move_to(positions[0][0]),
            t5.animate.move_to(positions[1][0])
            )
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])

'''
Showing the effect of different velocities
'''
class s5(Scene):
    def collision_points(self, a,b,c,m,d): #used to find where ball hits ramp for any angle
        coeff = [c-d, b-m, a]
        x_vals = np.polynomial.polynomial.polyroots(coeff)
        y_vals = m*x_vals + d
        return x_vals, y_vals
    
    def x_y_displacements(self, trajectory, ball, color):
        ball_end = trajectory.get_critical_point([1,-1,0])
        delta_x = Line(ball.get_center(), [ball_end[0], ball.get_y(), 0]).set_color(color).set_stroke(width = 6)
        delta_y = Line([ball_end[0], ball.get_y(), 0], ball_end).set_color(color).set_stroke(width = 6)
        ta = MathTex(r"\Delta x").set_color(color)
        tb = MathTex(r"\Delta y").set_color(color)
        ta.next_to(delta_x, UP)
        tb.next_to(delta_y, RIGHT)
        return ball_end, delta_x, delta_y, ta, tb
    
    def find_trajectory(self, horizontal_velocity, ball, ramp_slope, color):
        x_col, y_col = self.collision_points(-1/(horizontal_velocity ** 2), 0, ball.radius, ramp_slope, 0)
        x_col_ball, y_col_ball = self.collision_points(-1/(horizontal_velocity ** 2), 0, 0, ramp_slope, 0)
        t_col = x_col[1] / horizontal_velocity     
        t_col_ball = x_col_ball[1] / horizontal_velocity
        
        trajectory = ParametricFunction((lambda t: #seen trajectory on screen
            (horizontal_velocity*t + ball.get_x(), 
             -(t**2) + ball.get_y(), 0)), t_range = (0,t_col), fill_opacity = 0)
        trajectory.set_color(color)
        trajectory.set_stroke(width = 6)
        trajectory_ball = ParametricFunction((lambda t: #trajectory ball travels on (slightly shorter)
            (horizontal_velocity*t + ball.get_x(), 
             -(t**2) + ball.get_y(), 0)), t_range = (0,t_col_ball), fill_opacity = 0)
        trajectory_ball.set_color(color)
        trajectory_ball.set_stroke(width = 6)
        return x_col, y_col, x_col_ball, y_col_ball, t_col, t_col_ball, trajectory, trajectory_ball
    
    def construct(self):
        #initialization
        MathTex.set_default(font_size = 60)
        
        ramp_width = 8.75
        ramp_height = 5
        ramp_slope = -ramp_height / ramp_width
        ramp_diag = np.array([ramp_width,-ramp_height,0])
        ramp = Polygon([0,0,0], [ramp_width,0,0], [0,ramp_height,0], color = WHITE) #screen coords run -7,7 -4,4
        ramp.move_to([0,-1.2,0])
        ramp_top = ramp.get_critical_point([-1,1,0])
        
        ball_radius = 0.15
        ball = Circle(radius = ball_radius, color = ORANGE, fill_opacity = 1)
        
        horizontal_velocity = 3 #changable parameter
        horizontal_velocity_1 = horizontal_velocity * 0.4
        horizontal_velocity_2 = horizontal_velocity * 1.2
        ramp_slope = -ramp_height/ramp_width #changable parameter
        
        t1 = MathTex(r"v_0", stroke_width = 1)
        t1.set_color(GREEN)
        t2 = MathTex(r"\theta", stroke_width = 1)
        t2.set_color(YELLOW)
        
        #some movement and further initializations
        ball_start = 0.1
        ball.move_to(ramp_top + [0,ball_radius + 0.07,0] + ball_start*ramp_diag)
        v_0 = Arrow(ball.get_center() + [ball_radius,0,0] , ball.get_center() + 0.5*horizontal_velocity*RIGHT,
                    color= GREEN, buff=0, max_stroke_width_to_length_ratio= 10, max_tip_length_to_length_ratio= 1) 
        #shorter and longer arrows for compartive trajectories
        v_1 = Arrow(ball.get_center() + [ball_radius,0,0] , ball.get_center() + 0.5*horizontal_velocity_1*RIGHT,
                    color= YELLOW, buff=0, max_stroke_width_to_length_ratio= 10, max_tip_length_to_length_ratio= 1)
        v_2 = Arrow(ball.get_center() + [ball_radius,0,0] , ball.get_center() + 0.5*horizontal_velocity_2*RIGHT,
                    color= BLUE, buff=0, max_stroke_width_to_length_ratio= 10, max_tip_length_to_length_ratio= 1)
        t1.next_to(v_0, RIGHT, buff = 0.2)
        t2.move_to(ramp.get_critical_point([1,-1,0]) + [-2,0.5,0])
        
        #altered cartesian coords (ball_centered)
        axis_origin = ball.get_center()
        x_axis = Arrow(axis_origin, axis_origin + 1.5*RIGHT,color= WHITE, buff=0)
        y_axis = Arrow(axis_origin, axis_origin + 1.5*UP,color= WHITE, buff=0)
        t5 = MathTex("x", stroke_width = 1)
        t6 = MathTex("y", stroke_width = 1)
        t5.next_to(x_axis, DOWN, buff = 0.1)
        t6.next_to(y_axis, LEFT, buff = 0.1)
        
#########################################################################################
        #drawing trajectory
        #gravity is set to 1 since it should be static
        '''
        defined the ramp and ball motion as functions in the form y=mx+b and ax^2+c = y, and used those
        coefficients to find their intersection points, x and y should each have two vals, only interested in 2nd.
        two collision times, one for the line, and one for the ball 
        '''
        x_col, y_col, x_col_ball, y_col_ball, t_col, t_col_ball, trajectory, trajectory_ball = self.find_trajectory(horizontal_velocity, ball, ramp_slope, GREEN)
        #shorter trajectory
        x_col_1, y_col_1, x_col_ball_1, y_col_ball_1, t_col_1, t_col_ball_1, trajectory_1, trajectory_ball_1 = self.find_trajectory(horizontal_velocity_1, ball, ramp_slope, YELLOW)
        #longer trajectory
        x_col_2, y_col_2, x_col_ball_2, y_col_ball_2, t_col_2, t_col_ball_2, trajectory_2, trajectory_ball_2 = self.find_trajectory(horizontal_velocity_2, ball, ramp_slope, BLUE)
#########################################################################################
        #lines for x and y displacement, and their collision points
        ball_end, delta_x, delta_y, t7, t8 = self.x_y_displacements(trajectory, ball, YELLOW)
        ball_end_1, delta_x_1, delta_y_1, t71, t81 = self.x_y_displacements(trajectory_1, ball, YELLOW)
        ball_end_2, delta_x_2, delta_y_2, t72, t82 = self.x_y_displacements(trajectory_2, ball, YELLOW)
        
        point_0 = Dot(ball_end, color = GREEN).set_stroke(width = 9)
        point_1 = Dot(ball_end_1, color = YELLOW).set_stroke(width = 9)
        point_2 = Dot(ball_end_2 - [0,0.05,0], color = BLUE).set_stroke(width = 9)
        connection = Line(point_1, point_2).set_color(YELLOW).set_stroke(width = 8)
#########################################################################################
        ball.set_z_index(1)
        point_0.set_z_index(1)
        point_1.set_z_index(1)
        point_2.set_z_index(1)
        
        #animations
        self.play(
            FadeIn(ramp), FadeIn(v_0),
            FadeIn(ball), FadeIn(t1)
        )
        self.play(Wait(1))
        self.play(
            Create(trajectory),
            FadeOut(t1),
        )
        
        #saving initial state
        trajectory.save_state()
        v_0.save_state()
        
        self.play(Wait(1))
        self.play(
            Transform(trajectory, trajectory_1),
            Transform(v_0, v_1),
            run_time = 1.5
        )
        self.play(Wait(1))
        self.play(
            Transform(trajectory, trajectory_2),
            Transform(v_0, v_2),
            run_time = 1.5
        )
        self.play(Wait(1))
        self.play(
            Restore(trajectory),
            FadeOut(v_0),
            Create(trajectory_1),
            Create(trajectory_2),
            run_time = 1.5
        )
        self.play(Wait(1))
        self.play(
            Create(delta_x), Create(delta_y),
            Create(delta_x_1), Create(delta_y_1),
            Create(delta_x_2), Create(delta_y_2),
            Write(t72), Write(t82)
        )
        self.play(Wait(1))
        self.play(Succession(
            Write(t2), Indicate(t2)
        ), run_time = 2)
        self.play(Wait(1))
        self.play(
            Create(point_0), Create(point_1), Create(point_2)
        )
        self.play(Wait(1))
        self.play(Create(connection))
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])

'''
Final equations
'''
class s6(Scene):
    def construct(self):
        #intializing MathTex from where we left off in s2
        MathTex.set_default(font_size = 70)
        buff_size = 0.5
        
        t1 = MathTex(r"d = \sqrt{x^2 + y^2}")
        t2 = MathTex(r"x = v_0t")
        t3 = MathTex(r"y = -\frac{g}{2}t^2")
        t4 = MathTex(r"v_y = -gt")
        t5 = MathTex(r"v_y^2 = -2gy")
        t6 = MathTex(r"y = -x tan \theta")
        
        group1 = VGroup(t1, t2, t3, t4, t5)
        #possible positions for the equations to be
        positions = np.array([[[-3,2.25,0], [3,2.25,0]],
                             [[-3,0.75,0], [3,0.75,0]],
                             [[-3,-0.75,0], [3,-0.75,0]],
                             [[-3,-2.25,0], [3,-2.25,0]]])
        dividing_line = Line([0,3.5,0], [0,-3.5, 0]).set_stroke(width = 4)

        t1.move_to(positions[0,1])
        t2.move_to(positions[1,1])
        t3.move_to(positions[2,1])
        t4.move_to(positions[0,0])
        t5.move_to(positions[1,0])

        #animation
        self.play(Write(t6))
        self.play(Wait(1))
        self.play(FadeOut(t6))
        self.play(Wait(1))
        self.play(
            FadeIn(group1),
            FadeIn(dividing_line)
        )
        self.play(Wait(1))
        t6.move_to(positions[3,1])
        self.play(FadeIn(t6))
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])
        self.play(Wait(1))

'''
generalized equations
'''
class s7(Scene):
    def construct(self):
        MathTex.set_default(font_size = 70)
        buff_size = 0.5
        
        #final answers
        t1 = MathTex(r"x = \frac{2 v_0^2 tan \theta}{g}")
        t2 = MathTex(r"y = - \frac{2 v_0^2 tan^2 \theta}{g}")
        t3 = MathTex(r"d = x \sqrt{1 + tan^2 \theta}")
        
        #general equations
        t4 = MathTex(r"x = \frac{2 v_0^2}{g} cos \phi (cos \phi tan \theta \pm sin \phi)")
        t5 = MathTex(r"y = - \frac{2 v_0^2}{g} cos \phi (cos \phi tan \theta \pm sin \phi) tan \theta")
        
        group1 = VGroup(t1, t2, t3).arrange(DOWN, buff_size)
        group2 = VGroup(t4, t5).arrange(DOWN, buff_size)
        
        self.play(Write(group1), run_time=2)
        self.play(Wait(1))
        self.play(FadeOut(group1))
        self.play(Wait(1))
        self.play(Write(group2), run_time = 2)
        self.play(Wait(1))
        self.play(FadeOut(group2))
        