from manim import *
import numpy as np

MathTex.set_default(font_size = 70)
MathTex.set_default(stroke_width=2.5)

def Outline(self,obj):
    '''
    function which takes in some Mobject and return an outline-only version
    '''
    temp = obj.copy()
    temp.set_fill(color=None, opacity=0).set_stroke(width=DEFAULT_STROKE_WIDTH, color=WHITE)
    return temp

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