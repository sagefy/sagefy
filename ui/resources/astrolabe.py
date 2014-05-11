"""
Generates Astrolabe icon.
"""

from jinja2 import Template

### Colors ###

light_color = '#AAA354'
medium_color = '#6C6733'
dark_color = '#343115'


### Attributes ###

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
            1: {
                "width": 5.0,
                "height": 5.0,
                "fill": dark_color,
            },

            2: {
                "width": 5.0,
                "height": 5.0,
                "fill": dark_color,
            },

            3: {
                "width": 5.0,
                "height": 5.0,
                "fill": dark_color,
            },

            4: {
                "width": 5.0,
                "height": 5.0,
                "fill": dark_color,
            },

            5: {
                "width": 5.0,
                "height": 5.0,
                "fill": dark_color,
            },

            6: {
                "width": 5.0,
                "height": 5.0,
                "fill": dark_color,
            },

            7: {
                "width": 5.0,
                "height": 5.0,
                "fill": dark_color,
            },

            8: {
                "width": 5.0,
                "height": 5.0,
                "fill": dark_color,
            },
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
        "radius": 1.0,
        "rotate": '-30',
        "fill": light_color,

        "arms": {
            1: {
                "width": 5.0 / 2,
                "slice": 0.5,
                "fill": light_color,
            },

            2: {
                "width": 5.0 / 2,
                "slice": 0.5,
                "fill": light_color,
            },
        },
    },
}


### Methods ###

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

    # TODO: measure.arms[1, 2].d
    # TODO: main_circle.buttresses[1..8].d
    # TODO: small_circle.buttresses[1, 2].d

    def baseify(ats):
        for key, val in ats.iteritems():
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
    print generate()
