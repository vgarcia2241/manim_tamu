from manim import *
import numpy as np

stroke_width = 7
label_buffer = 0.5
MathTex.set_default(font_size = 80)

#inital bullet and question set  up
class s1(Scene):
    def Bullet(self, pos):
        return Polygon([-1,-0.5,0], [-1,0.5,0], [0.5,0.5,0], [1.2,0,0], 
                         [0.5,-0.5,0]).set_stroke(width = stroke_width).scale(0.3).move_to(pos)
    
    def moving(self, obj, velocity, tar_pos, t):
        position = [velocity*t,0,0] + obj.get_center()
        if(position[0] >= tar_pos[0]):
            position = tar_pos
            
        return obj.copy().move_to(position).set_z_index(1)
    
    def construct(self):
        #initial and stylistic parameters
        target_radius = 4
        
        tar_1 = Ellipse(width= target_radius*0.2,height= target_radius, color= WHITE).set_stroke(width = stroke_width)
        tar_2 = tar_1.copy().scale(0.5)
        tar_g = VGroup(tar_1, tar_2)
        tar_g.to_edge(RIGHT, buff = 1)
        
        start_line = Line((-(tar_g.get_critical_point((1,0,0))[0]),2,0),
                          (-(tar_g.get_critical_point((1,0,0))[0]),-2,0)).set_stroke(width = stroke_width)
        barrel = Rectangle(WHITE, 0.5, 1.7).set_stroke(width = stroke_width).move_to(start_line.get_center())
        
        sw_1 = Arc(radius=0.4, start_angle=-PI/2, angle=PI,color = RED).set_stroke(width=stroke_width)
        sw_2 = Arc(radius=0.2, start_angle=-PI/2, angle=PI,color = RED).set_stroke(width=stroke_width).shift([-0.05,0,0])
        sw_3 = Dot(radius = 0.1,color = RED).shift([-0.1,0,0])
        sw_g = VGroup(sw_1, sw_2, sw_3)
        
        bullet = self.Bullet(ORIGIN).next_to(start_line, RIGHT, buff = 0.1)
        sw_g.next_to(start_line, RIGHT, buff = 0.05)
        
        b_vel_label = MathTex(r"v_b = 300~\text{m/s}", color = YELLOW).next_to(bullet, RIGHT, buff = 2*label_buffer)
        sw_vel_label = MathTex(r"v_s = 350~\text{m/s}", color = YELLOW).next_to(sw_g, RIGHT, buff = 2*label_buffer)
        
        dist = BraceBetweenPoints(barrel.get_critical_point([1,0,0]), tar_g.get_center()).set_y(tar_g.get_bottom()[1] - 0.5)
        dist_label = MathTex(r"d", color = YELLOW).next_to(dist, DOWN)
        
        #adjustable
        sound_vel = (tar_g.get_center()[0] - start_line.get_center()[0])
        bullet_vel = 0.5*sound_vel
        
        #bullet impact time
        t_impact = ((tar_g.get_center() - start_line.get_center()) / bullet_vel)[0]
        #sound impact time
        t_impact_2 = ((tar_g.get_center() - start_line.get_center()) / sound_vel)[0]
        
###########################################################################################
        
        self.play(
            Create(barrel), Create(tar_g)
        )
        self.play(Create(bullet), Write(b_vel_label))
        self.play(Wait(1))
        self.play(FadeOut(b_vel_label))
        
        time_tracker = ValueTracker(0)
        sound_mov = always_redraw(
            lambda: self.moving(sw_g, sound_vel, tar_g.get_center(), time_tracker.get_value())
        )
        bullet_mov = always_redraw(
            lambda: self.moving(bullet, bullet_vel, tar_g.get_center(), time_tracker.get_value())
        )
        sound_mov.set_z_index(1)
        bullet_mov.set_z_index(1)
        
        self.play(Create(bullet_mov), run_time = 0.5)
        self.add(sound_mov)
        self.remove(bullet)
        self.play(time_tracker.animate.set_value(t_impact), rate_func = linear, run_time = 1.5)
        
        self.play(Wait(1))
        sw_vel_label.next_to(sound_mov, LEFT, buff = 0.5)
        self.play(Write(sw_vel_label))
        self.play(Wait(1))
        
        self.play(FadeIn(dist), Write(dist_label), run_time = 1)
        self.play(Indicate(dist_label, scale_factor= 1.5), run_time = 2)
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])

#listing equations
class s2(Scene):
    def construct(self):
        #knowns
        t1 = MathTex(r"x_{0,b} = 0")
        t2 = MathTex(r"x_{0,s} = 0")
        t3 = MathTex(r"v_b = 300 \text{m/s}")
        t4 = MathTex(r"v_s = 350 \text{m/s}")
        #unknowns
        t5 = MathTex(r"x_{f,b} =~?")
        t5_1 = MathTex(r"x_{f,b} = d =~?")
        t6 = MathTex(r"x_{s,f} = d =~?")
        t7 = MathTex(r"t_b =~?")
        t8 = MathTex(r"t_s =~?")
        
        #dividing line
        divider = Line([0,2.5,0], [0,-3.5,0])
        
        g1 = VGroup(t1, t2, t3, t4, t5, t6, t7, t8)
        g1.arrange_in_grid(4,2,buff = (1.5, 0.7), flow_order= 'dr')
        t5_1.move_to(t5)
        first_round = [t1,t2,t3,t4, t5]
        second_round = [t6,t7,t8]
        
        
######################################################################
        self.play(Create(divider))
        self.play(Wait(1.0))
        for i in first_round:
            self.play(Write(i))
            self.play(Wait(1.0))

        self.play(TransformMatchingShapes(t5,t5_1))
        self.play(Wait(1.0))
        for i in second_round:
            self.play(Write(i))
            self.play(Wait(1.0))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])

#relating distance and time of bullet and sound
class s3(Scene):
    def moving(self, obj, velocity, tar_pos, t):
        position = [velocity*t,0,0] + obj.get_center()
        if(position[0] >= tar_pos[0]):
            position = tar_pos
            
        return obj.copy().move_to(position).set_z_index(1)
    
    def Bullet(self, pos):
        return Polygon([-1,-0.5,0], [-1,0.5,0], [0.5,0.5,0], [1.2,0,0], 
                         [0.5,-0.5,0]).set_stroke(width = stroke_width).scale(0.3).move_to(pos)
        
    def construct(self):
       #initial and stylistic parameters
        target_radius = 4
        
        tar_1 = Ellipse(width= target_radius*0.2,height= target_radius, color= WHITE).set_stroke(width = stroke_width)
        tar_2 = tar_1.copy().scale(0.5)
        tar_g = VGroup(tar_1, tar_2)
        tar_g.to_edge(RIGHT, buff = 1)
        
        start_line = Line((-(tar_g.get_critical_point((1,0,0))[0]),2,0),
                          (-(tar_g.get_critical_point((1,0,0))[0]),-2,0)).set_stroke(width = stroke_width)
        barrel = Rectangle(WHITE, 0.5, 1.7).set_stroke(width = stroke_width).move_to(start_line.get_center())
        
        sw_1 = Arc(radius=0.4, start_angle=-PI/2, angle=PI,color = RED).set_stroke(width=stroke_width)
        sw_2 = Arc(radius=0.2, start_angle=-PI/2, angle=PI,color = RED).set_stroke(width=stroke_width).shift([-0.05,0,0])
        sw_3 = Dot(radius = 0.1,color = RED).shift([-0.1,0,0])
        sw_g = VGroup(sw_1, sw_2, sw_3)
        
        bullet = self.Bullet(ORIGIN).next_to(start_line, RIGHT, buff = 0.1)
        sw_g.next_to(start_line, RIGHT, buff = 0.05)

        dist = BraceBetweenPoints(barrel.get_critical_point([1,0,0]), tar_g.get_center()).set_y(tar_g.get_bottom()[1] - 0.5)
        dist_label = MathTex(r"d", color = YELLOW).next_to(dist, DOWN)
        
        #adjustable
        sound_vel = (tar_g.get_center()[0] - start_line.get_center()[0])
        bullet_vel = 0.5*sound_vel
        
        #bullet impact time
        t_impact = ((tar_g.get_center() - start_line.get_center()) / bullet_vel)[0]
        #sound impact time
        t_impact_2 = ((tar_g.get_center() - start_line.get_center()) / sound_vel)[0]
        
        #objects in last scene
        g_1 = VGroup(bullet, barrel, tar_g, dist, dist_label)

        #new equations
        t1 = MathTex(r"x_{f,b} = d = x_{f,s}")
        t2 = MathTex(r"t_{b} = t_s + 1~\text{s}")
        g_2 = VGroup(t1, t2).arrange(DOWN, buff = 0.7).shift([0,1,0])
        
        
###########################################################################################
        
        self.play(FadeIn(g_1))
        self.play(Wait(1.0))
        self.play(Indicate(dist_label, scale_factor= 1.5), run_time = 1.5)
        self.play(Wait(1.0))
        
        self.play(Write(t1))
        
        time_tracker = ValueTracker(0)
        sound_mov = always_redraw(
            lambda: self.moving(sw_g, sound_vel, tar_g.get_center(), time_tracker.get_value())
        )
        bullet_mov = always_redraw(
            lambda: self.moving(bullet, bullet_vel, tar_g.get_center(), time_tracker.get_value())
        )
        sound_mov.set_z_index(1)
        bullet_mov.set_z_index(1)
        
        self.play(Create(bullet_mov), run_time = 0.5)
        self.add(sound_mov)
        self.remove(bullet)
        self.play(time_tracker.animate.set_value(t_impact), rate_func = linear, run_time = 1.5)

        self.play(Wait(1.0))
        self.play(Write(t2))
        self.play(Wait(1.0))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])

class s4(Scene):
    def construct(self):
        title = Title("Constant acceleration kinematic equations", font_size = 60)
        t1 = MathTex(r"x_b(t) = x_{0} + v_b t + \frac{1}{2}a_b t^2")
        t1_1 = MathTex(r"d = v_b t_b")
        t2 = MathTex(r"x_s(t) = x_0 + v_s t + \frac{1}{2}a_s t^2")
        t2_1 = MathTex(r"d = v_s t_s")
        t3 = MathTex(r"x_b = x_s")
        t4 = MathTex(r"v_b t_b = v_s t_s")
        
        g1 = VGroup(title, t1, t2).arrange(DOWN, buff = 2*label_buffer)
        g2 = VGroup(t1_1, t2_1, t3)
        t1_1.move_to(t1)
        t2_1.move_to(t2)
        
        
        self.play(Succession(
            Write(title), Write(t1)
            ))
        self.play(Wait(1))
        self.play(FadeTransformPieces(t1, t1_1))
        self.play(Wait(1))
        self.play(Write(t2))
        self.play(Wait(1))
        self.play(FadeTransformPieces(t2, t2_1))
        self.play(Wait(1))
        self.play(FadeIn(t3), g2.animate.arrange(DOWN, buff = 2*label_buffer).shift([0,-0.5,0]))
        self.play(Wait(1))
        self.play(Succession(
            FadeOut(g2), Write(t4)
            ))
        
        #stitching these scenes together
        t5 = MathTex(r"t_b = t_s + 1~\text{s}")
        t6 = MathTex(r"v_b (t_s + 1~\text{s}) = v_s t_s")
        t7 = MathTex(r"v_b t_s + v_b(1~\text{s}) = v_s t_s")
        t8 = MathTex(r"t_s = \frac{v_b(1~\text{s})}{v_s - v_b}")
        
        g3 = VGroup(t4, t5)
        
        self.play(Wait(1))
        self.play(FadeOut(title), Write(t5), g3.animate.arrange(DOWN, buff = 2*label_buffer))
        self.play(Wait(1))
        self.play(FadeTransform(g3, t6))
        self.play(Wait(1))
        self.play(TransformMatchingShapes(t6,t7))
        self.play(Wait(1))
        self.play(TransformMatchingShapes(t7,t8))
        self.play(Wait(1))
        
        #and these scenes together as well
        
        t9 = MathTex(r"v_b = 300~\text{m/s}")
        t10 = MathTex(r"v_s = 350~\text{m/s}")
        t11 = MathTex(r"t_s = 6~\text{seconds}")
        t12 = MathTex(r"t_b = 7~\text{seconds}")
        
        g4 = VGroup(t9,t10).arrange(RIGHT, buff= 2*label_buffer).shift([0,2,0])
        g5 = VGroup(t11,t12)
        
        self.play(FadeIn(g4))
        self.play(Wait(1))
        self.play(FadeOut(g4), TransformMatchingShapes(t8,t11))
        self.play(Wait(1))
        self.play(g5.animate.arrange(DOWN, buff = 2*label_buffer))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])

class s5(Scene):
    def construct(self):
        t1 = MathTex(r"d = v_b t_b")
        t2 = MathTex(r"d= (300~\text{m/s})(7~\text{s})")
        t3 = MathTex(r"d= 2100~\text{m}")
        
        t4 = MathTex(r"d = v_s t_s")
        t5 = MathTex(r"d = (350~\text{m/s})(6~\text{s})")
        t6 = MathTex(r"d = 2100~\text{m}")
        
        self.play(FadeIn(t1))
        self.play(Wait(1))
        self.play(TransformMatchingShapes(t1,t2))
        self.play(Wait(1))
        self.play(TransformMatchingShapes(t2,t3))
        self.play(Circumscribe(t3), run_time = 1.5)
        self.play(Wait(1))
         
        g1 = VGroup(t3, t4)
        
        self.play(
            FadeIn(t4), 
            g1.animate.arrange(DOWN, buff = 2*label_buffer)
        )
        t5.move_to(t4)
        t6.move_to(t4)
        
        self.play(TransformMatchingShapes(t4,t5))
        self.play(TransformMatchingShapes(t5,t6))
        self.play(Circumscribe(t6))
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])
        
class s6(Scene):
    def moving(self, obj, velocity, tar_pos, t):
        position = [velocity*t,0,0] + obj.get_center()
        if(position[0] >= tar_pos[0]):
            position = tar_pos
            
        return obj.copy().move_to(position).set_z_index(1)
    
    def Bullet(self, pos):
        return Polygon([-1,-0.5,0], [-1,0.5,0], [0.5,0.5,0], [1.2,0,0], 
                         [0.5,-0.5,0]).set_stroke(width = stroke_width).scale(0.3).move_to(pos)
        
    def construct(self):
       #initial and stylistic parameters
        target_radius = 4
        
        tar_1 = Ellipse(width= target_radius*0.2,height= target_radius, color= WHITE).set_stroke(width = stroke_width)
        tar_2 = tar_1.copy().scale(0.5)
        tar_g = VGroup(tar_1, tar_2)
        tar_g.to_edge(RIGHT, buff = 1)
        
        start_line = Line((-(tar_g.get_critical_point((1,0,0))[0]),2,0),
                          (-(tar_g.get_critical_point((1,0,0))[0]),-2,0)).set_stroke(width = stroke_width)
        barrel = Rectangle(WHITE, 0.5, 1.7).set_stroke(width = stroke_width).move_to(start_line.get_center())
        
        sw_1 = Arc(radius=0.4, start_angle=-PI/2, angle=PI,color = RED).set_stroke(width=stroke_width)
        sw_2 = Arc(radius=0.2, start_angle=-PI/2, angle=PI,color = RED).set_stroke(width=stroke_width).shift([-0.05,0,0])
        sw_3 = Dot(radius = 0.1,color = RED).shift([-0.1,0,0])
        sw_g = VGroup(sw_1, sw_2, sw_3)
        
        bullet = self.Bullet(ORIGIN).next_to(start_line, RIGHT, buff = 0.1)
        sw_g.next_to(start_line, RIGHT, buff = 0.05)

        dist = BraceBetweenPoints(barrel.get_critical_point([1,0,0]), tar_g.get_center()).set_y(tar_g.get_bottom()[1] - 0.5)
        dist_label = MathTex(r"d", color = YELLOW).next_to(dist, DOWN)
        
        #adjustable
        sound_vel = (tar_g.get_center()[0] - start_line.get_center()[0])
        bullet_vel = 0.5*sound_vel
        
        #bullet impact time
        t_impact = ((tar_g.get_center() - start_line.get_center()) / bullet_vel)[0]
        #sound impact time
        t_impact_2 = ((tar_g.get_center() - start_line.get_center()) / sound_vel)[0]
        
        #objects in last scene
        g_1 = VGroup(bullet, barrel, tar_g, dist, dist_label)
        
        #label for time tracking
        t1 = MathTex(r"t = ", color = YELLOW, font_size = 80).shift([-0.55,1.5,0])
        post_collision = ValueTracker(0)
        t2 = DecimalNumber(0, num_decimal_places=2, font_size = 80, unit= "s", color = YELLOW).add_updater(lambda d: d.set_value(post_collision.get_value()))
        t2.next_to(t1, RIGHT)

###########################################################################################
        
        self.play(FadeIn(g_1))
        self.play(Wait(1.0))
        self.play(Indicate(dist_label, scale_factor= 1.5), run_time = 1.5)
        self.play(Wait(1.0))
        
        
        time_tracker = ValueTracker(0)
        sound_mov = always_redraw(
            lambda: self.moving(sw_g, sound_vel, tar_g.get_center(), time_tracker.get_value())
        )
        bullet_mov = always_redraw(
            lambda: self.moving(bullet, bullet_vel, tar_g.get_center(), time_tracker.get_value())
        )
        sound_mov.set_z_index(1)
        bullet_mov.set_z_index(1)
        
        self.play(Create(bullet_mov), run_time = 0.5)
        self.add(sound_mov)
        self.remove(bullet)
        self.play(time_tracker.animate.set_value(t_impact_2), rate_func = linear, run_time = 1.5)
        self.play(Wait(1.0))
        self.play(FadeIn(t1), FadeIn(t2))
        self.play(
            post_collision.animate.set_value(1.0),
            time_tracker.animate.set_value(t_impact),
            rate_func = linear, run_time = 1
            )
        self.play(Wait(1))
        
        #outro
        self.play(*[FadeOut(i) for i in self.mobjects])

        