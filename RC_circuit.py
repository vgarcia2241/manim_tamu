from manim import *
import numpy as np

stroke_width = 20
label_buffer = 0.5
MathTex.set_default(font_size = 80)
Tex.set_default(font_size = 80)
a = 0.7 #width of capacitor and battery objs
b = 0.2 #distance between plates

class s1(Scene):
    def Capacitor(self, direction = True, user_color = WHITE): #create capacitor obj
        middle_side = Rectangle(color = BLACK, height= 2*b, width= 2*a).set_fill(BLACK, 1)
        top_side = Line([-a,b,0], [a,b,0], stroke_width = stroke_width, color = user_color)
        bottom_side = Line([-a,-b,0], [a,-b,0], stroke_width = stroke_width, color = user_color)
        g1 = VGroup(middle_side, top_side, bottom_side)
        if(not direction):
            g1.rotate(PI/2)
        return g1
    
    def Resistor(self, direction = True, user_color = WHITE): #create resistor obj
        #takes in bool for vertical or horizontal orientation
        b = 0.3
        c = 2*a / 7.0
        #3 ups and 3 downs
        #default is horizontal
        back = Rectangle(color=BLACK, height = 2*b + 0.12, width = 2*a - 0.35).set_fill(BLACK, 1)
        l1 = Line([-a,0,0],[-a+c, b, 0])
        l2 = Line([-a+c, b, 0],[-a+2*c, -b, 0])
        l3 = Line([-a+2*c, -b, 0],[-a+3*c,b,0])
        l4 = Line([-a+3*c,b,0],[a-3*c,-b,0])
        l5 = Line([a-3*c,-b,0],[a-2*c, b, 0])
        l6 = Line([a-2*c, b, 0],[a-c, -b,0])
        l7 = Line([a-c, -b,0],[a,0,0])
        lines = VGroup(l1,l2,l3,l4,l5,l6,l7).set_color(user_color)
        squiggle = VGroup(back,l1,l2,l3,l4,l5,l6,l7).set_stroke(width = stroke_width)
        if(not direction): #rotation required
            squiggle.rotate(PI/2, about_point= ORIGIN)
    
        return squiggle
    
    def Battery(self, direction = True, user_color = WHITE):
        c = 0.66*a #width of negative terminal
        
        middle_side = Rectangle(color= BLACK, height=2*b, width = 2*a).set_fill(BLACK,1)
        top_side = Line([-a,b,0], [a,b,0], stroke_width = stroke_width, color = user_color)
        bottom_side = Line([-c,-b,0], [c,-b,0], stroke_width = stroke_width, color = user_color)
        g1 = VGroup(middle_side, top_side, bottom_side)
        if(not direction):
            g1.rotate(PI/2)
        return g1
    
    def construct(self):
        #important points, corners, splittings
        boundary = Rectangle(height = 5, width = 11, stroke_width = stroke_width)
        loop1 = Rectangle(height = 5, width = 0.5*boundary.width, stroke_width = stroke_width).next_to(boundary.get_critical_point([-1,0,0]), buff = 0)
        mid_branch = Line(loop1.get_critical_point([1,1,0]), loop1.get_critical_point([1,-1,0]), stroke_width = stroke_width)
        loop2 = Rectangle(height=5, width= 0.5*boundary.width, stroke_width = stroke_width).next_to(loop1.get_critical_point([1,0,0]), buff = 0)
        #defining circuit path as series of independent lines
        
        test_point = Dot(loop1.get_corner([-1,1,0]))
        cap_1 = self.Capacitor().move_to(boundary.get_critical_point([1,0,0])).shift([0,1,0]).set_z_index(1)
        res_1 = self.Resistor(False).move_to(boundary.get_critical_point([1,0,0])).shift([0,-1,0]).set_z_index(1)
        res_2 = self.Resistor(False).move_to(loop1.get_critical_point([1,0,0])).set_z_index(1)
        bat_1 = self.Battery().move_to(loop1.get_critical_point([-1,0,0])).set_z_index(1)
        total_cir = VGroup(cap_1, res_1, bat_1, res_2) #res_2 does not enjoy being in this group, and won't draw fully if added
        loops = VGroup(loop1, boundary)
        
        #texts 
        tex1 = MathTex(r"Q(t)", color = YELLOW)
        tex2 = MathTex(r"I(t)", color = YELLOW)
        tex3 = MathTex(r"V(t)", color = YELLOW)
        
        ######################################################
        self.play(Create(total_cir), Create(loops))
        self.wait(1)
        self.play(
            Create(loop1.copy().set_color(BLUE)), 
            FadeIn(self.Battery(user_color = BLUE).move_to(bat_1).set_z_index(1.1)), 
            FadeIn(self.Resistor(False, BLUE).move_to(res_2).set_z_index(1.1)),
            run_time = 1.5
        )
        self.wait(1)
        self.play(FadeIn(total_cir.copy().set_z_index(1.2)), FadeIn(loops.copy()))
        self.wait(1)
        self.play(
            Create(boundary.copy().set_color(BLUE)),
            FadeIn(self.Battery(user_color=BLUE).move_to(bat_1).set_z_index(1.3)),
            FadeIn(self.Capacitor(user_color=BLUE).move_to(cap_1).set_z_index(1.3)),
            FadeIn(self.Resistor(False, user_color=BLUE).move_to(res_1).set_z_index(1.3)),
            run_time = 1.5
        )
        self.wait(1)
        self.play(FadeIn(total_cir.copy().set_z_index(1.4)), FadeIn(loops.copy()))
        
        ##########################################################
        '''Showing dots along wires'''
        rate= 2
        loop_a = loop1.width / rate #proportion for specific loop
        loop_b = loop2.height / rate 

        #Rect1 = Rectangle(width=2,height=2).move_to([-1,0,0])
        #self.add(Rect1)

        emfdots1 = VGroup()
        emfdots2 = VGroup()
        new_emfdot1 = Dot(point=loop1.point_from_proportion(0.75), color=RED)
        new_emfdot2 = Dot(point=loop2.point_from_proportion(0.25), color=BLUE_A)
        emfdots1.add(new_emfdot1)
        emfdots2.add(new_emfdot2)
        self.add(emfdots1)
        self.add(emfdots2)
        #self.add(new_emfdot)

        # Variable to control the creation of new dots
        dot_creation_timer1 = ValueTracker(0)
        dot_creation_timer2 = ValueTracker(0)
        time_text = always_redraw(
            lambda: MathTex(f"t={dot_creation_timer1.get_value():.2f}").move_to([0,3,0])
        )
        #time_text.move_to([1,0,0])
        self.add(time_text)

        def UpdateTime1(mob,dt):
            dot_creation_timer1.set_value(dot_creation_timer1.get_value()+dt)
        def UpdateTime2(mob, dt):
            dot_creation_timer2.set_value(dot_creation_timer2.get_value()+dt)

        emfdots1.add_updater(UpdateTime1)
        emfdots2.add_updater(UpdateTime2)

        # Add an updater to create new dots periodically
        def add_new_emfdots1(mob, dt):
            ndots = len(mob)
            if mob[ndots-1].get_center()[0]<-loop_a: 
                new_dot = Dot(point=loop1.point_from_proportion(0.25), color=RED)
                emfdots1.add(new_dot)
        emfdots1.add_updater(add_new_emfdots1)

        def add_new_emfdots2(mob, dt):
            ndots = len(mob)
            if mob[ndots-1].get_center()[1]< loop_b:
                new_dot = Dot(point=loop2.point_from_proportion(0.99), color=BLUE_A)
                emfdots2.add(new_dot)
        emfdots2.add_updater(add_new_emfdots2)

        def move_emfdots_along_path1(mob, dt):
            for dot in mob:
                x = dot.get_center()[0]
                y = dot.get_center()[1] 
            
                if abs(y+(0.5*loop1.height))<0.01:#dot is on path bottom horizontally
                    currentprop = 0.5+0.25*(x+loop1.width)/loop1.width
                elif abs(y-((0.5*loop1.height)))<0.01:#dot is on path top horizontally
                    currentprop = 0.25-0.25*(x+loop1.width)/loop1.width
                else: #dot is on path left vertically
                    currentprop = 0.5-0.25*(y+(loop1.height/2.))/loop1.height
            
                if np.sign(currentprop-1./100) == -1.:
                    newprop = 0.0
                    #self.remove(dot)
                else:
                    newprop = currentprop-1./100

                dot.move_to(loop1.point_from_proportion(newprop))
                '''
                Use circle moving dots py for changing rates
                '''
        emfdots1.add_updater(move_emfdots_along_path1)
        
        def move_emfdots_along_path2(mob, dt):
            for dot in mob:
                x = dot.get_center()[0]
                y = dot.get_center()[1] 
            
                if abs(y+(0.5*loop2.height))<0.01:#dot is on path bottom horizontally
                    currentprop = 0.5+0.25*(x+loop2.width)/loop2.width
                elif abs(y-((0.5*loop2.height)))<0.01:#dot is on path top horizontally
                    currentprop = 0.25-0.25*(x+loop2.width)/loop2.width
                else: #dot is on path left vertically
                    currentprop = 0.5-0.25*(y+(loop2.height/2.))/loop2.height
            
                if np.sign(currentprop-1./100) == -1.:
                    newprop = 0.0
                    #self.remove(dot)
                else:
                    newprop = currentprop-1./100

                dot.move_to(loop2.point_from_proportion(newprop))
        emfdots2.add_updater(move_emfdots_along_path2)
        
        self.wait(5.0)