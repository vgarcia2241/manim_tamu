from manim import *
import numpy as np

MathTex.set_default(font_size = 80)
fontsize = 70
line_weight = 5

def Bullet(self, pos):
    return Polygon([-1,-0.5,0], [-1,0.5,0], [0.5,0.5,0], [1.2,0,0], 
                        [0.5,-0.5,0]).set_stroke(width = line_weight).scale(0.3).move_to(pos)
def moving(self, obj, velocity, tar_pos, t):
    position = [velocity*t,0,0] + obj.get_center()
    if(position[0] <= tar_pos[0]):
        position = tar_pos
        
    return obj.copy().move_to(position).set_z_index(1)



class s1(Scene):
    def construct(self):
        disk = Circle(2, stroke_width = line_weight)
        d_center = Dot(disk.get_center(), stroke_width = line_weight)
        d_c_label = MathTex(r"C", font_size = 0.75*fontsize).next_to(d_center, LEFT)
        d_pivot = Dot(disk.get_center() -[0,0.6*disk.radius,0], stroke_width = line_weight)
        d_p_label = MathTex(r"P", font_size = 0.75*fontsize).next_to(d_pivot, RIGHT)
        g_disk = VGroup(disk, d_center, d_pivot, d_p_label, d_c_label).shift([0,1,0])
        piv_dist_line = Line(d_center, d_pivot)
        piv_dist = BraceLabel(piv_dist_line,"d",LEFT, font_size = fontsize)
        piv_dist.submobjects[1].set_color(YELLOW)
        
        mass = MathTex(r"M", font_size = 0.75*fontsize, color = YELLOW).next_to(disk, UL, buff = -1.4)
        r_line = Line(disk.get_center(), disk.point_at_angle(0))
        radius = MathTex(r"R", font_size = 0.75*fontsize, color = YELLOW).next_to(r_line, UP)
        
        bullet = Bullet(self, [5.5,2.25,0]).rotate(PI)
        collision_point = Dot(bullet.get_center() - [4.75,0,0])
        bullet_vel = -(bullet.get_x() - collision_point.get_x())
        t_impact = ((collision_point.get_center() - bullet.get_center()) / bullet_vel)[0]
        
        impact_line = Line(bullet.get_center(),bullet.get_center() - [0,bullet.get_y() - d_center.get_y(),0])
        impact_parameter = BraceLabel(impact_line,r"b", RIGHT, buff = 1*MED_LARGE_BUFF, font_size= fontsize)
        impact_parameter.submobjects[1].set_color(YELLOW)
        
        h_line = DashedLine(disk.get_center(), disk.get_center() + [bullet.get_x() + 0.5,0,0])
        
        self.play(
            Create(disk), Create(d_center)
        )
        self.wait()
        self.play(
            Write(mass), Write(radius), Create(r_line)
        )
        self.wait()
        self.play(
            Create(d_pivot), Write(d_p_label)
        )
        self.play(Create(piv_dist))
        self.wait()
        self.play(
            Create(bullet), FadeOut(d_center), FadeOut(piv_dist),
            FadeOut(d_p_label), FadeOut(r_line), FadeOut(radius),
            FadeOut(mass)
        )
        self.wait()
        self.play(
            Create(h_line), Create(impact_parameter), Create(d_center)
        )
        self.wait()
        self.play(
            FadeOut(h_line), FadeOut(impact_parameter), FadeOut(d_center)
        )
        self.wait()
        
        time_tracker = ValueTracker(0)
        bullet_mov = always_redraw(
            lambda: moving(self, bullet, bullet_vel, collision_point.get_center(), time_tracker.get_value())
        )
        disk_mov = always_redraw(
            lambda: Circle(disk.radius).move_to(d_center)
        )
        bullet_mov.set_z_index(1)
        self.add(bullet_mov)
        self.remove(bullet)
        self.add(disk_mov)
        self.remove(disk)
        self.play(time_tracker.animate.set_value(t_impact), rate_func = rate_functions.linear, run_time = 0.175)
        
        g_rot = VGroup(disk.copy(), d_pivot.copy(), bullet.copy().move_to(bullet_mov))
        self.add(g_rot)
        self.remove(bullet_mov, disk_mov, d_pivot)
        self.play(Rotate(g_rot, 180*DEGREES, about_point = d_pivot.get_center()), rate_func = rate_functions.ease_out_elastic, run_time = 2.35)
        self.wait()
        
        self.play(*[FadeOut(i) for i in self.mobjects])
        self.wait()
        
        self.play(FadeIn(disk, d_pivot, bullet))
        self.wait()
        time_tracker.set_value(0)
        self.add(bullet_mov)
        self.remove(bullet)
        self.play(time_tracker.animate.set_value(t_impact), rate_func = rate_functions.linear, run_time = 0.175)
        self.wait()
        self.remove(bullet_mov)
        self.add(bullet.move_to(bullet_mov))
        
        l_line = DashedLine(bullet.get_center() + [0.07,-0.15,0], d_pivot, buff = 0.1)
        l_vec = l_line.get_end() - l_line.get_start()
        l_len = np.linalg.norm(l_vec)
        l_unit = l_vec / l_len
        new_direction = np.array([-l_unit[1], l_unit[0], 0])
        l_dist = MathTex(r"l", color=YELLOW, font_size = fontsize).next_to(l_line, RIGHT, buff=0).shift([0,-0.1,0])
        
        self.play(Create(l_line), Write(l_dist))
        self.wait()
        
        ang_cir = Circle(radius=1.2*(disk.radius)).move_to(disk)
        angular_velocity = CurvedArrow(ang_cir.point_at_angle(4.5*PI/6), ang_cir.point_at_angle(PI), angle=0.75)
        ang_label = MathTex(r"\omega_f", color=YELLOW, font_size = fontsize).next_to(angular_velocity, LEFT).shift([0.3,0.4,0])
        
        self.play(Create(angular_velocity), Write(ang_label))
        '''
        self.wait()
        self.play(FadeOut(angular_velocity), FadeOut(ang_label), FadeOut(l_dist), FadeOut(l_line))
        
        self.play(
            Rotate(disk, 180*DEGREES, about_point = d_pivot.get_center()),
            Rotate(bullet, 180*DEGREES, about_point = d_pivot.get_center())
        )
        angular_velocity.rotate(180*DEGREES, about_point = d_pivot.get_center())
        ang_label.next_to(angular_velocity, RIGHT)
        self.play(FadeIn(angular_velocity), FadeIn(ang_label))
        '''

        self.wait()
        self.play(*[FadeOut(i) for i in self.mobjects])
        
        
class s2(Scene):
    def construct(self):
        t1 = MathTex(r"Energy")
        t2 = MathTex(r"Momentum")
        g1 = VGroup(t1, t2).arrange(DOWN, buff = 1.5)
        scratch = Line(t1.get_left() - [0.05,0,0], t1.get_right() + [0.05,0,0]).set_stroke(width = 7)
        t3 = MathTex(r"Angular~Momentum", color = YELLOW).move_to(t2)
        
        self.play(Write(g1))
        self.wait()
        self.play(Create(scratch), t2.animate.set_color(YELLOW))
        self.wait()
        self.play(TransformMatchingTex(t2, t3))
        self.wait()
        
        self.play(*[FadeOut(i) for i in self.mobjects])
        
        #first set of equations appear
        fontsize =  80
        t1_1 = MathTex(r"L_i = {{r}} \times {{m}}{{v}} ").to_edge(LEFT, buff=1.75)
        t1_2 = MathTex(r"= (b + d) \times mv").move_to(t1_1)
        t2 = MathTex(r"m=100~\text{kg}")
        t3 = MathTex(r"v_0 = 200~\text{m/s}")
        
        disk = Circle(2, stroke_width = line_weight)
        bullet = Bullet(self, [5.5,1.4,0]).rotate(PI)
        d_center = Dot(disk.get_center(), stroke_width = line_weight)
        d_pivot = Dot(disk.get_center() -[0,0.6*disk.radius,0], stroke_width = line_weight)
        motion = Arrow(bullet.get_left(), bullet.get_left() + 2*LEFT)
        g1 = VGroup(disk, bullet, d_pivot, motion)
        box = SurroundingRectangle(g1.copy().scale(0.6).to_edge(RIGHT, buff=1.5), corner_radius=0.2, buff = 0.75, color = WHITE)
        
        self.play(FadeIn(disk), FadeIn(bullet), FadeIn(d_pivot))
        self.wait()
        self.play(Create(motion))
        self.wait()
        self.play(g1.animate.scale(0.65).move_to(box.get_center()), Create(box))
        self.wait()
        
        r_vec = always_redraw(
            lambda:Arrow(bullet.get_center(), d_pivot.get_center())
        )
        r_lab = always_redraw(
            lambda: MathTex(r"r", font_size = 0.65*fontsize).next_to(r_vec, DR).shift([-1.5,0.75,0])
        )
        
        self.play(Write(t1_1))
        self.wait()
        self.play(Succession(Indicate(t1_1[3]), Indicate(t1_1[4])), run_time = 3)
        self.wait()
        self.play(Indicate(t1_1[1]))
        self.wait()
        self.play(Create(r_vec), Write(r_lab))
        self.wait()
        self.play(FadeOut(r_lab))
        
        '''
        self.play(FadeOut(t1_1), FadeOut(box), FadeOut(r_lab))
        self.play(g1.animate.scale((1/0.65)).shift(ORIGIN - disk.get_center()))
        self.wait()
        '''
        
        g1_1 = VGroup(bullet, motion)
        self.play(g1_1.animate.shift([-3.6,0,0]), run_time = 1.5)
        self.wait()
        self.play(g1_1.animate.shift([3.5,0,0]), run_time = 1.5)
        self.wait()
        
        '''
        self.play(g1.animate.scale(0.65).move_to(box.get_center()), FadeIn(box))
        '''
        d_center = Dot(disk.get_center(), stroke_width = line_weight)
        
        self.play(Indicate(t1_1[0]))
        self.wait()
        self.play(g1_1.animate.shift([d_pivot.get_x() - bullet.get_x(),0,0]))
        self.wait()
        
        impact_line = Line(bullet.get_center(),bullet.get_center() - [0,bullet.get_y() - d_center.get_y(),0])
        impact_parameter = BraceLabel(impact_line,r"b", RIGHT, buff = 3*SMALL_BUFF, font_size= fontsize)
        impact_parameter.submobjects[1].set_color(YELLOW)
        
        piv_dist_line = Line(d_center, d_pivot)
        piv_dist = BraceLabel(piv_dist_line,"d",RIGHT, font_size = fontsize, buff = 3*SMALL_BUFF)
        piv_dist.submobjects[1].set_color(YELLOW)
        
        self.play(FadeIn(impact_parameter), FadeIn(piv_dist))
        self.wait()
        self.play(TransformMatchingTex(t1_1, t1_2))
        self.wait()

        self.play(*[FadeOut(i) for i in self.mobjects])
        
class s3(Scene):
    def construct(self):
        center_point = ORIGIN + [0,-1,0]
        point = Dot(center_point, stroke_width = line_weight)
        theta = ValueTracker(230) #zero point is to the right
        v1 = Arrow(center_point, center_point + 2.5*DOWN, color = BLUE, stroke_width = 10, buff = 0)
        v2 = always_redraw(
            lambda:Arrow(center_point, center_point + [2.5*np.cos(theta.get_value()*DEGREES), 2.5*np.sin(theta.get_value()*DEGREES),0], color = RED, stroke_width = 10, buff = 0)
        )
        #component vectors
        v2_x = always_redraw(
            lambda:Arrow(center_point, center_point + [v2.get_length()*(np.cos(theta.get_value()*DEGREES)),0,0], stroke_width = 10, buff = 0)
        )
        v2_y = always_redraw(
            lambda:Arrow(center_point, center_point + [0,v2.get_length()*(np.sin(theta.get_value()*DEGREES)),0], stroke_width = 10, buff = 0)
        )
        #model bullet
        bullet = Bullet(self,[0,0.5,0]).rotate(PI)
        v1_lab = MathTex(r"v_1", font_size = fontsize, color = YELLOW).next_to(v1, RIGHT)
        v2_lab = MathTex(r"v_2", font_size = fontsize, color = YELLOW).next_to(v2, LEFT)
        
        self.play(
            Create(v1), Write(v1_lab), 
        )
        self.play(
            Create(v2), Write(v2_lab), Create(point)
        )
        self.wait(2)
        self.play(FadeOut(v2_lab), FadeOut(v1_lab))
        #self.play(Rotate(v2, 2*PI, about_point = center_point), run_time = 1.5, rate_func = rate_functions.smooth)
        self.wait()
        self.play(FadeIn(v2_x), FadeIn(v2_y))
        self.wait()
        self.play(theta.animate.set_value(200))
        self.wait()
        self.play(theta.animate.set_value(230))
        self.wait()
        self.play(theta.animate.set_value(60))
        self.wait()
        
        t1 = MathTex(r"v_1 \times v_2 = |v_1||v_2|~sin \theta", font_size = fontsize)
        t1.to_edge(UP, buff = 1.2*LARGE_BUFF)
        t2 = MathTex(r"v_1 \times v_2 = |v_1||v_2|")

        self.play(Write(t1))
        self.wait()
        self.play(Indicate(v2_x), run_time = 1.5)
        self.wait()
        self.play(theta.animate.set_value(180))
        self.wait()