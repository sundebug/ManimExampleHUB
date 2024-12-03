from manimlib import *
from RunScene import generate_label


class Rtat(Scene):  # Right triangle altitude theorem
	def construct(self):
		A, B, C, D = ((0, 2, 0), (-4, 0, 0), (1, 0, 0), ORIGIN)

		tri = Polygon(A, B, D, C)
		tri_ACD = Polygon(A, C, D, fill_color=GREEN_D, fill_opacity=0.5)
		tri_ABD = Polygon(A, B, D, fill_color=LIGHT_PINK, fill_opacity=0.5)
		height_AD = Line(A, D)
		vg = VGroup(tri, tri_ABD, tri_ACD, height_AD)
		for t, v, d in zip(
				["A", "B", "D", "C"],
				tri.get_vertices(),
				(UP, LEFT, DOWN, DOWN),
		):
			vg.add(Text(t).next_to(v, d))
		vg.align_on_border(UL).shift(RIGHT * 1.5)
        # 将程序目录加入到python路径中
		tri_ACD.generate_target().rotate(
				PI / 2, about_point=tri_ACD.get_points()[4]
		).next_to(tri, RIGHT, aligned_edge=DOWN, buff=2)
		self.add(vg)

		tri_ACD_label = generate_label(
				["A", "C", "D"], tri_ACD.target.get_vertices(), [DOWN, UP, DOWN]
		)
		tri1 = VGroup(*[vg[i] for i in [4, 6, 7]]).copy()
		ag = AnimationGroup(
				MoveToTarget(
						tri_ACD,
				),
				Transform(
						tri1,
						VGroup(*tri_ACD_label),
				),
		)
		self.play(ag, lag_ratio=0)
		polyline_AC_AD = Polyline(
				*[tri_ACD.get_vertices()[p] for p in [0, 2, 1]], color=GREEN_C
		)
		polyline_BD_DA = Polyline(
				*[tri_ABD.get_vertices()[p] for p in [1, 2, 0]], color=LIGHT_PINK
		)

		self.add(polyline_AC_AD, polyline_BD_DA)
		tex_string = [R"\frac{BD}{DA}", "=", R"\frac{AC}{DA}"]
		rtat_formular = (
			Tex(*tex_string, t2c={tex_string[0]: PINK, tex_string[2]: GREEN_C})
			.align_on_border(DL)
			.shift(RIGHT * 3)
		)
		self.play(
				Transform(polyline_BD_DA, rtat_formular[tex_string[0]]),
				Transform(polyline_AC_AD, rtat_formular[tex_string[2]]),
				lag_ratio=0,
		)
		self.play(FadeIn(rtat_formular[tex_string[1]]))
		self.play(
				FadeInFromPoint(
						Tex(R"\Rightarrow AD^2=BD \times AC").next_to(
								rtat_formular,
								RIGHT,
						),
						rtat_formular.get_edge_center(RIGHT),
				)
		)


if __name__ == '__main__':
	from RunScene import runScene

	runScene(Rtat)
