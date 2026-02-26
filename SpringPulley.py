from manim import *
import numpy as np

MathTex.set_default(font_size = 80)
fontsize = 70
line_weight = 2
width = 6 #for ramp

def Outline(self,obj):
    '''
    function which takes in some Mobject and return an outline-only version
    '''
    temp = obj.copy()
    temp.set_fill(color=None, opacity=0).set_stroke(width=DEFAULT_STROKE_WIDTH, color=WHITE)
    return temp

def Check_Point(self, text): #create obj with text and box for checklist
    box = Square(0.7).set_stroke(width=line_weight)
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

class s1(Scene):             
    
    def funcspring(self,t):
        N=3.5
        #return (np.cos(2*PI*N*t/np.abs(func(ttracker.get_value())+3)+PI)+t*np.abs(func(ttracker.get_value())+3)/N,np.sin(2*PI*N*t/np.abs(func(ttracker.get_value())+3)+PI),0)
        return(np.cos(t)+N*t/(2*PI),np.sin(t),0)

    def construct(self):
        k=50
        m1=5
        m2=15
        mu=0.2
        g=9.8
        A0=m2*g/k/2
        omega=np.sqrt((m1+m2)/k)
        period=2*PI/omega
        E=4*mu*m1*g/k/period

        def func(x):
            return -1*(A0-E*x)*np.cos(omega*x)
        
        ttracker = ValueTracker(0)
        
        sq1 = always_redraw(
            lambda: Square(color=BLUE_D, fill_opacity=1,side_length=0.5).move_to([func(ttracker.get_value())+1,2,0])
        )
        sq2 = always_redraw(
            lambda: Square(color=YELLOW, fill_opacity=1,side_length=0.5).move_to([2+1,-1*func(ttracker.get_value())-1,0])
        )

        N=5.5
        aspect=0.75
        amp=0.25
        spring = always_redraw(
            lambda: ParametricFunction(
            lambda t: np.array([(func(ttracker.get_value())-1.625+5)*t-amp*aspect*(np.cos(2*PI*t*N)-1)-3,-amp*np.sin(2*PI*t*N)+2,0]),color=WHITE
        ).set_z_index(-0.1))
        self.add(spring)

        circrad=0.25
        pulley = Circle(radius=circrad,fill_opacity=1,color=GRAY).move_to([sq2.get_center()[0]-0.25,sq1.get_center()[1]-0.25,0]).set_z_index(1.2) #color=YELLOW_C,
        Dash1 = always_redraw(
            lambda: DashedLine(start=pulley.get_center(),end=pulley.get_center()+[circrad*np.cos(270*PI/180-(func(ttracker.get_value())+func(0))/circrad),circrad*np.sin(270*PI/180-(func(ttracker.get_value())+func(0))/circrad),0],color=BLACK).set_z_index(1.2)
        )
        Dash2 = always_redraw(
            lambda: DashedLine(start=pulley.get_center(),end=pulley.get_center()+[circrad*np.cos(150*PI/180-(func(ttracker.get_value())+func(0))/circrad),circrad*np.sin(150*PI/180-(func(ttracker.get_value())+func(0))/circrad),0],color=BLACK).set_z_index(1.2)
        )
        Dash3 = always_redraw(
            lambda: DashedLine(start=pulley.get_center(),end=pulley.get_center()+[circrad*np.cos(30*PI/180-(func(ttracker.get_value())+func(0))/circrad),circrad*np.sin(30*PI/180-(func(ttracker.get_value())+func(0))/circrad),0],color=BLACK).set_z_index(1.2)
        )

        HLine = always_redraw(
            lambda: Line(start=sq1.get_center()+[0.25,0,0],end=pulley.get_center()+[0,circrad,0])
        )
        VLine = always_redraw(
            lambda: Line(start=sq2.get_center()+[0,circrad,0],end=pulley.get_center()+[circrad,0,0])
        )
        connect = Arc(radius=circrad,start_angle=0,angle=PI/2,arc_center=pulley.get_center(),color=WHITE)
        
        ground = Line([spring.get_left()[0], sq1.get_bottom()[1], 0], [pulley.get_center()[0], sq1.get_bottom()[1], 0]).set_z_index(1.1)
        wall = Line(ground.get_right() + [-0.15,0,0], ground.get_right() + [-0.15,-4,0]).set_z_index(-1)
        back_wall = Line(ground.get_left(), ground.get_left() + [0,0.5,0])
        
        accel_1 = Arrow(sq1.get_right(), sq1.get_right() + 1.5*RIGHT, color = RED, buff=0)
        accel_1_lab = MathTex(r"a", color=RED).next_to(accel_1, UP)
        
        x_origin = Line(sq1.get_center()+[0,-0.1,0], sq1.get_center()+[0,-0.5,0]).set_z_index(1)
        x_origin_lab = MathTex(r"x=0", font_size = 60).next_to(x_origin, DOWN, buff=0.1)
        
        cover = Rectangle(width=14,height=8, color=BLACK).set_fill(BLACK, 1).set_z_index(2)
        
        #animations
        self.play(FadeIn(sq1,sq2,spring,pulley,Dash1,Dash2,Dash3,HLine,VLine,connect, ground, wall, back_wall))
        #self.play(ttracker.animate.set_value(20),run_time=10,rate_func=linear)
        self.wait()
        self.play(ShowPassingFlash(HLine.copy().set_color(YELLOW), time_width=1.5), run_time = 2)
        self.play(ShowPassingFlash(VLine.copy().set_color(YELLOW), time_width=1.5), run_time = 2)
        self.wait()
        self.play(ShowPassingFlash(spring.copy().set_color(YELLOW).set_z_index(1), time_width=1.5), run_time = 1.5)
        self.wait()
        self.play(Create(accel_1), Write(accel_1_lab))
        self.wait()
        self.play(Create(x_origin), Write(x_origin_lab))
        self.wait()
        self.play(FadeOut(accel_1, accel_1_lab, x_origin, x_origin_lab))
        self.wait()
        self.play(ttracker.animate.set_value(21), run_time = 4.5, rate_func = rate_functions.linear)
        self.wait(1)
        self.play(FadeIn(cover), run_time=0.5)
        self.play(ttracker.animate.set_value(0), run_time=0.5)
        self.play(FadeOut(cover))
        self.wait()
        self.play(ttracker.animate.set_value(21), run_time=4.5, rate_func = rate_functions.linear)
        self.play(FadeIn(cover), run_time=0.5)
        self.play(ttracker.animate.set_value(0), run_time=0.5)
        self.play(FadeOut(cover))
        self.wait()
        
class s2(MovingCameraScene):
    def construct(self):
        k=50
        m1=5
        m2=15
        mu=0.2
        g=9.8
        A0=m2*g/k/2
        omega=np.sqrt((m1+m2)/k)
        period=2*PI/omega
        E=4*mu*m1*g/k/period

        def func(x):
            return -1*(A0-E*x)*np.cos(omega*x)
        
        ttracker = ValueTracker(0)
        
        sq1 = always_redraw(
            lambda: Square(color=BLUE_D, fill_opacity=1,side_length=0.5).move_to([func(ttracker.get_value())+1,2,0]).set_z_index(1)
        )
        sq2 = always_redraw(
            lambda: Square(color=YELLOW, fill_opacity=1,side_length=0.5).move_to([2+1,-1*func(ttracker.get_value())-1,0]).set_z_index(1)
        )

        N=5.5
        aspect=0.75
        amp=0.25
        spring = always_redraw(
            lambda: ParametricFunction(
            lambda t: np.array([(func(ttracker.get_value())-1.625+5)*t-amp*aspect*(np.cos(2*PI*t*N)-1)-3,-amp*np.sin(2*PI*t*N)+2,0]),color=WHITE
        ).set_z_index(-0.1))
        self.add(spring)

        circrad=0.25
        pulley = Circle(radius=circrad,fill_opacity=1,color=GRAY).move_to([sq2.get_center()[0]-0.25,sq1.get_center()[1]-0.25,0]).set_z_index(1.2) #color=YELLOW_C,
        Dash1 = always_redraw(
            lambda: DashedLine(start=pulley.get_center(),end=pulley.get_center()+[circrad*np.cos(270*PI/180-(func(ttracker.get_value())+func(0))/circrad),circrad*np.sin(270*PI/180-(func(ttracker.get_value())+func(0))/circrad),0],color=BLACK).set_z_index(1.2)
        )
        Dash2 = always_redraw(
            lambda: DashedLine(start=pulley.get_center(),end=pulley.get_center()+[circrad*np.cos(150*PI/180-(func(ttracker.get_value())+func(0))/circrad),circrad*np.sin(150*PI/180-(func(ttracker.get_value())+func(0))/circrad),0],color=BLACK).set_z_index(1.2)
        )
        Dash3 = always_redraw(
            lambda: DashedLine(start=pulley.get_center(),end=pulley.get_center()+[circrad*np.cos(30*PI/180-(func(ttracker.get_value())+func(0))/circrad),circrad*np.sin(30*PI/180-(func(ttracker.get_value())+func(0))/circrad),0],color=BLACK).set_z_index(1.2)
        )

        HLine = always_redraw(
            lambda: Line(start=sq1.get_center()+[0.25,0,0],end=pulley.get_center()+[0,circrad,0])
        )
        VLine = always_redraw(
            lambda: Line(start=sq2.get_center()+[0,circrad,0],end=pulley.get_center()+[circrad,0,0])
        )
        connect = Arc(radius=circrad,start_angle=0,angle=PI/2,arc_center=pulley.get_center(),color=WHITE)
        
        ground = Line([spring.get_left()[0], sq1.get_bottom()[1], 0], [pulley.get_center()[0], sq1.get_bottom()[1], 0]).set_z_index(1.1)
        wall = Line(ground.get_right() + [-0.15,0,0], ground.get_right() + [-0.15,-4,0]).set_z_index(-1)
        back_wall = Line(ground.get_left(), ground.get_left() + [0,0.5,0])
        
        #checklist
        t1 = Tex(r"Checklist:").scale(0.35)
        t_list = ["Gravity","Normal","Friction","Tension","Spring","Other","Motion"]
        g_list = VGroup()
        for i in range(0,7):
            g_list.add(Check_Point(self, t_list[i]))
        g_list.arrange_in_grid(4,2, flow_order='dr', cell_alignment=[-1,0,0], buff = 0.4).scale(0.28).next_to(sq2, RIGHT, buff=0.55).shift([0,-0.15,0])
        pos_list = []
        bol_list = [True,False,False,True,False,False,True]
        g_check = VGroup()
        for i in range(0,7):
            pos_list.append(g_list[i][0].get_center())
            g_check.add(Check(self, bol_list[i]).move_to(pos_list[i]).scale(0.28).set_stroke(width=2))        
        t1.next_to(g_list, UP)
        
        #sq2 forces
        MathTex.set_default(font_size=25)
        gravity2 = Arrow(sq2.get_bottom(), sq2.get_bottom()+0.65*DOWN, color=ORANGE, buff=0)
        f_g2 = MathTex(r"F_g", color=ORANGE).next_to(gravity2, RIGHT, buff=0.0)
        tension2 = Arrow(sq2.get_top(), sq2.get_top() + 0.65*UP, color=BLUE, buff=0)
        f_t2 = MathTex(r"F_T", color=BLUE).next_to(tension2, RIGHT, buff=0.0)
        accelA = gravity2.copy().set_color(GREEN)
        accelB = tension2.copy().set_color(GREEN)
        f_a2 = MathTex(r"a", color=GREEN).next_to(sq2, RIGHT, buff=0.1)
        
        #animation
        self.add(sq1, sq2, spring, wall, back_wall, ground, pulley, Dash1, Dash2, Dash3, connect, VLine, HLine)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(sq2.copy().shift([1.3,0,0])).set(width=7.5*sq2.width))
        self.wait()
        self.play(Write(t1), Write(g_list))
        self.wait()
        for i in g_check:
            self.play(Write(i), run_time=0.25)
        self.wait()
        self.play(Create(gravity2), Write(f_g2))
        self.play(Create(tension2), Write(f_t2))
        self.wait()
        self.play(
            Create(accelA), Create(accelB), Write(f_a2), 
            gravity2.animate.shift([0.15,0,0]),
            f_g2.animate.shift([0.15,0,0]),
            accelA.animate.shift([-0.15,0,0]),
            tension2.animate.shift([0.15,0,0]),
            f_t2.animate.shift([0.15,0,0]),
            accelB.animate.shift([-0.15,0,0])
        )
        self.wait()
        self.play(FadeOut(t1, g_check, g_list))
        self.wait()
        
        t2 = MathTex(r"F_y:").move_to(t1)
        t3 = MathTex(r"m_2 a = m_2 g - F_T").next_to(t2, DOWN, buff=0.3)
        t3A = MathTex(r"{{a}} = g - {{F_T}} / m_2").move_to(t3)
        
        self.play(Write(t2))
        self.wait()
        self.play(Write(t3))
        self.wait()
        self.play(TransformMatchingShapes(t3,t3A))
        self.wait()
        self.play(Indicate(t3A[2]), run_time=1.5)
        self.wait()
        self.play(Indicate(t3A[0]), run_time=1.5)
        self.wait()
        self.play(
            FadeOut(t2, t3A, gravity2, f_g2, tension2, f_t2, accelA, accelB, f_a2),
            Restore(self.camera.frame)
        )
        self.wait()
        
        #first block forces
        gravity1 = Arrow(sq1.get_bottom(), sq1.get_bottom() + 0.5*DOWN, color=ORANGE, buff=0, max_stroke_width_to_length_ratio=7)
        f_g1 = MathTex(r"F_g", color=ORANGE).next_to(gravity1, RIGHT, buff=0)
        tension1 = Arrow(sq1.get_right(), sq1.get_right() + 0.5*RIGHT, color=BLUE, buff=0, max_stroke_width_to_length_ratio=7)
        f_t1 = MathTex(r"F_T", color=BLUE).next_to(tension1, UP, buff=0)
        
        #checklist
        
        self.play(self.camera.frame.animate.move_to(sq1.copy().shift([0,0.6,0])).set(width=10*sq1.width))
        self.wait()
        self.play(Create(gravity1), Write(f_g1))
        self.play(Create(tension1), Write(f_t1))
        self.wait()
        