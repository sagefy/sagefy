def json_dict_to_html(data):
    """
    Prepend HTML output with the two required tags.
    """

    return '<!doctype html><meta charset="utf-8">' + htmlify(data)


def htmlify(data, depth=1):
    """
    Take a dict in JSONic form and return an HTML document.
    """

    html = ''

    depth = 6 if depth > 6 else depth

    for key, value in data.items():
        html += "<div>"
        html += '<h{depth}>{key}</h{depth}>'.format(key=key, depth=depth)
        if isinstance(value, dict):
            html += htmlify(value, depth + 1)
        elif isinstance(value, (tuple, list)):
            html += '<ul>'
            for list_value in value:
                html += '<li>'
                if isinstance(list_value, dict):
                    html += htmlify(list_value, depth + 1)
                else:
                    html += linkify(str(list_value))
                html += '</li>'
            html += '</ul>'
        else:
            html += "<p>{value}</p>".format(value=linkify(value))
        html += "</div>"

    return html


def linkify(value):
    """
    Create an HTML link when seeing matching content.
    """

    value = str(value)
    value = value.split(' ')
    for i, v in enumerate(value):
        if v.startswith('/') or v.startswith('http'):
            value[i] = '<a href="{v}">{v}</a>'.format(v=v)
    return ' '.join(value)
