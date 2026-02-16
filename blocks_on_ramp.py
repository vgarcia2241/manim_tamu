from manim import *
import numpy as np

MathTex.set_default(font_size = 70)
MathTex.set_default(stroke_width=2.5)
#Tex.set_default(font_size=60*(1/0.3))
Tex.set_default(stroke_width = 1)

def Outline(self,obj):
    '''
    function which takes in some Mobject and return an outline-only version
    '''
    temp = obj.copy()
    temp.set_fill(color=None, opacity=0).set_stroke(width=DEFAULT_STROKE_WIDTH, color=WHITE)
    return temp

def Check_Point(self, text): #create obj with text and box for checklist
    box = Square(0.7)
    t1 = Tex(text)
    g_return = VGroup(box,t1).arrange(RIGHT, buff = 0.2)
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

class s1(Scene): #Initial scene        
    def construct(self):
        #ramp initialization
        ramp = Polygon([-3.5,-3,0],[-3.5,1,0],[3.5,-3,0], color=GRAY_C).set_stroke(width=0.1).set_fill(GRAY_C,opacity=1)
        ramp_line = Line(ramp.get_critical_point([-1,1,0]), ramp.get_critical_point([1,-1,0]))
        ramp_direction = np.reciprocal(ramp_line.get_unit_vector())
        ramp_direction[2] = 0
        ramp_direction[1] *= -1
        ramp_direction = ramp_direction / np.linalg.norm(ramp_direction)
        
        normal = Arrow(ramp_line.point_from_proportion(0.5), ramp_line.point_from_proportion(0.5)+3*ramp_direction, buff=0)
        
        #setting up blocks
        block_dim = [1,4,1,2] #setting dimensions here should allow for easy size changing
        block2 = Rectangle(BLUE, block_dim[0], block_dim[1]).set_stroke(width=0.1).set_fill(BLUE, opacity=1)
        block2.rotate(ramp_line.get_angle()).move_to(ramp_line.point_from_proportion(0.65)).shift(ramp_direction*block_dim[0]/2)
        block1 = Rectangle(RED, block_dim[2], block_dim[3]).set_stroke(width=0.1).set_fill(RED, opacity=1)
        block1.rotate(ramp_line.get_angle()).move_to(ramp_line.point_from_proportion(0.65)).shift(ramp_direction*((2*block_dim[0]+block_dim[2])/2))
        
        #creating pulley system
        disk = Circle(0.5, GRAY_C).set_stroke(width=0.1).set_fill(GRAY_C,opacity=1).set_z_index(0.1)
        disk.rotate(ramp_line.get_angle()).move_to(ramp_line.point_from_proportion(0.01)).shift(ramp_direction*block_dim[0])
        stick = Line(ramp_line.point_from_proportion(0.01), disk.get_center(), color = GRAY_E).set_stroke(width=9).set_z_index(0.2)
        #connection points of pulley
        pointB = disk.point_from_proportion(0.75)
        pointA = disk.point_from_proportion(0.25)
        #conection points to blocks
        p2 =  (0.5*block_dim[0] + block_dim[1]) / (2*block_dim[0] + 2*block_dim[1])
        p1 = (0.5*block_dim[2] + block_dim[3]) / (2*block_dim[2] + 2*block_dim[3])
        point2 = block2.point_from_proportion(p2)
        point1 = block1.point_from_proportion(p1)
        #pulley lines
        line2 = Line(point2, pointB)
        line1 = Line(point1,pointA)
        
        #creating labels/text
        MathTex.set_default(color=YELLOW)
        mass2 = MathTex(r"m_2").next_to(block2, DR).shift([0,0.75,0])
        mass1 = MathTex(r"m_1").next_to(block1, RIGHT)
        mu2 = MathTex(r"\mu_2").move_to(ramp_line.point_from_proportion(0.65)).rotate(ramp_line.get_angle())
        mu1 = MathTex(r"\mu_1").move_to(block2.point_from_proportion(0.2)).rotate(ramp_line.get_angle())
        theta = MathTex(r"\theta").move_to(ramp.get_critical_point([1,-1,0])).shift([-1.7,0.45,0])
        theta_line = Line(ramp.get_critical_point([1,-1,0]), ramp.get_critical_point([-1,-1,0]))
        theta_angle = Angle(theta_line, theta_line.copy().rotate(ramp_line.get_angle(), about_point=theta_line.get_right()), radius=1.25, other_angle=True, color=YELLOW)
        acceleration = Tex(r"What is the magnitude of\\ acceleration of the top block?", color=WHITE).to_edge(UP)
        motion = Arrow(block2.point_from_proportion(0.95), block2.point_from_proportion(0.95)+1.5*ramp_line.get_unit_vector(), buff=0, color=BLUE).shift([0,-0.75,0])
        motion2 = Arrow(block1.point_from_proportion(p1), block1.point_from_proportion(p1)-1.5*ramp_line.get_unit_vector(), buff=0, color=WHITE)
        
        print(ramp_line.get_unit_vector())
        
        #Fade in setup
        original = VGroup(ramp, block1, block2, disk, stick, line2, line1)
        self.play(FadeIn(original), run_time=1.5)
        self.wait()
        
        #creating outlined objects and grabbing current ones
        outlined = VGroup()
        for i in original:
            outlined.add(Outline(self,i))
            
        ''' showcase of changing to outlined appearance
        self.play(FadeOut(original), FadeIn(outlined))
        self.wait()
        self.play(TransformMatchingShapes(outlined[0], original[0]))
        self.play(TransformMatchingShapes(outlined,original))
        '''
        
        self.play(Write(mass2))
        self.wait()
        self.play(Write(theta), Create(theta_angle))
        self.wait()
        self.play(Write(mu2))
        self.wait()
        self.play(Write(mass1))
        self.wait()
        self.play(Write(mu1))
        self.wait()
        self.play(ShowPassingFlash(line2.copy().set_color(YELLOW), time_width = 0.35, run_time=2),
                  ShowPassingFlash(line1.copy().set_color(YELLOW), time_width = 0.35, run_time=2))
        self.play(Indicate(disk), run_time=1.5)
        self.wait()
        
        g1 = Group()
        for i in self.mobjects:
            g1.add(i)
        self.play(g1.animate.shift([0,-0.75,0]),
                  Write(acceleration))    
        self.wait()
        
        self.play(FadeOut(mass2), FadeOut(mass1))
        self.play(Create(motion))
        
        self.wait()
        
        g2 = VGroup(mu2,mu1,motion,acceleration, theta,theta_angle)
        self.play(
            FadeOut(g2),
            original.animate.shift([0,0.75,0])
        )
        self.wait(2)
        
#_______________________________________________________________________
# end of paragraph 1 ###################################################
        
        for i in original:
            self.play(Indicate(i, scale_factor=1.1), run_time=0.7)
        self.wait()

        val1 = ValueTracker(0)
        val2 = ValueTracker(0)
        friction2 = always_redraw(
            lambda: Arrow(ramp_line.point_from_proportion(0.65), ramp_line.point_from_proportion(0.65) + val1.get_value()*ramp_line.get_unit_vector())
        )
        friction1 = always_redraw(
            lambda: Arrow(block2.point_from_proportion(0.2), block2.point_from_proportion(0.2) - val1.get_value()*ramp_line.get_unit_vector())
        )
        norm1 = always_redraw(
            lambda: Arrow(block2.point_from_proportion(0.16), block2.point_from_proportion(0.16) - ramp_direction*val2.get_value(), buff=0)
        )
        norm1_1 = always_redraw(
            lambda: Arrow(block2.point_from_proportion(0.2), block2.point_from_proportion(0.2) + ramp_direction*val2.get_value(), buff=0)
        )
        norm2 = always_redraw(
            lambda: Arrow(ramp_line.point_from_proportion(0.65), ramp_line.point_from_proportion(0.65) + ramp_direction*val2.get_value(), buff=0)
        )
        norm2_1 = always_redraw(
            lambda: Arrow(ramp_line.point_from_proportion(0.69), ramp_line.point_from_proportion(0.69) - ramp_direction*val2.get_value(), buff=0)
        )
        
        self.add(friction1, friction2, norm1, norm1_1, norm2, norm2_1)
        self.play(val1.animate.set_value(3))
        self.wait(0.3)
        self.play(val1.animate.set_value(-2))
        self.wait(0.3)
        self.play(val1.animate.set_value(0))
        self.wait(0.3)
        self.play(val2.animate.set_value(0.75))
        self.wait()
        self.play(val2.animate.set_value(0))
        self.wait(2)
        
#________________________________________________
# end of paragraph 2

'''
Attempting to zoom into block1 (red)
'''
class s2(MovingCameraScene):
    def construct(self):
        #ramp initialization
        ramp = Polygon([-3.5,-3,0],[-3.5,1,0],[3.5,-3,0], color=GRAY_C).set_stroke(width=0.1).set_fill(GRAY_C,opacity=1)
        ramp_line = Line(ramp.get_critical_point([-1,1,0]), ramp.get_critical_point([1,-1,0]))
        ramp_direction = np.reciprocal(ramp_line.get_unit_vector())
        ramp_direction[2] = 0
        ramp_direction[1] *= -1
        ramp_direction = ramp_direction / np.linalg.norm(ramp_direction)
        
        #setting up blocks
        block_dim = [1,4,1,2] #setting dimensions here should allow for easy size changing
        block2 = Rectangle(BLUE, block_dim[0], block_dim[1]).set_stroke(width=0.1).set_fill(BLUE, opacity=1)
        block2.rotate(ramp_line.get_angle()).move_to(ramp_line.point_from_proportion(0.65)).shift(ramp_direction*block_dim[0]/2)
        block1 = Rectangle(RED, block_dim[2], block_dim[3]).set_stroke(width=0.1).set_fill(RED, opacity=1)
        block1.rotate(ramp_line.get_angle()).move_to(ramp_line.point_from_proportion(0.65)).shift(ramp_direction*((2*block_dim[0]+block_dim[2])/2))
        
        #creating pulley system
        disk = Circle(0.5, GRAY_C).set_stroke(width=0.1).set_fill(GRAY_C,opacity=1).set_z_index(0.1)
        disk.rotate(ramp_line.get_angle()).move_to(ramp_line.point_from_proportion(0.01)).shift(ramp_direction*block_dim[0])
        stick = Line(ramp_line.point_from_proportion(0.01), disk.get_center(), color = GRAY_E).set_stroke(width=9).set_z_index(0.2)
        #connection points of pulley
        pointB = disk.point_from_proportion(0.75)
        pointA = disk.point_from_proportion(0.25)
        #conection points to blocks
        p2 =  (0.5*block_dim[0] + block_dim[1]) / (2*block_dim[0] + 2*block_dim[1])
        p1 = (0.5*block_dim[2] + block_dim[3]) / (2*block_dim[2] + 2*block_dim[3])
        point2 = block2.point_from_proportion(p2)
        point1 = block1.point_from_proportion(p1)
        #pulley lines
        line2 = Line(point2, pointB)
        line1 = Line(point1,pointA)
        
        #block1 force/motion lines
        MathTex.set_default(font_size = 60)
        MathTex.set_default(stroke_width=1)
        motion1 = Arrow(block1.point_from_proportion(p1), block1.point_from_proportion(p1)-1*ramp_line.get_unit_vector(), buff=0, color=WHITE)
        motion1_lab = MathTex(r"a", color=WHITE).next_to(motion1, UP, buff=-0.05).shift([0.3,0,0])
        gravity = Arrow(block1.get_center(), block1.get_center() + 1.5*DOWN, buff=0, color = BLUE)
        f_g = MathTex(r"F_g", color = BLUE, font_size=40).next_to(gravity, LEFT, buff=0.1)
        normal = Arrow(block1.get_center(), block1.get_center()+1.5*ramp_direction, buff=0, color=GREEN)
        f_n = MathTex(r"F_n", font_size = 40, color = GREEN).next_to(normal, UL, buff = -0.25)
        contact1 = Line(block1.point_from_proportion(0.5),block1.point_from_proportion(0.5 + (block_dim[3]/(2*block_dim[2] + 2*block_dim[3]))), buff=0)
        frictionA = always_redraw(
            lambda: Arrow(block1.get_center(), block1.get_center() + 1.5*ramp_line.get_unit_vector(), buff=0, color=YELLOW)
        )
        frictionB = always_redraw(
            lambda: Arrow(block1.get_center(), block1.get_center() - 1.5*ramp_line.get_unit_vector(), buff=0, color=YELLOW)
        )
        f_f = always_redraw(
            lambda: MathTex(r"F_f", color=YELLOW, font_size = 40).move_to(block1.get_center()).shift(0.25*ramp_direction)
        )
        tension = motion1.copy().set_color(ORANGE)
        f_t = MathTex(r"F_T", font_size=40, color=ORANGE).next_to(tension, UP, buff=-0.05).shift([0.3,0,0])
        
        #checklist
        t1 = Tex(r"Checklist:", font_size=50)
        t_list = ["Gravity","Normal","Friction","Tension","Spring","Other","Motion"]
        g_list = VGroup()
        for i in range(0,7):
            g_list.add(Check_Point(self, t_list[i]))
        g_list.arrange_in_grid(4,2, flow_order='dr', cell_alignment=[-1,0,0], buff = 0.4).scale(0.5).next_to(block1,RIGHT, buff = 0.5)
        pos_list = []
        bol_list = [True,True,True,True,False,False,True]
        g_check = VGroup()
        for i in range(0,7):
            pos_list.append(g_list[i][0].get_center())
            g_check.add(Check(self, bol_list[i]).move_to(pos_list[i]).scale(0.5))        
        t1.next_to(g_list, UP)
        
        #variables
        mu2 = MathTex(r"\mu_2", font_size=40).move_to(ramp_line.point_from_proportion(0.65)).rotate(ramp_line.get_angle())
        mu1 = MathTex(r"\mu_1", font_size=40).move_to(block2.point_from_proportion(0.27)).rotate(ramp_line.get_angle()).shift(-0.2*ramp_direction)
        
        #mojects groups for outlining
        original = VGroup(ramp, block1, block2, disk, stick, line2, line1)
        outlined = VGroup()
        for i in original:
            outlined.add(Outline(self,i))
        outlined[1] = original[1]
        
        #animation
        self.add(original)
        self.camera.frame.save_state()
        #self.play(Restore(self.camera.frame)) #used to restore to fullscreen
        self.wait()
        self.play(
            self.camera.frame.animate.move_to(block1.copy().shift([1.5,0,0])).set(width=3*block1.width),
            TransformMatchingShapes(original,outlined)
        )
        self.wait()
        self.play(Create(motion1), Write(motion1_lab))
        self.wait()
        self.play(Write(t1))
        self.wait()
        self.play(Write(g_list), FadeOut(motion1), FadeOut(motion1_lab))
        self.wait()
        self.play(Create(gravity), Write(f_g))
        self.play(Create(g_check[0]))
        self.wait()
        self.play(FadeOut(gravity), FadeOut(f_g))
        self.play(ShowPassingFlash(contact1.copy().set_color(GREEN), 1.5), run_time=1.5)
        self.wait()
        self.play(ShowPassingFlash(outlined[2].copy().set_color(YELLOW), 0.4), run_time=1.5)
        self.wait()
        self.play(
            Create(normal), Write(f_n))
        self.play(Create(g_check[1]))
        self.wait()
        self.play(FadeIn(mu1))
        self.wait()
        self.play(FadeOut(normal), FadeOut(f_n))
        self.play(
            Create(frictionA), 
            Create(frictionB), 
            Write(f_f),
            FadeOut(mu1)
            )
        self.wait()
        self.play(
            outlined[2].animate.shift(0.3*ramp_line.get_unit_vector()),
            block1.animate.shift(-0.3*ramp_line.get_unit_vector()),
            outlined[6].animate.shift(-0.3*ramp_line.get_unit_vector()),
            run_time=1.5,
            rate_func = rate_functions.linear)
        self.wait()
        self.play(FadeOut(frictionB))
        self.play(
            Write(g_check[2]),
            outlined[2].animate.shift(-0.3*ramp_line.get_unit_vector()),
            block1.animate.shift(0.3*ramp_line.get_unit_vector()),
            outlined[6].animate.shift(0.3*ramp_line.get_unit_vector())
            )
        self.wait()
        self.play(FadeOut(frictionA), FadeOut(f_f))
        self.wait()
        self.play(Create(tension), Write(f_t))
        self.play(Create(g_check[3]))
        self.wait()
        self.play(Indicate(tension), run_time=1.5)
        self.wait()
        self.play(FadeOut(tension), FadeOut(f_t))
        self.play(Create(g_check[4]), Create(g_check[5]))
        self.wait()
        self.play(Create(g_check[6]))
        self.wait(2)
        
        #next paragraph, end of checklist
        
        self.play(FadeOut(g_check), FadeOut(g_list), FadeOut(t1))
        #self.play(self.camera.frame.animate.move_to(block1.copy()).set(width=3*block1.width))
        axis_center = block2.point_from_proportion(0.0)
        x_axis = Arrow(axis_center, axis_center + 1*LEFT, buff = 0)
        y_axis = Arrow(axis_center, axis_center + 1*UP, buff = 0)
        g_axis = VGroup(x_axis,y_axis).shift(0.3*ramp_direction + 1*RIGHT)
        axis_center = x_axis.get_right()
        x_axis_tex = always_redraw(
            lambda: MathTex(r"x", font_size = 40).next_to(x_axis, LEFT, buff=0.1)
        )
        y_axis_tex = always_redraw(
            lambda: MathTex(r"y", font_size = 40).next_to(y_axis, UP, buff=0.1)
        )
        
        self.play(Create(g_axis), Write(x_axis_tex), Write(y_axis_tex))
        self.wait()
        self.play(g_axis.animate.rotate(ramp_line.get_angle(), about_point=axis_center))
        self.wait()
        tension.shift(0.2*ramp_direction)
        motion1.shift(-0.2*ramp_direction)
        self.play(Succession(
            FadeIn(frictionA),
            FadeIn(normal),
            FadeIn(tension),
            FadeIn(motion1)
        ))
        self.wait()
        self.play(FadeIn(gravity))
        self.wait()
        self.play(Succession(Indicate(y_axis), Indicate(x_axis)), run_time=2)
        self.wait()
        g_fade = VGroup(x_axis, y_axis, x_axis_tex, y_axis_tex)
        self.play(
            FadeOut(g_fade)
        )
        self.wait()
        
        #starting forces
        MathTex.set_default(font_size=35)
        ta = MathTex(r"F_x:", font_size=50).move_to(t1)
        tb = MathTex(r"F_T")
        tc = MathTex(r"- F_{g,x}")
        td = MathTex(r"-F_f")
        tda = MathTex(r"-\mu_1 F_N")
        te = MathTex(r"= m_1 a_1")
        t_group = VGroup(tb, tc, td).arrange(RIGHT, buff=0.1).next_to(ta,DOWN)
        te.next_to(t_group,DOWN)
        tda.move_to(td)
        
        self.play(Write(ta))
        self.wait()
        self.play(Write(tb))
        self.wait()
        self.play(Write(tc))
        self.wait()
        self.play(Write(td))
        self.wait()
        self.play(Write(te))
        self.wait()
        self.play(Succession(Indicate(td), Indicate(tb)))
        self.wait()
        self.play(TransformMatchingShapes(td,tda), tb.animate.shift([-0.2,0,0]), tc.animate.shift([-0.2,0,0]))
        self.wait()
        g_fade = VGroup(ta, tb, tc, tda, te)
        self.play(FadeOut(g_fade))
        self.wait()
        
        ta = MathTex(r"F_y:", font_size=50).move_to(t1)
        tb = MathTex(r"F_N")
        tc = MathTex(r"-F_{g,y}")
        td = MathTex(r"= 0")
        te = MathTex(r"F_N=F_{g,y}")
        t_group = VGroup(tb, tc).arrange(RIGHT, buff=0.1).next_to(ta,DOWN)
        td.next_to(t_group, DOWN)
        te.move_to(t_group)
        
        self.play(Write(ta))
        self.wait()
        self.play(Write(tb))
        self.wait()
        self.play(Write(tc))
        self.wait()
        self.play(Write(td))
        self.wait()
        self.play(TransformMatchingShapes(t_group,te), FadeOut(td))
        self.wait()
        self.play(Indicate(tension))
        self.wait()
        
        g_fade = VGroup(ta, te, normal, tension, motion1, gravity, frictionA)
        
        self.play(FadeOut(g_fade))
        self.play(
            Restore(self.camera.frame),
            TransformMatchingShapes(outlined, original),
        )
        outlined[1] = Outline(self, original[1])
        outlined[2] = original[2]
        self.wait()
        self.play(Indicate(block2), run_time=1.5)
        self.wait()
        self.play(
            self.camera.frame.animate.move_to(block2.copy().shift([2.1,0,0])).set(width=2.45*block2.width),
            TransformMatchingShapes(original,outlined)
        )
        self.wait()
        
        # forces on second block
        g_list.next_to(block2,RIGHT, buff = 1).scale(1.4)
        t1.set_font_size(70).next_to(g_list, UP, buff=0.4)
        g_check = VGroup()
        pos_list = []
        for i in range(0,7):
            pos_list.append(g_list[i][0].get_center())
            g_check.add(Check(self, bol_list[i]).move_to(pos_list[i]).scale(0.5*1.4)) 
        
        #block2 force/motion lines
        MathTex.set_default(font_size = 55)
        MathTex.set_default(stroke_width=2)
        motion2 = Arrow(block2.get_center(), block2.get_center()+1*ramp_line.get_unit_vector(), buff=0, color=WHITE)
        motion2_lab = MathTex(r"a", color=WHITE).next_to(motion2, ramp_line.get_unit_vector(), buff = 0.1)
        gravity2 = Arrow(block2.get_center(), block2.get_center() + 1.5*DOWN, buff=0, color = RED)
        f_g2 = MathTex(r"F_g", color = RED).next_to(gravity2, LEFT, buff=0.05).shift([0,0,0])
        normal2 = Arrow(block2.get_center(), block2.get_center()+1.5*ramp_direction, buff=0, color=GREEN_B)
        f_n2 = MathTex(r"F_{N,s}", color = GREEN_B).next_to(normal2, UR, buff= 0)
        normal2A = Arrow(block2.get_center(), block2.get_center()-1.5*ramp_direction, buff=0, color=GREEN_B)
        f_n2A = MathTex(r"F_{N,1}", color = GREEN_B).next_to(normal2A, DL, buff = 0)
        
        contact2 = Line(block2.point_from_proportion(0.5),block2.point_from_proportion(0.5 + (block_dim[1]/(2*block_dim[0] + 2*block_dim[1]))), buff=0)
        frictionA2 = Arrow(block2.get_center(), block2.get_center() - 1.5*ramp_line.get_unit_vector(), buff=0, color=YELLOW)
        frictionB2 = Arrow(block2.get_center(), block2.get_center() - 1.5*ramp_line.get_unit_vector(), buff=0, color=YELLOW)
        f_f2 = MathTex(r"F_{f,s}", color=YELLOW).move_to(frictionB2.get_center()).shift(-0.75*ramp_direction - ramp_line.get_unit_vector())
        f_f2B = MathTex(r"F_{f,1}", color=YELLOW).move_to(frictionA2.get_center()).shift(0.45*ramp_direction - ramp_line.get_unit_vector())
        tension2 = Arrow(block2.point_from_proportion(p2),block2.point_from_proportion(p2) - 1*ramp_line.get_unit_vector(), color = ORANGE, buff=0)
        f_t2 = MathTex(r"F_T", color=ORANGE).next_to(tension2, UP, buff=-0.05).shift([0,0.25,0])
        
        self.play(Write(g_list), Create(t1))
        self.wait()
        self.play(
            Create(gravity2), 
            Write(f_g2),
            Write(g_check[0])
        )
        self.wait()
        self.play(Create(normal2))
        self.wait()
        self.play(Write(f_n2))
        self.wait()
        self.play(
            Create(normal2A), 
            Write(f_n2A),
            f_g2.animate.next_to(gravity2,RIGHT, buff=0.1).shift([0,-0.6,0]),
            Write(g_check[1])
        )
        self.wait()
        self.play(ShowPassingFlash(contact2.copy().set_color(YELLOW), time_width=1.5), run_time=1.5)
        self.wait()
        self.play(
            Create(frictionB2), 
            Write(f_f2),
            Write(g_check[2])
        )
        self.wait()
        self.play(ShowPassingFlash(contact1.copy().set_color(YELLOW), time_width=1.5), run_time=1.5)
        self.wait()
        self.play(FadeIn(frictionA))
        self.wait()
        self.play(FadeOut(frictionA))
        self.wait()
        self.play(
            Create(frictionA2), 
            Write(f_f2B),
            frictionA2.animate.shift(0.2*ramp_direction),
            frictionB2.animate.shift(-0.2*ramp_direction),
            f_f2.animate.shift(-0.15*ramp_direction),
            f_f2B.animate.shift(0.2*ramp_direction),
        )
        self.wait()
        self.play(
            Create(tension2),
            Write(f_t2),
            Write(g_check[3])
        )
        self.wait()
        self.play(Write(g_check[4]), Write(g_check[5]))
        self.wait()
        self.play(
            Create(motion2), 
            Write(motion2_lab),
            Write(g_check[6])
        )
        self.wait()
        
        axis_center = block2.point_from_proportion(0) + [1.5,-1,0]
        x_axis = Arrow(axis_center, axis_center + 1*LEFT, buff = 0)
        y_axis = Arrow(axis_center, axis_center + 1*UP, buff = 0)
        g_axis = VGroup(x_axis,y_axis).rotate(ramp_line.get_angle(), about_point=axis_center)
        axis_center = x_axis.get_right()
        x_axis_tex = always_redraw(
            lambda: MathTex(r"x", font_size = 40).next_to(x_axis, LEFT, buff=0.1)
        )
        y_axis_tex = always_redraw(
            lambda: MathTex(r"y", font_size = 40).next_to(y_axis, UP, buff=0.1)
        )
        
        self.play(
            FadeOut(t1),
            FadeOut(g_list),
            FadeOut(g_check)
        )
        self.wait()
        self.play(
            FadeIn(g_axis),
            FadeIn(x_axis_tex),
            FadeIn(y_axis_tex)
        )
        self.wait()
        self.play(Succession(
            Indicate(tension2),
            Indicate(frictionA2),
            Indicate(frictionB2),
            Indicate(normal2),
            Indicate(normal2A),
            Indicate(motion2)
        ), run_time = 3)
        self.wait()
        self.play(
            FadeOut(g_axis),
            FadeOut(x_axis_tex),
            FadeOut(y_axis_tex)
        )
        self.wait()        

        g_fade = Group(
            frictionA2, frictionB2,
            f_f2, f_f2B,
            normal2, normal2A,
            f_n2, f_n2A,
            motion2, motion2_lab,
            tension2, f_t2,
            gravity2, f_g2
        )
        

        
