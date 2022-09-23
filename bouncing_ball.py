from manim import *
class BouncingBall(Scene):
        CONFIG={
                "bouncing_ball":35,
        }
        def construct(self):
                box=Box()
                ball=Ball(color=YELLOW)
                self.play(ShowCreation(box))
                self.play(FadeIn(ball))
                def update_ball(ball,dt):
                        ball.aceleration=np.array([0,-5,0])
                        ball.velocidad=ball.velocidad+ball.aceleration*dt
                        ball.shift(ball.velocidad*dt)
                        if ball.get_bottom()[1]<=box.get_bottom()[1]*0.96 or ball.get_top()[1]>=box.get_top()[1]*0.96:
                                ball.velocidad[1]=-ball.velocidad[1]
                        if ball.get_left()[0]<=box.get_left()[0] or ball.get_right()[0]>= box.get_right()[0]:
                                ball.velocidad[0]=-ball.velocidad[0]
                ball.add_updater(update_ball)
                count=self.get_my_count(ball,box)
                self.play(Write(count))
                my_path=self.get_traced_path(ball=ball)
                self.add(ball,my_path)
                self.wait(self.bouncing_ball)
                ball.clear_updaters()
                self.wait(3)
        def get_traced_path(self,ball):
                path=VMobject()
                path.set_stroke(width=1.3,color=RED)
                path.start_new_path(ball.get_center())
                buff=0.02
                def path_update(path):
                        new_point=ball.get_center()
                        if get_norm(new_point-path.get_last_point())>buff:
                                path.add_line_to(new_point)
                path.add_updater(path_update)
                return path
        def get_my_count(self,ball,box):
                counter=Integer(0)
                texto=VGroup(TexMobject("Colisiones: "), (counter)).arrange(RIGHT,buff=0.1)
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