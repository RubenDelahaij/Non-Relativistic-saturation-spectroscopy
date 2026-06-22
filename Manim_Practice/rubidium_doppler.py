from manim import *
import numpy as np


class RubidiumSaturationSpectroscopyCorrected(Scene):

    def construct(self):

        # ============================================================
        # INTRO: ELECTRONIC ABSORPTION LINES
        # ============================================================
        intro_title = Text("Rubidium absorption lines", font_size=36)
        self.play(FadeIn(intro_title), run_time=2.0)
        self.wait(2.5)
        self.play(FadeOut(intro_title), run_time=1.5)

        energy_levels = VGroup(
            Line(LEFT*2, RIGHT*2),
            Line(LEFT*2, RIGHT*2).shift(UP*1.5),
        )

        labels = VGroup(
            Text("Ground state (5S)", font_size=24).next_to(energy_levels[0], LEFT),
            Text("Excited state (5P)", font_size=24).next_to(energy_levels[1], LEFT),
        )

        arrow = Arrow(
            energy_levels[0].get_center(),
            energy_levels[1].get_center(),
            buff=0.1,
            color=YELLOW
        )

        photon_label = Text("Photon absorption → electron excitation", font_size=24)
        photon_label.shift(DOWN*2)

        self.play(Create(energy_levels), Write(labels), run_time=3.0)
        self.play(GrowArrow(arrow), run_time=2.0)
        self.play(Write(photon_label), run_time=2.5)
        self.wait(3)

        self.play(FadeOut(VGroup(energy_levels, labels, arrow, photon_label)))

        # ============================================================
        # TITLE
        # ============================================================
        title = Text("Rubidium Saturation Spectroscopy", font_size=40)
        self.play(FadeIn(title), run_time=2.0)
        self.wait(2.5)
        self.play(FadeOut(title), run_time=1.5)

        divider = Line(UP*3, DOWN*3, color=GREY)
        self.play(Create(divider), run_time=2.0)

        # ============================================================
        # LEFT: SETUP
        # ============================================================
        cell = Rectangle(width=3, height=2.2, color=BLUE).shift(LEFT*3)
        cell_label = Text("Rb Vapour Cell", font_size=24).next_to(cell, UP)

        detector = Rectangle(width=0.9, height=0.9, color=GREEN).move_to(LEFT*0.5)
        det_label = Text("Photodiode", font_size=20).next_to(detector, DOWN)

        probe = Dot(color=RED).move_to(LEFT*6 + DOWN*0.3)
        probe_label = Text("Probe beam", font_size=20).next_to(probe, DOWN)

        probe_beam = Line(probe.get_right(), detector.get_left(), color=RED)

        self.play(Create(cell), Write(cell_label), run_time=2.5)
        self.play(Create(detector), Write(det_label), run_time=2.0)

        self.play(FadeIn(probe), Write(probe_label), run_time=2.0)
        self.play(Create(probe_beam), run_time=2.0)

        self.wait(2)

        # ============================================================
        # DOPPLER BROADENED SPECTRUM
        # ============================================================
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 1, 0.2],
            x_length=5,
            y_length=3
        ).shift(RIGHT*3)

        axis_label = Text("Detuning (MHz)", font_size=20).next_to(axes, DOWN)
        graph_title = Text("Absorption spectrum (Doppler broadened)", font_size=22).next_to(axes, UP)

        self.play(Create(axes), Write(axis_label), Write(graph_title), run_time=3.0)

        def doppler(x, sigma):
            return np.exp(-x**2 / (2*sigma**2))

        broad = axes.plot(lambda x: doppler(x, 1.6), color=BLUE)
        self.play(Create(broad), run_time=2.5)

        self.wait(3)

        # ============================================================
        # PUMP BEAM (ORIGINAL POSITION, UNCHANGED)
        # ============================================================
        pump = Dot(color=PURPLE).move_to(LEFT*0.5 + UP*0.78)
        pump_label = Text("Pump beam", font_size=20).next_to(pump, UP)

        pump_beam = Line(
            LEFT*0.5 + UP*0.78,
            LEFT*4.5 + DOWN*0.55,
            color=PURPLE
        )

        self.play(FadeIn(pump), Write(pump_label), run_time=2.0)
        self.play(Create(pump_beam), run_time=2.5)

        # ============================================================
        # TEXT FIX (POSITION ONLY CHANGE)
        # ============================================================
        pump_note = Text("Counter-propagating pump beam", font_size=20)

        # same place as atoms explanation
        pump_note.shift(LEFT*3 + DOWN*2)

        self.play(Write(pump_note), run_time=2.0)
        self.wait(3)
        self.play(FadeOut(pump_note))

        # ============================================================
        # PHYSICS INTUITION
        # ============================================================
        explanation = VGroup(
            Text("Atoms see Doppler-shifted frequencies (k·v)", font_size=20),
            Text("Pump + probe interact mainly with v ≈ 0 atoms", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT).shift(LEFT*3 + DOWN*2)

        self.play(Write(explanation), run_time=3.0)
        self.wait(4)
        self.play(FadeOut(explanation))

        # ============================================================
        # LAMB DIP
        # ============================================================
        dip_depth = 0.35

        def lamb_dip(x):
            return doppler(x, 1.6) - dip_depth*np.exp(-x**2/(2*0.22**2))

        narrow = axes.plot(lambda x: lamb_dip(x), color=PURPLE)

        self.play(Transform(broad, narrow), run_time=3.0)
        self.wait(4)

        # ============================================================
        # CLEAN EXIT
        # ============================================================
        self.play(
            FadeOut(VGroup(
                cell, cell_label,
                probe, probe_label, probe_beam,
                pump, pump_label, pump_beam,
                detector, det_label,
                axes, axis_label, graph_title, broad,
                divider
            )),
            run_time=3.0
        )

        #end = Text("Doppler-free spectroscopy via saturation", font_size=32)
        #self.play(FadeIn(end), run_time=2.5)
        #self.wait(4)
        #self.play(FadeOut(end), run_time=2.0)