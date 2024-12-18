from manimlib import *


class hand2hand(Scene):

    def construct(self):

        self.camera.frame.shift(LEFT)
        angle = PI / 2
        angle_between = PI / 4
        origin_vector = np.array([1, 2, 0])
        v_list = [
            origin_vector,
            rotate_vector(origin_vector * np.sqrt(2), angle_between),
            rotate_vector(origin_vector, angle),
            rotate_vector(origin_vector * np.sqrt(2), angle + angle_between),
        ]
        poly_1 = Polygon(ORIGIN, v_list[0], v_list[2], color=GREEN_D, fill_opacity=0)
        poly_2 = Polygon(ORIGIN, v_list[1], v_list[3], color=YELLOW_D, fill_opacity=0)
        poly_3 = always_redraw(
            lambda: Polygon(poly_1.get_anchors()[1], poly_2.get_anchors()[1], ORIGIN)
            .set_fill(GREY_D, 0.5)
            .set_stroke(opacity=0)
        )

        poly_4 = always_redraw(
            lambda: Polygon(poly_1.get_anchors()[2], poly_2.get_anchors()[2], ORIGIN)
            .set_fill(MAROON_D, 0.5)
            .set_stroke(opacity=0)
        )
        l_1 = always_redraw(
            lambda: DashedLine(
                poly_1.get_vertices()[1], poly_2.get_vertices()[1]
            ).set_color(RED_D)
        )
        l_2 = always_redraw(
            lambda: DashedLine(
                poly_1.get_vertices()[2], poly_2.get_vertices()[2]
            ).set_color(RED_D)
        )

        poly_label = [Text(m).set_color(YELLOW) for m in ["A", "B", "C", "D"]]
        list(
            map(
                lambda m: always(m[0].next_to, m[1], UP),
                zip(
                    poly_label, [*poly_1.get_vertices()[1:], *poly_2.get_vertices()[1:]]
                ),
            )
        )
        arc = always_redraw(
            lambda: Arc(
                start_angle=angle_of_vector(v_list[0]),
                angle=angle_between_vectors(v_list[0], poly_2.get_vertices()[1]),
                radius=np.sqrt(5) / 3,
                color=GREY,
            )
        )
        arc1 = always_redraw(
            lambda: Arc(
                start_angle=angle_of_vector(v_list[2]),
                angle=angle_between_vectors(v_list[2], poly_2.get_vertices()[2]),
                radius=np.sqrt(5) / 3.5,
                color=MAROON,
            )
        )
        self.add(Text("O").next_to(ORIGIN))
        self.add(poly_1, poly_2, l_1, l_2, poly_3, poly_4)
        self.add(*poly_label)
        self.add(arc, arc1)
        self.add(
            Tex(
                r"手拉手:& \triangle{OAC}\cong \triangle{OBD} \\ &\angle{OAC} = \angle{OBD} \\&OA=OB  \\&OC=OD ",
                font_size=32,
                t2c={"手拉手": RED},
            ).next_to(TOP + LEFT_SIDE, direction=DOWN + RIGHT)
        )

        self.play(Rotating(poly_2, angle=PI / 2, run_time=15))


if __name__ == "__main__":
    from RunScene import runScene

    runScene(hand2hand)
