from manim import *


class PendulumBob(Scene):
    def construct(self):

        title = Text("Simple Pendulum Animation")
        title.to_edge(UP)
        self.play(Write(title))


        pivot = UP * 2

        bob = Circle(
            radius=0.4,
            color=WHITE,
            fill_color=BLUE,
            fill_opacity=0.8
        )
        bob.move_to(DOWN * 1.5)

        string = Line(
            start=pivot,
            end=bob.get_center()
        )

        pendulum = VGroup(string, bob)


        self.play(Create(string))
        self.play(GrowFromCenter(bob))
        self.wait()


        self.play(
            Rotate(pendulum, angle=70 * DEGREES, about_point=pivot),
            run_time=1,
            rate_func=smooth
        )

        self.play(
            Rotate(pendulum, angle=-140 * DEGREES, about_point=pivot),
            run_time=2,
            rate_func=smooth
        )

        self.play(
            Rotate(pendulum, angle=140 * DEGREES, about_point=pivot),
            run_time=2,
            rate_func=smooth
        )

        self.play(
            Rotate(pendulum, angle=-70 * DEGREES, about_point=pivot),
            run_time=1,
            rate_func=smooth
        )

        self.wait()