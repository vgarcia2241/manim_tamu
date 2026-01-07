from manim import *
import numpy as np

MathTex.set_default(font_size = 80)
fontsize = 70
line_weight = 0.7
width = 6 #for ramp

class s1(Scene):
    def Check_Point(self, text): #create obj with text and box for checklist
        box = Square(0.7)
        t1 = Tex(text)
        g_return = VGroup(box,t1).arrange(RIGHT, buff = 0.5)
        return g_return
        
    def Check(self, bol): #create check or X, depends on true or false
        if(bol): #return check
            line1 = Line([-0.5,0,0], [0,-0.5,0])
            line2 = Line([0,-0.5,0],[1,1,0])
            g_return = VGroup(line1, line2).scale(0.35).set_stroke(width = 5)
            return g_return
        else: #return X
            line1 = Line([-1,1,0],[1,-1,0])
            line2 = Line([-1,-1,0],[1,1,0])
            g_return = VGroup(line1, line2).scale(0.3).set_stroke(width = 5)
            return g_return
             
    def construct(self):
        rotationCenter = [-3,-3,0]
        angle = 30
        base_line = Line([-width/2.0,-3,0], [width/2.0,-3,0])
        slope_line = Line([-width/2.0,-3,0], [width/2.0,-3,0])
        square = Square(side_length=1).align_to(slope_line, DOWN)
        square.shift(slope_line.point_from_proportion(0.25)- slope_line.point_from_proportion(0.0))
        s_dot = Dot(square.get_center()).set_z_index(1)
        s_dot.rotate(angle*DEGREES,about_point=rotationCenter)
        sg = VGroup(square, slope_line)
        sg.rotate(angle*DEGREES,about_point=rotationCenter)
        angle1 = Angle(base_line, slope_line, radius=2, other_angle=False)
        angle1_tex = MathTex(r"\theta", color = YELLOW, font_size = fontsize).move_to(
            Angle(base_line, slope_line, radius=0.5 + 2*LARGE_BUFF, other_angle=False).point_from_proportion(0.5)
        )
        mass = MathTex(r"m", font_size = fontsize, color = YELLOW).next_to(square, UL).shift([0,-0.55,0])
        
        #checklist
        t1 = Tex(r"Checklist:")
        t_list = ["Gravity","Normal","Friction","Tension","Spring","Other","Motion"]
        g_list = VGroup(t1)
        for i in range(0,7):
            g_list.add(self.Check_Point(t_list[i]))
        g_list.arrange(DOWN, center=False, aligned_edge = LEFT, buff = 0.4).scale(0.8)
        
        g1 = VGroup(base_line, slope_line, angle1, angle1_tex, square, s_dot, mass)
        self.play(Create(g1))
        self.wait()
        g3 = VGroup(g1,g_list)
        self.play(FadeIn(g_list), g3.animate.arrange(RIGHT, buff = 1.5))
        
        pos_list = []
        bol_list = [True,True,True,False,False,False,True]
        g_check = VGroup()
        for i in range(0,7):
            pos_list.append(g_list[i+1][0].get_center())
            g_check.add(self.Check(bol_list[i]).move_to(pos_list[i]))        
        
        gravity = Arrow(square.get_center(), square.get_center() + 2*DOWN, buff=0, color = BLUE)
        f_g = MathTex(r"F_g", font_size = fontsize, color = BLUE).next_to(gravity, RIGHT)
        n_force = Arrow(square.get_center(), square.get_center() + [-2*(1 - angle / 90.0 + 0.15)*np.sin(angle*DEGREES),2*(1 - angle / 90.0 + 0.15)*np.cos(angle*DEGREES),0], buff=0, color = GREEN)
        f_n = MathTex(r"F_n", font_size = fontsize, color = GREEN).next_to(n_force, UR, buff = -0.25)
        friction = Arrow(square.get_center(), square.get_center() + [2*(1 - angle / 90.0 + 0.15)*np.cos(angle*DEGREES),2*(1 - angle / 90.0 + 0.15)*np.sin(angle*DEGREES),0], buff=0, color = RED)
        f_f = MathTex(r"F_f", font_size = fontsize, color = RED).next_to(friction, UR, buff = 0)
        acceleration = Arrow(square.get_center() - [(angle / 90.0 + 0.4)*np.cos(angle*DEGREES),(angle / 90.0 + 0.4)*np.sin(angle*DEGREES),0], square.get_center() - [3*(angle / 90.0 + 0.4)*np.cos(angle*DEGREES),3*(angle / 90.0 + 0.4)*np.sin(angle*DEGREES),0], buff=0, color = ORANGE)
        f_a = MathTex(r"a", font_size = fontsize, color = ORANGE).next_to(acceleration, LEFT)
        
        self.wait()
        self.play(Indicate(mass))
        self.wait()
        list1 = VGroup(gravity, n_force, friction)
        list2 = VGroup(f_g, f_n, f_f)
        for i in range(0,3):
            self.play(Create(g_check[i]), run_time = 0.5)
            self.wait()
            self.play(Create(list1[i]), Write(list2[i]))
            self.wait()
        for i in range(3,6):
            self.play(Create(g_check[i]), run_time = 0.5)
            self.wait()
        self.play(Create(g_check[6]), run_time = 0.5)
        self.wait()
        self.play(Create(acceleration), Write(f_a))
        self.wait()
        self.play(Succession(Indicate(f_g), Indicate(f_f), run_time = 3))
        self.wait()
        
        fade_list = VGroup(g_list, g_check)
        self.play(FadeOut(fade_list))
        self.wait()
        
        #flat case
        line2 = base_line.copy()
        square2 = Square(side_length=1).move_to(base_line.point_from_proportion(0.5)).align_to(line2, DOWN)
        mass2 = mass.copy().next_to(square2, LEFT, buff = 0.35)
        dot2 = s_dot.copy().move_to(square2.get_center())
        g_slope = Group()
        for i in self.mobjects:
            g_slope.add(i)
        g_flat = VGroup(line2, square2, mass2, dot2).align_to(g_slope).to_edge(RIGHT, buff = 0.5)      
        gravity2 = Arrow(square2.get_center(), square2.get_center() + 2*DOWN, buff=0, color = BLUE)
        f_g2 = MathTex(r"F_g", font_size = fontsize, color = BLUE).next_to(gravity2.get_end(), RIGHT)
        n_force2 = Arrow(square2.get_center(), square2.get_center() + 2*UP, buff=0, color = GREEN)
        f_n2 = MathTex(r"F_n", font_size = fontsize, color = GREEN).next_to(n_force2.get_end(), RIGHT)
        
        self.play(Create(g_flat), g_slope.animate.to_edge(LEFT, buff = 0.5))
        self.wait()
        self.play(Create(gravity2), Write(f_g2))
        self.wait()
        self.play(Create(n_force2), Write(f_n2))
        self.wait()

        self.play(*[FadeOut(i) for i in self.mobjects])
        

class s2(Scene):
    def construct(self):
        t1 = MathTex(r"\sum F_{net}")
        t1_1 = MathTex(r"\sum F_{net} = m \vec{a}")
        
        t2 = MathTex(r"\sum F_y:~F_N - F_{g,y}")
        t2_1 = MathTex(r"\sum F_y:~F_N - F_{g,y} = m a_y")
        t2_2 = MathTex(r"\sum F_y:~F_N - F_{g,y} = 0")
        t3 = MathTex(r"\sum F_x:~F_{g,x} - F_f")
        t3_1 = MathTex(r"\sum F_x:~F_{g,x} - F_f = ma_x")
        g1 = VGroup(t3,t2).arrange(DOWN, buff = 1.5)
        t3_1.move_to(t3)
        t2_1.move_to(t2)
        t2_2.move_to(t2)
        
        self.play(Write(t1))
        self.wait()
        self.play(TransformMatchingShapes(t1,t1_1))
        self.wait()
        self.play(FadeOut(t1_1))
        self.wait()
        self.play(Write(g1))
        self.wait()
        self.play(FadeTransformPieces(t3, t3_1))
        self.wait()
        self.play(FadeTransformPieces(t2,t2_1))
        self.wait()
        self.play(FadeTransformPieces(t2_1, t2_2))
        
        self.play(*[FadeOut(i) for i in self.mobjects])
        

class s3(Scene):
    def construct(self):
        rotationCenter = [-3,-3,0]
        angle = 30
        base_line = Line([-width/2.0,-3,0], [width/2.0,-3,0])
        slope_line = Line([-width/2.0,-3,0], [width/2.0,-3,0])
        square = Square(side_length=1).align_to(slope_line, DOWN)
        square.shift(slope_line.point_from_proportion(0.25)- slope_line.point_from_proportion(0.0))
        s_dot = Dot(square.get_center()).set_z_index(1)
        s_dot.rotate(angle*DEGREES,about_point=rotationCenter)
        sg = VGroup(square, slope_line)
        sg.rotate(angle*DEGREES,about_point=rotationCenter)
        angle1 = Angle(base_line, slope_line, radius=2, other_angle=False)
        angle1_tex = MathTex(r"\theta", color = YELLOW, font_size = fontsize).move_to(
            Angle(base_line, slope_line, radius=0.5 + 2*LARGE_BUFF, other_angle=False).point_from_proportion(0.5)
        )
        gravity = Arrow(square.get_center(), square.get_center() + 2*DOWN, buff=0, color = BLUE)
        f_g = MathTex(r"F_g", font_size = fontsize, color = BLUE).next_to(gravity, RIGHT)
        n_force = Arrow(square.get_center(), square.get_center() + [-2*(1 - angle / 90.0 + 0.15)*np.sin(angle*DEGREES),2*(1 - angle / 90.0 + 0.15)*np.cos(angle*DEGREES),0], buff=0, color = GREEN)
        f_n = MathTex(r"F_n", font_size = fontsize, color = GREEN).next_to(n_force, UR, buff = -0.25)
        friction = Arrow(square.get_center(), square.get_center() + [2*(1 - angle / 90.0 + 0.15)*np.cos(angle*DEGREES),2*(1 - angle / 90.0 + 0.15)*np.sin(angle*DEGREES),0], buff=0, color = RED)
        f_f = MathTex(r"F_f", font_size = fontsize, color = RED).next_to(friction, UR, buff = 0)
        acceleration = Arrow(square.get_center() - [(angle / 90.0 + 0.4)*np.cos(angle*DEGREES),(angle / 90.0 + 0.4)*np.sin(angle*DEGREES),0], square.get_center() - [3*(angle / 90.0 + 0.4)*np.cos(angle*DEGREES),3*(angle / 90.0 + 0.4)*np.sin(angle*DEGREES),0], buff=0, color = ORANGE)
        f_a = MathTex(r"a", font_size = fontsize, color = ORANGE).next_to(acceleration, LEFT)
        g_force = Group(gravity, f_g, n_force, f_n, friction, f_f, acceleration, f_a)
        gravity_full = Arrow(square.get_center(), square.get_center() + [0,(base_line.get_y() - square.get_center()[1]),0], buff=0, color = BLUE)
        #fixing angle to be inside triangle######################
        intersection = line_intersection([slope_line.get_start(), slope_line.get_end()], [gravity_full.get_start(), gravity_full.get_end()])
        line1 = Line(intersection, intersection - slope_line.get_vector(), color = RED)
        line2 = Line(intersection, intersection + gravity.get_vector(), color = RED)
        angle2 = Angle(line1, line2, radius = 0.75, other_angle = False).set_z_index(-1)
        angle2_tex = MathTex(r"\phi", color = YELLOW, font_size = fontsize).move_to(
            Angle(line1, line2, radius= 1 + 1*MED_SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        )
        #transformation for angle1
        angle3 = Angle(base_line, slope_line, radius=1, other_angle=False)
        angle3_tex = MathTex(r"\theta", color = YELLOW, font_size = fontsize).move_to(
            Angle(base_line, slope_line, radius= 1.2 + 1*MED_SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        )
        
        #axis
        axis_center = [-5,-2,0]
        x_axis = Arrow(axis_center, axis_center + 1.5*RIGHT, buff = 0)
        x_axis_tex = MathTex(r"x", font_size = fontsize).next_to(x_axis, RIGHT)
        y_axis = Arrow(axis_center, axis_center + 1.5*UP, buff = 0)
        y_axis_tex = MathTex(r"y", font_size = fontsize).next_to(y_axis, UP)
        g_axis = VGroup(x_axis,y_axis)
        
        #right angle and vertical
        r_angle = Square(side_length= 0.5).move_to(intersection + [-0.5/2,-intersection[1] + base_line.get_y() + 0.5/2,0]).set_z_index(-1)
        vertical = DashedLine(square.get_center(), square.get_center() - [-2*(1 - angle / 90.0 + 0.15)*np.sin(angle*DEGREES),2*(1 - angle / 90.0 + 0.15)*np.cos(angle*DEGREES),0], buff=0)
        angle4 = Angle(gravity, vertical, radius = 1.33).set_z_index(-1)
        angle4_tex = MathTex(r"\theta", font_size = fontsize, color = YELLOW).move_to(
            Angle(gravity, vertical, radius= 1.6 + 1*MED_SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        )
        r_angle2 = Square(side_length = 0.3).align_to(vertical)
        
        g1 = VGroup(base_line, sg, s_dot, angle1, angle1_tex)
        
        self.play(FadeIn(g1), FadeIn(g_force))
        self.wait()
        self.play(Create(g_axis), Write(x_axis_tex), Write(y_axis_tex))
        self.wait()
        self.play(FadeOut(x_axis_tex), FadeOut(y_axis_tex), run_time = 0.3)
        self.play(g_axis.animate.rotate(angle*DEGREES, about_point = axis_center))
        x_axis_tex.next_to(x_axis, UR, buff = 0.15)
        y_axis_tex.next_to(y_axis, UL, buff = 0.1)
        self.play(FadeIn(x_axis_tex), FadeIn(y_axis_tex), run_time = 0.3)
        self.wait()
        self.play(Indicate(f_g), run_time = 1.5)
        self.wait()
        self.play(FadeOut(g_force), Create(gravity_full))
        self.wait()
        self.play(
            Create(angle2), Write(angle2_tex),
            TransformMatchingShapes(angle1, angle3),
            TransformMatchingShapes(angle1_tex, angle3_tex),
            Create(r_angle)
            )
        self.wait()
        
        
        t1 = MathTex(r"\theta + \phi + 90^{\circ} = 180^{\circ}", font_size = fontsize).to_edge(UP, buff = 1.5)
        t2 = MathTex(r"\theta + \phi = 90^{\circ}", font_size = fontsize).move_to(t1)
        t3 = MathTex(r"F_{g,y} = F_gcos(\theta)", font_size = fontsize)
        t4 = MathTex(r"F_{g,x} = F_gsin(\theta)", font_size = fontsize)
        g2 = VGroup(t3,t4).arrange(DOWN).to_edge(UP, buff = 1)

        self.play(Write(t1))
        self.wait()
        self.play(TransformMatchingShapes(t1, t2))
        self.wait()
        self.play(Create(vertical), Create(angle4), Write(angle4_tex))
        self.wait()
        self.play(FadeOut(t2))
        self.wait()
        self.play(Write(t3))
        self.wait()
        self.play(Write(t4))
        self.wait()
        
        self.play(*[FadeOut(i) for i in self.mobjects])
        
class s4(Scene):
    def construct(self):
        MathTex.set_default(font_size = fontsize)
        
        t1 = MathTex(r"\Sigma F_y = F_N - F_{g,y} = 0")
        t1_1 = MathTex(r"F_N = F_{g,y} = mgcos(\theta)")
        t2 = MathTex(r"\Sigma F_x = F_{g,x} - F_f = ma_x")
        t2_1 = MathTex(r"a_x = \frac{F_{g,x} - F_f}{m}")
        t2_2 = MathTex(r"a_x = \frac{mgsin(\theta) - \mu mgcos(\theta)}{m}")
        t2_3 = MathTex(r"a_x = g(sin(\theta) - \mu cos(\theta))")
        
        g1 = VGroup(t1, t2).arrange(DOWN, buff = 1.5)
        t1_1.move_to(t1)
        t2_1.move_to(t2)
        t2_2.move_to(t2)
        t2_3.move_to(t2)
        
        self.play(Write(t1))
        self.wait()
        self.play(TransformMatchingShapes(t1, t1_1))
        self.wait()
        self.play(Write(t2))
        self.wait()
        self.play(TransformMatchingShapes(t2,t2_1))
        self.wait()
        self.play(TransformMatchingShapes(t2_1, t2_2))
        self.wait()
        self.play(TransformMatchingShapes(t2_2, t2_3))
        self.wait()
        
        self.play(*[FadeOut(i) for i in self.mobjects])

class RampTest(Scene):
    def construct(self):
        rotationCenter = [-3,-3,0]
        thetaTracker = ValueTracker(30)
        baseLine = Line([-3,-3,0],[3,-3,0])
        slopeLine = Line([-3,-3,0],[3,-3,0])
        refLine = baseLine.copy()

        square = Square(side_length=1).align_to(slopeLine,DOWN)
        square.shift(slopeLine.point_from_proportion(0.25)- slopeLine.point_from_proportion(0.0))
        sqCenter = square.get_center()
        print(sqCenter)
        sqDot = Dot(sqCenter).set_z_index(1)
        sqDotRef = sqDot.copy()
        sg=VGroup(square,slopeLine)
        sgRef = sg.copy()

        #slopeLine.rotate(thetaTracker.get_value()*DEGREES,about_point=rotationCenter)
        sg.rotate(thetaTracker.get_value()*DEGREES,about_point=rotationCenter)
        sqDot.rotate(thetaTracker.get_value()*DEGREES,about_point=rotationCenter)
        #a = Angle(baseLine, sg, radius=0.5,other_angle=False)
        a = Angle(baseLine, slopeLine, radius=2, other_angle=False)
        tex = MathTex(r"\theta", color = YELLOW, font_size = fontsize).move_to(
            #Angle(baseLine,sg,radius=0.5+3*SMALL_BUFF,other_angle=False).point_from_proportion(0.5)
            Angle(baseLine, slopeLine, radius=0.5 + 2*LARGE_BUFF, other_angle=False).point_from_proportion(0.5)
        )

        ramp_direction = np.reciprocal(slopeLine.get_unit_vector())
        ramp_direction[2] = 0
        ramp_direction[0] *= -1
        ramp_direction = ramp_direction / np.linalg.norm(ramp_direction)
        friction = Arrow(square.get_center(), square.get_center() + 2*(slopeLine.get_unit_vector() / np.linalg.norm(slopeLine.get_unit_vector())), buff = 0)

        mass = MathTex(r"m", font_size = fontsize, color = YELLOW).next_to(square, LEFT)
        unknown_motion = Arrow(square.get_center(), square.get_center() - [2*np.cos(thetaTracker.get_value()*DEGREES),2*np.sin(thetaTracker.get_value()*DEGREES),0], buff=0, color = YELLOW)
        unknown_tex = MathTex(r"\text{?}", font_size = fontsize, color = YELLOW).next_to(unknown_motion, UP, buff = 0).shift([-0.35,-0.3,0])
        
        
        gravity = always_redraw(
            lambda : Arrow(square.get_center(), square.get_center() + 2*DOWN, buff=0, color = BLUE)
        )
        f_g = always_redraw(
            lambda: MathTex(r"F_g", font_size = fontsize, color = BLUE).next_to(gravity, RIGHT)
        )
        n_force = always_redraw(
            lambda: Arrow(square.get_center(), square.get_center() + [-2*(1 - thetaTracker.get_value() / 90.0 + 0.15)*np.sin(thetaTracker.get_value()*DEGREES),2*(1 - thetaTracker.get_value() / 90.0 + 0.15)*np.cos(thetaTracker.get_value()*DEGREES),0], buff=0, color = GREEN)
        )
        f_n = always_redraw(
            lambda: MathTex(r"F_n", font_size = fontsize, color = GREEN).next_to(n_force, LEFT)
        )
        friction = always_redraw(
            lambda: Arrow(square.get_center(), square.get_center() + [2*(1 - thetaTracker.get_value() / 90.0 + 0.15)*np.cos(thetaTracker.get_value()*DEGREES),2*(1 - thetaTracker.get_value() / 90.0 + 0.15)*np.sin(thetaTracker.get_value()*DEGREES),0], buff=0, color = RED)
        )
        f_f = always_redraw(
            lambda: MathTex(r"F_f", font_size = fontsize, color = RED).next_to(friction, RIGHT)
        )
        acceleration = always_redraw(
            lambda: Arrow(square.get_center() - [(1)*np.cos(thetaTracker.get_value()*DEGREES),(1)*np.sin(thetaTracker.get_value()*DEGREES),0], square.get_center() - [3.5*(thetaTracker.get_value() / 90.0 + 0.4)*np.cos(thetaTracker.get_value()*DEGREES),3.5*(thetaTracker.get_value() / 90.0 + 0.4)*np.sin(thetaTracker.get_value()*DEGREES),0], buff=0, color = ORANGE)
        )
        f_a = always_redraw(
            lambda: MathTex(r"a", font_size = fontsize, color = YELLOW).next_to(acceleration, LEFT)
        )        

        self.wait()
        g1 = VGroup(baseLine, sqDot, sg,)
        g2 = VGroup(gravity, f_g, n_force, f_n, friction, f_f, acceleration, f_a)
        self.play(FadeIn(g1), FadeIn(a), FadeIn(tex))
        slopeLine.add_updater(
            lambda x: x.become(refLine.copy()).rotate(
                thetaTracker.get_value()*DEGREES, about_point=rotationCenter
            )
        )
        sg.add_updater(
            lambda x: x.become(sgRef.copy()).rotate(
                thetaTracker.get_value()*DEGREES, about_point=rotationCenter
            )
        )
        sqDot.add_updater(
            lambda x: x.become(sqDotRef.copy()).rotate(
                thetaTracker.get_value()*DEGREES, about_point=rotationCenter
            )
        )
        a.add_updater(
            lambda x: x.become(Angle(baseLine, slopeLine, radius=2, other_angle=False))
        )
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    baseLine, slopeLine, radius = 0.5 + 2*LARGE_BUFF, other_angle = False
                ).point_from_proportion(0.5)
            )
        )
        self.wait()
        self.play(FadeIn(g2))
        self.wait()
        self.play(thetaTracker.animate.set_value(20))
        self.wait()
        self.play(thetaTracker.animate.set_value(45))
        self.wait()
        self.play(thetaTracker.animate.set_value(15))
        
        #self.play(*[FadeOut(i) for i in self.mobjects])