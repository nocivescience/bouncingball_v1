from manim import *
class Ball(Circle):
        CONIFG={
                "rasius":.3,
                "fill_color":YELLOW,
                "fill_opacity":1,
        }
        def __init__(self,**kwargs):
                Circle.__init__(self,**kwargs) #no coloque el Circle.__init__
                self.velocidad=np.array([2,0,0])
class Box(Rectangle):
        CONFIG={
                "height":6,
                "width":config['frame_width']-2,
                "color":GREEN_C
        }
        def __init__(self,**kwargs):
                Rectangle.__init__(self,**kwargs)
                self.set(width=self.CONFIG['width'])
                self.set(height=self.CONFIG['height'])
class BouncingBall(Scene):
        CONFIG={
                "bouncing_ball":10,
        }
        def construct(self):
                box=Box()
                ball=Ball(color=YELLOW)
                self.play(Create(box))
                self.play(FadeIn(ball))
                def update_ball(ball,dt):
                        ball.aceleration=np.array([0,-5,0])
                        ball.velocidad=ball.velocidad+ball.aceleration*dt
                        ball.shift(ball.velocidad*dt)
                        if ball.get_bottom()[1]>=box.get_bottom()[1] or ball.get_top()[1]<=box.get_top()[1]:
                                ball.velocidad[1]=-ball.velocidad[1]
                        if ball.get_left()[0]<=box.get_left()[0] or ball.get_right()[0]>= box.get_right()[0]:
                                ball.velocidad[0]=-ball.velocidad[0]
                ball.add_updater(update_ball)
                count=self.get_my_count(ball,box)
                self.play(Write(count))
                my_path=self.get_traced_path(ball=ball)
                self.add(ball,my_path)
                self.wait(self.CONFIG['bouncing_ball'])
                ball.clear_updaters()
                self.wait(3)
        def get_traced_path(self,ball):
                path=VMobject()
                path.set_stroke(width=1.3,color=RED)
                path.start_new_path(ball.get_center())
                buff=0.02
                def path_update(path):
                        new_point=ball.get_center()
                        if np.linalg.norm(new_point-path.get_last_point())>buff:
                                path.add_line_to(new_point)
                path.add_updater(path_update)
                return path
        def get_my_count(self,ball,box):
                counter=Integer(0)
                texto=VGroup(MathTex("Colisiones: "), (counter)).arrange(RIGHT,buff=0.1)
                texto.to_edge(UP)
                texto.scale(1)
                counter.ball=ball
                counter.box=box
                counter.hit=False
                def update_colision(counter):
                        dist=abs(counter.box.get_bottom()[1]-counter.ball.get_bottom()[1])   
                        counter.will_be_colision=dist<1
                        if (not counter.hit) and counter.will_be_colision:
                                counter.increment_value()
                        counter.hit=counter.will_be_colision
                counter.add_updater(update_colision)
                return texto