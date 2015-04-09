from modules.json_dict_to_html import htmlify, linkify, json_dict_to_html


def test_json_dict_to_html():
    """
    Expect to prepend HTML output with the two required tags.
    """

    assert json_dict_to_html({}) == \
        '<!doctype html><meta charset="utf-8">'


def test_htmlify():
    """
    Expect to take a dict in JSONic form and
    return an HTML document.
    """

    # Simple Dict
    assert htmlify({'page': 'profile'}) == \
        '<div><h1>page</h1><p>profile</p></div>'
    # Dict in a Dict
    assert htmlify({'user': {'name': 'Sally'}}) == \
        '<div><h1>user</h1><div><h2>name</h2><p>Sally</p></div></div>'
    # List
    assert htmlify({'friends': ['Haruka', 'Fernando']}) == \
        '<div><h1>friends</h1><ul><li>Haruka</li><li>Fernando</li></ul></div>'
    # List of Dicts
    assert htmlify({'people': [{
        'name': 'Haruka'
    }, {
        'name': 'Fernando'
    }]}) == ''.join([
        '<div>',
        '<h1>people</h1>',
        '<ul>',
        '<li><div><h2>name</h2><p>Haruka</p></div></li>',
        '<li><div><h2>name</h2><p>Fernando</p></div></li>',
        '</ul>',
        '</div>',
    ])


def test_linkify():
    """
    Expect to create an HTML link when seeing matching content.
    """

    assert linkify('http://google.com') == \
        '<a href="http://google.com">http://google.com</a>'
