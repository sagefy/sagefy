"""
Generates Astrolabe icon.
"""

from jinja2 import Template

# Colors ###

light_color = '#ccc7a8'
medium_color = '#625f4a'
dark_color = '#323124'

# Light Colors

light_color = '#fcfcfb'
medium_color = '#ccc7a8'
dark_color = '#969272'

# Attributes ###

attrs = {
    "main_circle": {
        "r": 25.0 / 2,
        "stroke_width": 2.0,
        "stroke": medium_color,

        "pipes": {
            1: {
                "stroke_width": 2.0,
                "stroke": medium_color,
            },

            2: {
                "stroke_width": 2.0,
                "stroke": medium_color,
            },
        },

        "buttresses": {
            "fill": dark_color,
            1: {"rotate": '0'},
            2: {"rotate": '0'},
            3: {"rotate": '90'},
            4: {"rotate": '90'},
            5: {"rotate": '180'},
            6: {"rotate": '180'},
            7: {"rotate": '270'},
            8: {"rotate": '270'},
        }
    },

    "small_circle": {
        "r": 2.5,
        "stroke_width": 1.0,
        "stroke": dark_color,

        "neck": {
            "height": 5.0,
            "stroke_width": 1.5,
            "stroke": medium_color,
        },

        "buttresses": {
            1: {
                "width": 5.0,
                "height": 5.0 / 2,
                "fill": dark_color,
            },

            2: {
                "width": 5.0,
                "height": 5.0 / 2,
                "fill": dark_color,
            },
        }
    },

    "measure": {
        "width": 8.0,
        "height": 5.0,
        "rotate": '-30',
        "fill": light_color,

        "arms": {
            1: {
                "fill": light_color,
            },

            2: {
                "fill": light_color,
            },
        },
    },
}


# Methods ###

def generate(base=10):
    """
    Produce the SVG for the logo
    """

    attrs = get_attrs(base)
    return get_svg(attrs)


def get_attrs(base):
    attrs['width'] = (
        attrs['main_circle']['r'] * 2
        + attrs['main_circle']['stroke_width']  # Half, twice
    )
    attrs['height'] = (
        attrs['width']
        + attrs['small_circle']['neck']['height']
        - attrs['main_circle']['stroke_width'] / 2
        - attrs['small_circle']['stroke_width'] / 2
        + attrs['small_circle']['r'] * 2
        + attrs['small_circle']['stroke_width']  # Half, twice
    )
    attrs['main_circle']['cx'] = attrs['width'] / 2
    attrs['small_circle']['cx'] = attrs['main_circle']['cx']
    attrs['main_circle']['cy'] = attrs['height'] - attrs['main_circle']['cx']
    attrs['small_circle']['cy'] = (
        attrs['small_circle']['stroke_width'] / 2
        + attrs['small_circle']['r']
    )
    attrs['main_circle']['pipes'][1]['x1'] = (
        attrs['main_circle']['pipes'][1]['stroke_width'] / 2
    )
    attrs['main_circle']['pipes'][1]['x2'] = (
        attrs['width']
        - attrs['main_circle']['pipes'][1]['x1']
    )
    attrs['main_circle']['pipes'][1]['y1'] = \
        attrs['main_circle']['pipes'][1]['y2'] = (
            attrs['height'] - (
                attrs['main_circle']['pipes'][1]['stroke_width'] / 2
                + attrs['main_circle']['r']
            )
        )
    attrs['main_circle']['pipes'][2]['x1'] = \
        attrs['main_circle']['pipes'][2]['x2'] = \
        attrs['small_circle']['neck']['x1'] = \
        attrs['small_circle']['neck']['x2'] = (
            attrs['width'] / 2
        )
    attrs['main_circle']['pipes'][2]['y1'] = (
        attrs['height'] - (
            attrs['main_circle']['pipes'][2]['stroke_width'] / 2
            + attrs['main_circle']['r'] * 2
        )
    )
    attrs['main_circle']['pipes'][2]['y2'] = (
        attrs['height'] - (
            attrs['main_circle']['pipes'][2]['stroke_width'] / 2
        )
    )
    attrs['small_circle']['neck']['y1'] = (
        attrs['small_circle']['stroke_width'] / 2
        + attrs['small_circle']['r'] * 2
    )
    attrs['small_circle']['neck']['y2'] = (
        attrs['small_circle']['neck']['y1']
        + attrs['small_circle']['neck']['height']
    )
    attrs['measure']['x'] = (
        attrs['main_circle']['cx']
        - attrs['measure']['width'] / 2
    )
    attrs['measure']['y'] = (
        attrs['main_circle']['cy']
        - attrs['measure']['height'] / 2
    )
    arms_width = (
        attrs['main_circle']['r']
        - attrs['measure']['width'] / 2
    )
    arms_y_center = (
        attrs['main_circle']['pipes'][1]['y1']
    )
    arms1_x1 = (
        attrs['main_circle']['cx']
        + attrs['measure']['width'] / 2
    )
    arms2_x1 = (
        attrs['main_circle']['cx']
        - attrs['measure']['width'] / 2
    )
    attrs['measure']['arms'][1]['d'] = \
        'M %s %s L %s %s Q %s %s %s %s' % (
            # x1
            base * arms1_x1,
            # y1
            base * arms_y_center,
            # x2
            base * (arms1_x1 + arms_width),
            # y2
            base * arms_y_center,
            # xq
            base * (arms1_x1 + arms_width / 2),
            # yq
            base * (
                arms_y_center
                - attrs['measure']['height'] / 2
            ),
            # x3
            base * arms1_x1,
            # y3
            base * (
                arms_y_center
                - attrs['measure']['height'] / 2
            ),
        )
    attrs['measure']['arms'][2]['d'] = \
        'M %s %s L %s %s Q %s %s %s %s' % (
            # x1
            base * arms2_x1,
            # y1
            base * arms_y_center,
            # x2
            base * (arms2_x1 - arms_width),
            # y2
            base * arms_y_center,
            # xq
            base * (arms2_x1 - arms_width / 2),
            # yq
            base * (
                arms_y_center
                + attrs['measure']['height'] / 2
            ),
            # x3
            base * arms2_x1,
            # y3
            base * (
                arms_y_center
                + attrs['measure']['height'] / 2
            )
        )

    s = attrs['main_circle']['pipes'][2]['stroke_width'] / 2
    b = 5.0

    base_path = \
        'M %s %s L %s %s Q %s %s %s %s L %s %s' % (
            # x1
            base * (attrs['main_circle']['pipes'][1]['x1'] + s),
            # y1
            base * (attrs['main_circle']['pipes'][1]['y1'] - s),
            # x2
            base * (attrs['main_circle']['pipes'][1]['x1'] + s + b),
            # y2
            base * (attrs['main_circle']['pipes'][1]['y1'] - s) + 1,
            # xq
            base * (attrs['main_circle']['pipes'][1]['x1'] + s),
            # yq
            base * (attrs['main_circle']['pipes'][1]['y1'] - s),
            # x3
            base * (attrs['main_circle']['pipes'][1]['x1'] + s) + base * 1.5,
            # y3
            base * (attrs['main_circle']['pipes'][1]['y1'] - s - b),
            # x4
            base * (attrs['main_circle']['pipes'][1]['x1'] + s),
            # y4
            base * (attrs['main_circle']['pipes'][1]['y1'] - s - b),
        )

    base_path2 = \
        'M %s %s L %s %s Q %s %s %s %s L %s %s' % (
            # x1
            base * (attrs['main_circle']['pipes'][1]['x1'] + s),
            # y1
            base * (attrs['main_circle']['pipes'][1]['y1'] + s),
            # x2
            base * (attrs['main_circle']['pipes'][1]['x1'] + s + b),
            # y2
            base * (attrs['main_circle']['pipes'][1]['y1'] + s) - 1,
            # xq
            base * (attrs['main_circle']['pipes'][1]['x1'] + s),
            # yq
            base * (attrs['main_circle']['pipes'][1]['y1'] + s),
            # x3
            base * (attrs['main_circle']['pipes'][1]['x1'] + s) + base * 1.5,
            # y3
            base * (attrs['main_circle']['pipes'][1]['y1'] + s + b),
            # x4
            base * (attrs['main_circle']['pipes'][1]['x1'] + s),
            # y4
            base * (attrs['main_circle']['pipes'][1]['y1'] + s + b),
        )

    attrs['main_circle']['buttresses']['d'] = base_path
    attrs['main_circle']['buttresses']['d2'] = base_path2

    scbx1 = (
        attrs['width'] / 2
        - attrs['small_circle']['neck']['stroke_width'] / 2
    )

    scby1 = (attrs['height'] - (
        attrs['main_circle']['pipes'][2]['stroke_width']
        + attrs['main_circle']['r'] * 2
    ))

    attrs['small_circle']['buttresses'][1]['d'] = \
        'M %s %s L %s %s Q %s %s %s %s' % (
            # x1
            base * scbx1,
            # y1
            base * scby1,
            # x2
            base * scbx1 + 1,
            # y2
            base * (
                scby1
                - attrs['small_circle']['neck']['height']
                + attrs['main_circle']['pipes'][2]['stroke_width'] / 2
                + attrs['small_circle']['stroke_width'] / 2
            ),
            # xq
            base * scbx1,
            # yq
            base * scby1,
            # x3
            base * scbx1 - base * 5 + 1,
            # y3
            base * scby1 + base * 1.3
        )

    scbx2 = (
        attrs['width'] / 2
        + attrs['small_circle']['neck']['stroke_width'] / 2
    )

    attrs['small_circle']['buttresses'][2]['d'] = \
        'M %s %s L %s %s Q %s %s %s %s' % (
            # x1
            base * scbx2,
            # y1
            base * scby1,
            # x2
            base * scbx2 - 1,
            # y2
            base * (
                scby1
                - attrs['small_circle']['neck']['height']
                + attrs['main_circle']['pipes'][2]['stroke_width'] / 2
                + attrs['small_circle']['stroke_width'] / 2
            ),
            # xq
            base * scbx2,
            # yq
            base * scby1,
            # x3
            base * scbx2 + base * 5 - 1,
            # y3
            base * scby1 + base * 1.3
        )

    def baseify(ats):
        for key, val in ats.items():
            if isinstance(val, dict):
                baseify(val)
            if isinstance(val, (float, int)):
                ats[key] = val * float(base)

    baseify(attrs)

    return attrs


def get_svg(attrs):
    f = open('astrolabe.svg', 'r').read()
    t = Template(f)
    return t.render(attrs)


if __name__ == "__main__":
    print(generate())
