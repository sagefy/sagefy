from random import SystemRandom
import string


random = SystemRandom()


def uniqid():
    """
    Generate a unique string with 24 characters.
    https://stackoverflow.com/a/2257449
    """
    return ''.join(
        random.choice(string.ascii_lowercase
                      + string.ascii_uppercase
                      + string.digits)
        for i in range(24)
    )


stylesheet = """
<style>
    * { font-family: Georgia, serif; }
    html { background: #f9f9f8; color: #31302c; }
    main { max-width: 600px; padding: 1em; margin: 0 auto; }
    a { color: #517b9e; }
    a:hover { color: #76b1e2; }
    h1, h2, h3 { font-weight: normal; }
    h1 { margin: 0; }
    h2 { text-indent: 2em; margin-top: 0; font-style: italic; }
    button, .button { background: #517b9e; color: white;
        text-decoration: none; padding: 0.5em 1em;
        border-radius: 5px; border: 0; cursor: pointer; }
    button:hover, .button:hover { background: #76b1e2; color: white; }
    input[type="text"], input[type="email"], textarea {
        display: block; font-size: 16px; padding: 0.25em 0.5em;
        width: 30em;
        border: 1px solid #a09e91;
    }
    button { display: block; font-size: 16px; }
    .subjects { list-style: none; padding: 0; margin-top: 2em; }
    .subjects li { border-bottom: 1px solid #a09e91; }
    .subjects h3 { margin-bottom: 0; }
    .subjects .count { font-size: 2em; }
    .subjects .votes { float: left; width: 6em; text-align: center; }
    .subjects .info { margin-left: 6em; }
</style>
"""


def serve(environ, start_response):
    """
    Handle a WSGI request and response.
    """

    method = environ['REQUEST_METHOD']
    path = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    if method == 'GET' and path.startswith('/suggest/add'):
        return get_add_form_route(environ, start_response)
    if method == 'POST' and path.startswith('/suggest/add'):
        return post_subject_route(environ, start_response)
    if method == 'GET' and path.startswith('/suggest/upvote'):
        return get_upvote_form(environ, start_response)
    if method == 'POST' and path.startswith('/suggest/upvote'):
        return post_upvote_form(environ, start_response)
    if method == 'GET' and path.startswith("/suggest"):
        return get_homepage_route(environ, start_response)
    start_response('404 Not Found', [
        ('Content-Type', 'text/html; charset=utf-8')
    ])
    html = "404 Not Found"
    return [html.encode()]

    # db_conn = make_db_connection()
    # request = construct_request(environ, db_conn)
    # code, data = call_handler(request)
    # close_db_connection(db_conn)
    # response_headers = [('Content-Type', 'application/json; charset=utf-8')]
    # if isinstance(data, dict):
    #     response_headers += set_cookie_headers(data.pop('cookies', {}))
    # status = str(code) + ' ' + status_codes.get(code, 'Unknown')
    # start_response(status, response_headers)
    # if isinstance(data, str):
    #     body = data.encode()
    # elif isinstance(data, dict):
    #     body = json.dumps(data, default=json_serial, ensure_ascii=False)
    #     body = body.encode()
    # return [body]


def get_homepage_route(environ, start_response):
    """

    """

    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8')
    ])
    html = """
    <!doctype html>
    <title>Suggest Subjects - by Sagefy</title>
    {stylesheet}
    <main>
        <h1>Suggest Subjects</h1>
        <h2>by <a href="/">Sagefy</a></h2>
        <p><strong>Can't find a free online learning experience
           for what you want to learn? <br />
           <em>Request and upvote here!</em></strong></p>
        <p>You can also post here if you're thinking about building <br />
            a new online learning experience... see if there's interest.</p>
        <p>No sign-up or log-in required.</p>
        <a class="button" href="/suggest/add">
            + Add a new subject
        </a>
        <p><em>No subjects added yet.</em></p>
        <ul class="subjects">
            <li>
                <div class="votes">
                    <span class="count">45</span>
                    <p><a href="/suggest/upvote/abcd1234">Upvote</a></p>
                </div>
                <div class="info">
                    <h3>Introduction to American Sign Language</h3>
                    <small>Created 45 minutes ago</small>
                    <p>I want to see you juicy wiggle.</p>
                </div>
            </li>
            <li>
                <div class="votes">
                    <span class="count">1032</span>
                    <p><a href="/suggest/upvote/abcd1234">Upvote</a></p>
                </div>
                <div class="info">
                    <h3>Introduction to American Sign Language</h3>
                    <small>Created 45 minutes ago</small>
                    <p>I want to see you juicy wiggle.</p>
                </div>
            </li>
        </ul>
        <p><small>&copy; Copyright 2017 Sagefy.
            All rights reserved.</small></p>
    </main>
    """.format(stylesheet=stylesheet)
    return [html.encode()]


def get_add_form_route(environ, start_response):
    """

    """

    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8')
    ])
    html = """
    <!doctype html>
    <title>Request a New Subject - Suggest by Sagefy</title>
    {stylesheet}
    <main>
        <h1>Request a New Subject</h1>
        <h2>Suggest Subjects by Sagefy</h2>
        <form method="POST">
            <p>
                <label for="name">Subject Name</label>
                <input type="text" name="name" id="name" />
            </p>
            <p>
                <label for="body">Brief Description of Scope</label>
                <textarea name="body" rows="4" id="body"></textarea>
            </p>
            <p>
                <label for="email">Your Email Address (optional)</label>
                <input type="email" name="email" id="email" />
                <small>If you provide your email address
                    we will send you updates.</small>
            </p>
            <button type="submit">
                + Add Subject to List
            </button>
        </form>
    </main>
    """.format(stylesheet=stylesheet)
    return [html.encode()]


def post_subject_route(environ, start_response):
    """

    """


def get_upvote_form(environ, start_response):
    """

    """

    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8')
    ])
    path = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    id_ = path.rsplit('/', 1)[-1]
    allowed = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    id_ = ''.join(filter(lambda x: x in allowed, id_))
    html = """
    <!doctype html>
    <title>Upvote a Subject - Suggest by Sagefy</title>
    {stylesheet}
    <main>
        <h1>Upvote a Subject</h1>
        <h2>Suggest Subjects by Sagefy</h2>
        <form method="POST">
            <input type="hidden" value="{id}" />
            <p>
                <label for="email">Your Email Address (optional)</label>
                <input type="email" name="email" id="email" />
                <small>If you provide your email address
                    we will send you updates.</small>
            </p>
            <button type="submit">
                +1 Upvote Subject
            </button>
        </form>
    </main>
    """.format(stylesheet=stylesheet, id=id_)
    return [html.encode()]


def post_upvote_form(environ, start_response):
    """

    """
