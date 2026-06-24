from manim import *
import numpy as np

class TheUltimateSASMovie(Scene):
    def construct(self):
        def clear_screen():
            self.play(*[FadeOut(mob, shift=DOWN*0.2) for mob in self.mobjects], run_time=1.2)

        def get_glowing_laser(start, end, color=RED, thickness=2, glow_factor=4):
            beam = VGroup()
            beam.add(Line(start, end, color=WHITE, stroke_width=thickness * 0.5))
            for i in range(glow_factor):
                beam.add(Line(
                    start, end, 
                    color=color, 
                    stroke_width=thickness * (i + 1) * 1.5, 
                    stroke_opacity=0.6 / (i + 1)
                ))
            return beam

        def explain_with_arrow(target_mob, text_str, direction=UP, color=YELLOW, font_size=16):
            txt = Text(text_str, font_size=font_size, color=color).add_background_rectangle(opacity=0.9, color=BLACK, buff=0.15).next_to(target_mob, direction, buff=0.8)
            arrow = Arrow(txt.get_edge_center(-direction), target_mob.get_center() + direction*0.2, buff=0.1, color=color)
            group = VGroup(txt, arrow)
            self.play(FadeIn(txt, shift=direction*0.2), GrowArrow(arrow))
            self.wait(2.5)
            self.play(FadeOut(group, shift=-direction*0.2))

        def bottom_info(text_str):
            return Text(text_str, font_size=24).add_background_rectangle(opacity=0.95, color=BLACK, buff=0.15).to_edge(DOWN, buff=0.2)

        # --- CHAPTER 1: INTRO ---
        main_title = Text("Saturated Absorption Spectroscopy", font_size=42, color=YELLOW).to_edge(UP, buff=0.8)
        self.play(Write(main_title, run_time=1.5))

        chapters = VGroup(
            Text("The Anatomy of Light", font_size=24),
            Text("Hyperfine Structure of Rubidium", font_size=24),
            Text("The Doppler Dilemma", font_size=24),
            Text("The Lab Setup (Single Laser)", font_size=24),
            Text("Adding the Pump Beam (Doppler-Free)", font_size=24),
            Text("Velocity Hole Burning", font_size=24),
            Text("The Crossover Resonance", font_size=24),
            Text("Signal Processing & Subtraction", font_size=24),
            Text("Shape Comparison (Normalized)", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(main_title, DOWN, buff=0.8)

        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.5) for c in chapters], lag_ratio=0.1), run_time=3.5)
        self.wait(3)
        clear_screen()

        # --- CHAPTER 2: ANATOMY OF LIGHT ---
        title = Text("The Anatomy of Light", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        info = bottom_info("Light is an oscillating electric and magnetic field.")
        self.play(FadeIn(info, shift=UP*0.2))

        axes_3d_fake = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], x_length=10, y_length=4)
        e_field = axes_3d_fake.plot(lambda x: np.sin(3 * x), color=RED)
        b_field = axes_3d_fake.plot(lambda x: 0.5 * np.sin(3 * x), color=BLUE)
        b_field.stretch(0.5, dim=1).apply_matrix(np.array([[1, 0.5, 0], [0, 1, 0], [0, 0, 1]]))

        e_label = Text("E-Field", font_size=20, color=RED).add_background_rectangle(opacity=0.9, color=BLACK).next_to(e_field, UP, buff=0.6)
        b_label = Text("B-Field", font_size=20, color=BLUE).add_background_rectangle(opacity=0.9, color=BLACK).next_to(b_field, DOWN, buff=0.6)

        self.play(Create(axes_3d_fake), run_time=1)
        self.play(Create(e_field), FadeIn(e_label, shift=UP*0.2), Create(b_field), FadeIn(b_label, shift=DOWN*0.2))
        
        moving_wave = VGroup(e_field, b_field)
        self.play(moving_wave.animate.shift(RIGHT * 2), rate_func=smooth, run_time=2.5)
        clear_screen()

        # --- CHAPTER 3: HYPERFINE STRUCTURE ---
        title = Text("Hyperfine Structure of Rubidium", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        info = bottom_info("Interaction with the atomic nucleus splits the energy levels.")
        self.play(FadeIn(info, shift=UP*0.2))

        l_g = Line(LEFT * 4, LEFT * 1, color=GRAY).shift(DOWN * 1)
        l_e = Line(LEFT * 4, LEFT * 1, color=GRAY).shift(UP * 1)
        
        lg_text = MathTex(r"5^2S_{1/2}", font_size=28).next_to(l_g, LEFT)
        le_text = MathTex(r"5^2P_{3/2}", font_size=28).next_to(l_e, LEFT)

        self.play(Create(l_g), Create(l_e), Write(lg_text), Write(le_text))

        arrow_g1 = DashedLine(l_g.get_right(), RIGHT * 1 + DOWN * 1.5, color=WHITE)
        arrow_g2 = DashedLine(l_g.get_right(), RIGHT * 1 + DOWN * 0.5, color=WHITE)
        
        hf_g1 = Line(RIGHT * 1, RIGHT * 4, color=BLUE_B).shift(DOWN * 1.5)
        hf_g2 = Line(RIGHT * 1, RIGHT * 4, color=BLUE_B).shift(DOWN * 0.5)
        
        fg1_text = MathTex(r"F=1", font_size=24).next_to(hf_g1, RIGHT)
        fg2_text = MathTex(r"F=2", font_size=24).next_to(hf_g2, RIGHT)

        self.play(
            LaggedStart(
                Create(arrow_g1), Create(hf_g1), Write(fg1_text),
                Create(arrow_g2), Create(hf_g2), Write(fg2_text),
                lag_ratio=0.2
            )
        )

        e_lines, e_texts = VGroup(), VGroup()
        for i, f in enumerate([0, 1, 2, 3]):
            y_pos = UP * 0.2 + UP * (i * 0.5)
            arrow = DashedLine(l_e.get_right(), RIGHT * 1 + y_pos, color=WHITE)
            hf_e = Line(RIGHT * 1, RIGHT * 4, color=RED_B).move_to(RIGHT * 2.5 + y_pos)
            text = MathTex(rf"F'={f}", font_size=24).next_to(hf_e, RIGHT)
            e_lines.add(arrow, hf_e)
            e_texts.add(text)

        self.play(LaggedStart(*[Create(mob) for mob in e_lines], lag_ratio=0.1), Write(e_texts), run_time=2.5)
        
        transition = Arrow(hf_g2.get_center(), e_lines[-1].get_center(), color=YELLOW, buff=0.1)
        trans_text = Text("The F=2 -> F'=3 Transition", font_size=20, color=YELLOW).add_background_rectangle(opacity=0.95, color=BLACK).next_to(transition, LEFT, buff=0.6)
        self.play(GrowArrow(transition), FadeIn(trans_text, shift=RIGHT*0.2))
        self.play(Indicate(transition, color=WHITE))
        self.wait(2)
        clear_screen()

        # --- CHAPTER 4: DOPPLER DILEMMA ---
        title = Text("The Doppler Dilemma", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        laser_source = Dot(color=RED, radius=0.2).to_edge(LEFT).shift(UP*0.5)
        laser_text = Text("Laser", font_size=20).next_to(laser_source, DOWN)
        self.play(FadeIn(laser_source, scale=0.5), Write(laser_text))

        atom1, atom2 = Dot(color=WHITE, radius=0.15).move_to(UP * 1.5), Dot(color=WHITE, radius=0.15).move_to(DOWN * 0.5)
        self.play(FadeIn(atom1, scale=0.5), FadeIn(atom2, scale=0.5))

        info = bottom_info("Atoms see a different color of light depending on their motion.")
        self.play(FadeIn(info, shift=UP*0.2))

        arr1 = Arrow(atom1.get_center(), atom1.get_center() + LEFT * 2, color=BLUE)
        arr2 = Arrow(atom2.get_center(), atom2.get_center() + RIGHT * 2, color=RED)
        
        self.play(GrowArrow(arr1), atom1.animate.set_color(BLUE).scale(1.2))
        lbl1 = Text("Sees the laser BLUER", font_size=16, color=BLUE).add_background_rectangle(opacity=0.9, color=BLACK).next_to(arr1, UP)
        
        self.play(GrowArrow(arr2), atom2.animate.set_color(RED).scale(1.2))
        lbl2 = Text("Sees the laser REDDER", font_size=16, color=RED).add_background_rectangle(opacity=0.9, color=BLACK).next_to(arr2, DOWN)
        
        self.play(FadeIn(lbl1, shift=UP*0.1), FadeIn(lbl2, shift=DOWN*0.1))
        self.wait(2)
        clear_screen()

        # --- CHAPTER 5: LAB SETUP (1 LASER) ---
        title = Text("The Lab Setup (1 Laser)", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        laser = RoundedRectangle(corner_radius=0.1, width=1.2, height=0.6, color=WHITE).set_fill(BLACK, 1).move_to(RIGHT*5.5 + DOWN*2)
        laser_text = Text("Laser", font_size=24).move_to(laser)

        isolator = RoundedRectangle(corner_radius=0.2, width=1.4, height=0.8, color=LIGHT_GREY).set_fill(DARK_GRAY, 1).move_to(RIGHT*3.5 + DOWN*2)
        iso_text = Text("Optical\nisolator", font_size=20).move_to(isolator)

        m1_ell = Ellipse(width=0.1, height=0.8, color=BLUE_D).set_fill(BLUE_C, 1).move_to(RIGHT*1.5 + DOWN*2).rotate(-PI/4)
        m1_label = Text("Mirror", font_size=20).next_to(m1_ell, DL, buff=0.1)

        pol = Ellipse(width=1.2, height=0.15, color=DARK_GRAY).set_fill(GRAY, 1).move_to(RIGHT*1.5 + DOWN*0.5)
        pol_label = Text("Polarizer", font_size=20).next_to(pol, RIGHT)

        bs = Square(side_length=0.6, color=BLACK).set_fill(LIGHT_GREY, 0.4).move_to(RIGHT*1.5 + UP*1)
        bs_line = Line(bs.get_corner(DL), bs.get_corner(UR), color=WHITE)
        bs_label = Text("Beam splitter", font_size=20).next_to(bs, RIGHT)

        chamber = Rectangle(width=2.5, height=2, color=WHITE).set_fill("#1F618D", 1).move_to(LEFT*2.5 + UP*1)
        chamber_text = Text("Rubidium\nchamber", font_size=28).move_to(chamber)

        pd = Rectangle(width=0.3, height=1.2, color=WHITE).set_fill("#154360", 1).move_to(LEFT*6 + UP*1)
        pd_label = Text("Photodiode", font_size=20).next_to(pd, DOWN)

        m2_ell = Ellipse(width=0.1, height=0.8, color=BLUE_D).set_fill(BLUE_C, 1).move_to(RIGHT*1.5 + UP*3.0).rotate(PI/4)
        m2_label = Text("Mirror", font_size=20).next_to(m2_ell, UR, buff=0.1)

        m3_ell = Ellipse(width=0.1, height=0.8, color=BLUE_D).set_fill(BLUE_C, 1).move_to(LEFT*5.5 + UP*3.0).rotate(-PI/8)
        m3_label = Text("Mirror", font_size=20).next_to(m3_ell, LEFT, buff=0.1)

        dump = Ellipse(width=0.1, height=0.4, color=WHITE).set_fill(BLACK, 1).move_to(RIGHT*0.5 + DOWN*1.0).rotate(-PI/6)

        base_setup = VGroup(laser, laser_text, isolator, iso_text, m1_ell, m1_label, pol, pol_label, bs, bs_line, bs_label, chamber, chamber_text, pd, pd_label)
        pump_setup = VGroup(m2_ell, m2_label, m3_ell, m3_label, dump)
        
        physical_setup = VGroup(base_setup, pump_setup)
        physical_setup.scale(0.55).move_to(RIGHT * 3.5 + UP * 0.5)

        beam_red_1 = get_glowing_laser(laser.get_left(), isolator.get_right(), color=RED)
        beam_red_2 = get_glowing_laser(isolator.get_left(), m1_ell.get_center(), color=RED)
        beam_red_3 = get_glowing_laser(m1_ell.get_center(), bs.get_bottom(), color=RED)
        beam_probe = get_glowing_laser(bs.get_left(), pd.get_right(), color=PURE_BLUE, thickness=2)

        ax_left = Axes(x_range=[-3, 3, 1], y_range=[0, 1.2, 0.5], x_length=5, y_length=4).move_to(LEFT * 3.5 + UP * 0.5)
        ax_labels = ax_left.get_axis_labels(x_label="Freq", y_label="Transmission")
        
        def doppler_bg(x): return 1.0 - 0.6 * np.exp(-(x - 0.5)**2 / 2)
        curve_bg_left = ax_left.plot(doppler_bg, color=BLUE_D, stroke_width=4)
        lbl_bg_left = Text("Doppler Broadened", font_size=16, color=BLUE_D).add_background_rectangle(opacity=0.9, color=BLACK).next_to(curve_bg_left, UP, buff=0.2)

        self.play(FadeIn(base_setup, shift=UP*0.2), Create(ax_left), Write(ax_labels), run_time=2)
        
        explain_with_arrow(isolator, "Prevents reflections\nback into the laser.", direction=UP)

        self.play(
            LaggedStart(
                Create(beam_red_1), Create(beam_red_2), Create(beam_red_3), Create(beam_probe),
                lag_ratio=0.2
            )
        )
        
        info = bottom_info("A single laser only measures a blurry, broad Doppler absorption.")
        self.play(FadeIn(info, shift=UP*0.2), Create(curve_bg_left), FadeIn(lbl_bg_left, shift=DOWN*0.1))
        self.wait(3)

        # --- CHAPTER 6: ADDING PUMP BEAM ---
        title_new = Text("Adding the Pump Beam (2 Lasers)", font_size=36, color=YELLOW).to_edge(UP)
        self.play(ReplacementTransform(title, title_new))

        beam_pump_1 = get_glowing_laser(bs.get_top(), m2_ell.get_center(), color=GREEN, thickness=3)
        beam_pump_2 = get_glowing_laser(m2_ell.get_center(), m3_ell.get_center(), color=GREEN, thickness=3)
        beam_pump_3 = get_glowing_laser(m3_ell.get_center(), dump.get_center(), color=GREEN, thickness=3)

        intersect_point = chamber.get_center()
        intersect_circle = Circle(radius=0.3, color=YELLOW, stroke_width=4).move_to(intersect_point)
        intersect_text = Text("Intersection", font_size=12, color=YELLOW).add_background_rectangle(opacity=0.9, color=BLACK).next_to(intersect_circle, UP, buff=0.4)

        def lamb_dips(x):
            d1, d2, d3 = 0.15 * (0.1**2 / ((x + 1.5)**2 + 0.1**2)), 0.25 * (0.1**2 / ((x + 0.5)**2 + 0.1**2)), 0.20 * (0.1**2 / ((x)**2 + 0.1**2))
            d4, d5, d6 = 0.35 * (0.1**2 / ((x - 0.8)**2 + 0.1**2)), 0.40 * (0.1**2 / ((x - 1.3)**2 + 0.1**2)), 0.25 * (0.1**2 / ((x - 1.8)**2 + 0.1**2))
            return d1 + d2 + d3 + d4 + d5 + d6
            
        def doppler_free(x): return doppler_bg(x) + lamb_dips(x)

        curve_free_left = ax_left.plot(doppler_free, color=PURPLE, stroke_width=4)
        lbl_free_left = Text("Doppler-Free (Lamb Peaks!)", font_size=16, color=PURPLE).add_background_rectangle(opacity=0.9, color=BLACK).move_to(lbl_bg_left.get_center())

        self.play(FadeIn(pump_setup, scale=0.9))
        self.play(LaggedStart(Create(beam_pump_1), Create(beam_pump_2), Create(beam_pump_3), lag_ratio=0.15))
        self.play(DrawBorderThenFill(intersect_circle), FadeIn(intersect_text, shift=UP*0.1))

        info2 = bottom_info("The Pump laser increases transmission! We see sharp upward peaks.")
        self.play(ReplacementTransform(info, info2))
        
        self.play(ReplacementTransform(curve_bg_left, curve_free_left), ReplacementTransform(lbl_bg_left, lbl_free_left), run_time=2)
        self.play(Indicate(curve_free_left, color=YELLOW, scale_factor=1.05))
        self.wait(4)
        clear_screen()

        # --- CHAPTER 7: HOLE BURNING ---
        title = Text("Velocity Hole Burning", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 1.2, 0.5], x_length=8, y_length=4)
        ax_labels = ax.get_axis_labels(x_label="Velocity (v)", y_label="Population")
        self.play(Create(ax), Write(ax_labels))

        info = bottom_info("The Pump beam excites atoms and 'burns a hole' in the velocity distribution.")
        self.play(FadeIn(info, shift=UP*0.2))

        scan_tracker = ValueTracker(-3)
        mb_curve = ax.plot(lambda x: np.exp(-(x/2)**2), color=DARK_GRAY, stroke_width=2)
        self.play(Create(mb_curve))

        dynamic_hole_curve = always_redraw(
            lambda: ax.plot(
                lambda x: np.exp(-(x/2)**2) - 0.7 * np.exp(-(x/2)**2) * (0.15**2 / ((x - scan_tracker.get_value())**2 + 0.15**2)),
                color=YELLOW, stroke_width=4
            )
        )
        
        laser_pointer = always_redraw(lambda: DashedLine(ax.c2p(scan_tracker.get_value(), 0), ax.c2p(scan_tracker.get_value(), 1), color=RED))
        pointer_label = always_redraw(lambda: Text("Laser Freq", font_size=16, color=RED).add_background_rectangle(opacity=0.9, color=BLACK).next_to(laser_pointer, UP, buff=0.3))

        self.play(FadeIn(dynamic_hole_curve), Create(laser_pointer), FadeIn(pointer_label))
        self.play(scan_tracker.animate.set_value(3), run_time=5, rate_func=smooth)
        self.wait(1)
        clear_screen()

        # --- CHAPTER 8: CROSSOVER RESONANCE ---
        title = Text("The Crossover Resonance", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        mid_atom = Dot(color=YELLOW, radius=0.3)
        self.play(FadeIn(mid_atom, scale=0.5))

        pump_beam = Arrow(LEFT * 4, mid_atom.get_left(), color=GREEN, stroke_width=6)
        probe_beam = Arrow(RIGHT * 4, mid_atom.get_right(), color=BLUE, stroke_width=2)
        
        pump_text = Text("Pump resonant with F'=3", font_size=20, color=GREEN).add_background_rectangle(opacity=0.9, color=BLACK).next_to(pump_beam, UP, buff=0.5)
        probe_text = Text("Probe resonant with F'=2", font_size=20, color=BLUE).add_background_rectangle(opacity=0.9, color=BLACK).next_to(probe_beam, UP, buff=0.5)

        self.play(GrowArrow(pump_beam), FadeIn(pump_text, shift=RIGHT*0.2))
        self.play(GrowArrow(probe_beam), FadeIn(probe_text, shift=LEFT*0.2))

        # Removed the v != 0 section here
        
        crossover_info = Text("Doppler shift causes BOTH lasers to interact simultaneously.\nThis creates extra peaks in the transmission!", font_size=24, color=YELLOW).add_background_rectangle(opacity=0.95, color=BLACK).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(crossover_info, shift=UP*0.3))
        self.play(Wiggle(mid_atom, scale_value=1.3))
        self.wait(3)
        clear_screen()

        # --- CHAPTER 9: SIGNAL PROCESSING ---
        title = Text("Signal Processing & Subtraction", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        diff_ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.2, 0.2], x_length=9, y_length=4).shift(UP*0.5)
        diff_labels = diff_ax.get_axis_labels(x_label="Time (s)", y_label="Voltage (V)")
        self.play(Create(diff_ax), Write(diff_labels))

        def doppler_bg(x): return 1.0 - 0.6 * np.exp(-(x - 0.5)**2 / 2)
        def lamb_dips(x):
            d1, d2, d3 = 0.15 * (0.1**2 / ((x + 1.5)**2 + 0.1**2)), 0.25 * (0.1**2 / ((x + 0.5)**2 + 0.1**2)), 0.20 * (0.1**2 / ((x)**2 + 0.1**2))
            d4, d5, d6 = 0.35 * (0.1**2 / ((x - 0.8)**2 + 0.1**2)), 0.40 * (0.1**2 / ((x - 1.3)**2 + 0.1**2)), 0.25 * (0.1**2 / ((x - 1.8)**2 + 0.1**2))
            return d1 + d2 + d3 + d4 + d5 + d6
            
        def doppler_free(x): return doppler_bg(x) + lamb_dips(x)

        curve_bg = diff_ax.plot(doppler_bg, color=BLUE_D, stroke_width=4)
        lbl_bg = Text("Doppler Absorption", font_size=18, color=BLUE_D).add_background_rectangle(opacity=0.9, color=BLACK).next_to(curve_bg, UP, buff=0.3).shift(LEFT*2)
        self.play(Create(curve_bg), FadeIn(lbl_bg, shift=DOWN*0.1))

        curve_free = diff_ax.plot(doppler_free, color=PURPLE, stroke_width=4)
        lbl_free = Text("Doppler-Free Spectrum", font_size=18, color=PURPLE).add_background_rectangle(opacity=0.9, color=BLACK).next_to(curve_bg, UP, buff=1.2).shift(RIGHT*1.5)
        self.play(Create(curve_free), FadeIn(lbl_free, shift=DOWN*0.1))
        
        info = bottom_info("We see small Lamb peaks in the broad curve. Let's isolate them!")
        self.play(FadeIn(info, shift=UP*0.2))
        self.wait(2)

        difference_area = diff_ax.get_area(curve_free, bounded_graph=curve_bg, color=YELLOW, opacity=0.5)
        self.play(FadeIn(difference_area))
        
        diff_text = Text("Difference = Doppler-Free MINUS Doppler", font_size=20, color=YELLOW).add_background_rectangle(opacity=0.9, color=BLACK).to_edge(UP, buff=1.5)
        self.play(FadeIn(diff_text, shift=DOWN*0.2))
        self.wait(2)

        self.play(FadeOut(curve_bg), FadeOut(curve_free), FadeOut(lbl_bg), FadeOut(lbl_free), FadeOut(diff_text), FadeOut(info))
        
        curve_diff_only = diff_ax.plot(lamb_dips, color=GREEN, stroke_width=4)
        lbl_diff_only = Text("Difference Signal (Isolated Peaks)", font_size=20, color=GREEN).add_background_rectangle(opacity=0.9, color=BLACK).next_to(curve_diff_only, UP, buff=0.8)
        
        info_2 = bottom_info("By subtracting the graphs, we are left with perfect data.")
        self.play(ReplacementTransform(difference_area, curve_diff_only), FadeIn(lbl_diff_only, shift=UP*0.1), FadeIn(info_2, shift=UP*0.2))
        
        crosses = VGroup()
        for peak_x in [-1.5, -0.5, 0, 0.8, 1.3, 1.8]:
            cross = Cross(stroke_color=RED, stroke_width=4, scale_factor=0.1).move_to(diff_ax.c2p(peak_x, lamb_dips(peak_x)))
            crosses.add(cross)
        
        self.play(LaggedStart(*[Create(cross) for cross in crosses], lag_ratio=0.15))
        self.wait(3)
        clear_screen()

        # --- CHAPTER 10: SHAPE COMPARISON ---
        title = Text("Shape Comparison (Normalized)", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        norm_ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.2, 0.2], x_length=9, y_length=5).shift(DOWN*0.5)
        norm_labels = norm_ax.get_axis_labels(x_label="Time (s)", y_label="Relative Amplitude")
        self.play(Create(norm_ax), Write(norm_labels))

        info = bottom_info("We compare measurements with different Pump/Probe ratios.")
        self.play(FadeIn(info, shift=UP*0.2))

        def pseudo_noise(x, offset, freq, amp): return amp * np.sin(freq * x + offset) + (amp/2) * np.cos(freq*2.5 * x - offset)

        bad_curves = VGroup()
        colors = [LIGHT_GREY, LIGHT_BROWN, BLUE_A, TEAL_A, ORANGE]
        
        for i in range(5):
            bad_func = lambda x, i=i: 0.8 * (0.5**2 / ((x - (-1 + i*0.4))**2 + 0.5**2)) + pseudo_noise(x, i, 15, 0.05) + 0.1
            bad_curve = norm_ax.plot(bad_func, color=colors[i], stroke_width=2, stroke_opacity=0.6)
            bad_curves.add(bad_curve)
        
        self.play(LaggedStart(*[Create(curve) for curve in bad_curves], lag_ratio=0.2), run_time=3.5)
        
        bad_lbl = Text("Measurements 2 to 10: Low ratio, high noise, unclear peaks.", font_size=18, color=LIGHT_GREY).add_background_rectangle(opacity=0.9, color=BLACK).to_edge(UP, buff=1.5)
        self.play(FadeIn(bad_lbl, shift=DOWN*0.2))
        self.wait(2)

        def best_data(x): return lamb_dips(x) / 0.40  

        best_curve = norm_ax.plot(best_data, color=WHITE, stroke_width=6)
        best_lbl = Text("Measurement 1 (Ratio 1:355.5) | R² = 0.971 - BEST DATA", font_size=20, color=YELLOW).add_background_rectangle(opacity=0.9, color=BLACK).to_edge(UP, buff=1.5)
        
        self.play(FadeOut(bad_lbl, shift=UP*0.2), Create(best_curve), run_time=2.5)
        self.play(FadeIn(best_lbl, shift=DOWN*0.2), Indicate(best_curve, color=YELLOW))
        
        info_final = bottom_info("With the perfect ratio, a flawless, noise-free quantum spectrum emerges!")
        self.play(ReplacementTransform(info, info_final))
        self.wait(3)

        self.play(
            FadeOut(norm_ax), FadeOut(norm_labels), FadeOut(best_lbl), 
            FadeOut(info_final), FadeOut(title), FadeOut(bad_curves)
        )

        # --- OUTRO: ATOM LOGO & CREDITS ---
        nucleus = Dot(color=RED, radius=0.3)
        orbit1 = Ellipse(width=4.5, height=1.5, color=TEAL).rotate(PI/4)
        orbit2 = Ellipse(width=4.5, height=1.5, color=BLUE).rotate(-PI/4)
        orbit3 = Ellipse(width=4.5, height=1.5, color=PURPLE).rotate(PI/2)
        
        atom_group = VGroup(nucleus, orbit1, orbit2, orbit3).move_to(ORIGIN)
        
        self.play(ReplacementTransform(best_curve, atom_group), run_time=2.5)

        e1 = Dot(color=YELLOW, radius=0.1)
        e2 = Dot(color=YELLOW, radius=0.1)
        e3 = Dot(color=YELLOW, radius=0.1)
        self.play(LaggedStart(*[FadeIn(e, scale=0.5) for e in [e1, e2, e3]], lag_ratio=0.2))

        self.play(
            MoveAlongPath(e1, orbit1),
            MoveAlongPath(e2, orbit2),
            MoveAlongPath(e3, orbit3),
            run_time=3.5,
            rate_func=smooth
        )

        rb_text = MathTex(r"^{87}\text{Rb}", font_size=96, color=YELLOW).move_to(ORIGIN)
        
        self.play(
            FadeOut(e1), FadeOut(e2), FadeOut(e3),
            FadeOut(orbit1), FadeOut(orbit2), FadeOut(orbit3),
            FadeOut(nucleus), # Replaced atom_group morph with cleaner component fades
            FadeIn(rb_text, scale=0.5),
            run_time=1.5
        )

        flash = Flash(ORIGIN, color=YELLOW, line_length=3, num_lines=20, flash_radius=2.0)
        self.play(flash, rb_text.animate.scale(1.5).set_color(RED), run_time=1)
        self.wait(1)
        
        self.play(FadeOut(rb_text, scale=1.2))
        self.wait(0.5)

        credits_title = Text("Credits", font_size=48, color=YELLOW).to_edge(UP, buff=0.8)

        students_col = VGroup(
            Text("Students", font_size=32, color=BLUE_C),
            Text("Hasib Yousuf", font_size=24),
            Text("Ruben Delahaij", font_size=24),
            Text("Fenna Hudson", font_size=24),
            Text("Rostam Kooshani", font_size=24)
        ).arrange(DOWN, buff=0.25)

        staff_col = VGroup(
            Text("Supervisors", font_size=32, color=BLUE_C),
            Text("Bubai Rahaman", font_size=24),
            Text("Pawni Manchanda", font_size=24),
            Rectangle(width=0.1, height=0.4, stroke_opacity=0),
            Text("Project Manager", font_size=32, color=BLUE_C),
            Text("Rene Gerritsma", font_size=24)
        ).arrange(DOWN, buff=0.25)

        credits_layout = VGroup(students_col, staff_col).arrange(RIGHT, buff=2.0, aligned_edge=UP).next_to(credits_title, DOWN, buff=0.8)

        self.play(Write(credits_title))
        self.play(
            LaggedStart(
                FadeIn(students_col, shift=UP * 0.3), 
                FadeIn(staff_col, shift=UP * 0.3),
                lag_ratio=0.3
            ),
            run_time=2.5
        )
        self.wait(5)