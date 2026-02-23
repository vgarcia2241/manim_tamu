from manim import *
import numpy as np

MathTex.set_default(font_size = 80)
fontsize = 70
line_weight = 0.7
width = 6 #for ramp

class s1(Scene):             
    
    def funcspring(self,t):
        N=3.5
        #return (np.cos(2*PI*N*t/np.abs(func(ttracker.get_value())+3)+PI)+t*np.abs(func(ttracker.get_value())+3)/N,np.sin(2*PI*N*t/np.abs(func(ttracker.get_value())+3)+PI),0)
        return(np.cos(t)+N*t/(2*PI),np.sin(t),0)

    def construct(self):
        k=50
        m1=5
        m2=20
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
            lambda: Square(color=BLUE, fill_opacity=1,side_length=0.5).move_to([func(ttracker.get_value())+1,2,0])
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
        
        #animations
        self.play(FadeIn(sq1,sq2,spring,pulley,Dash1,Dash2,Dash3,HLine,VLine,connect, ground, wall, back_wall))
        #self.play(ttracker.animate.set_value(20),run_time=10,rate_func=linear)
        self.wait()
        self.play(ShowPassingFlash(HLine.copy().set_color(YELLOW), time_width=1.5), run_time = 2)
        self.play(ShowPassingFlash(VLine.copy().set_color(YELLOW), time_width=1.5), run_time = 2)
        self.wait()
        self.play(ShowPassingFlash(spring.copy().set_color(YELLOW), time_width=1.5), run_time = 1.5)
        self.wait()
        self.play(Create(accel_1), Write(accel_1_lab))
        self.wait()
        self.play(Create(x_origin), Write(x_origin_lab))
        self.wait()
        
        

