import numpy as np
from manim import *
from manim import *
import numpy as np

class GasParticles(Scene):
    def construct(self):

        # Vierkante container
        box_size = 6
        box = Square(side_length=box_size, color=WHITE)

        # Aantal deeltjes
        n_particles = 50

        particles = VGroup()

        for _ in range(n_particles):
            x = np.random.uniform(-box_size/2 + 0.1, box_size/2 - 0.1)
            y = np.random.uniform(-box_size/2 + 0.1, box_size/2 - 0.1)

            particle = Dot(
                point=[x, y, 0],
                radius=0.05,
                color=BLUE
            )

            particles.add(particle)

        self.play(Create(box))
        self.play(FadeIn(particles))
        self.wait()

class Atomicphysics(Scene):
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
