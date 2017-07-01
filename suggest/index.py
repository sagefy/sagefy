from random import SystemRandom
import string
import psycopg2
import psycopg2.extras
from cgi import parse_qs
import re
from http.cookies import SimpleCookie
from datetime import datetime, timedelta


random = SystemRandom()

# https://wiki.python.org/moin/EscapingHtml
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&#x27;",
    ">": "&gt;",
    "<": "&lt;",
    "/": "&#x2F;"
}
allowed = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
skip = '&"\'<>/'


def html_escape(text):
    if not isinstance(text, str):
        return None
    return "".join(html_escape_table.get(c, c) for c in text)


def ensure_id(id_):
    if not isinstance(id_, str):
        return None
    return ''.join(filter(lambda x: x in allowed, id_))


def skip_bad(text):
    if not isinstance(text, str):
        return None
    return ''.join(filter(lambda x: x not in skip, text))


def is_email(value):
    """
    Ensure the given value is formatted as an email.
    """

    if value is None:
        return
    return re.match(r'\S+@\S+\.\S+', value)


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


def clean_email(email):
    if email:
        email = skip_bad(email)
        if not is_email(email):
            email = None
    return email


def pull_cookies(environ):
    """
    Pulls and formats cookies stored by user for domain.
    <http://pwp.stevecassidy.net/wsgi/cookies.html>
    """

    cookie = SimpleCookie(environ.get('HTTP_COOKIE', ''))
    return {key: morsel.value for key, morsel in cookie.items()}


def get_session_id(environ):
    """
    """

    cookies = pull_cookies(environ)
    return ensure_id(
        cookies.get('suggest_session_id', uniqid())
    )


def get_set_cookie_header(session_id):
    expires = ((datetime.utcnow() + timedelta(weeks=2))
               .strftime('%a, %d-%b-%Y %H:%M:%S GMT'))
    return ('Set-Cookie', '; '.join([
        'suggest_session_id={session_id}',
        'expires={expires}',
        'Path=/',
        'HttpOnly',
    ]).format(session_id=session_id, expires=expires))


def list_suggests(conn):
    data = None
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        with cur:
            cur.execute("""
                SELECT suggests.*, (
                    SELECT COUNT(*)
                    FROM suggests_followers
                    WHERE suggests_followers.suggest_id = suggests.id
                ) AS COUNT
                FROM suggests
                ORDER BY count DESC, created DESC;
            """)
            data = cur.fetchall()
        data = [row for row in data]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data


def list_my_follows(conn, session_id):
    if not session_id:
        return []
    data = []
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        with cur:
            cur.execute("""
                SELECT *
                FROM suggests_followers
                WHERE session_id=%s
                ORDER BY created DESC;
            """, (ensure_id(session_id),))
            data = cur.fetchall()
        data = [row['suggest_id'] for row in data]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data


def insert_suggest(conn, suggest):
    succeeded = False
    try:
        cur = conn.cursor()
        with cur:
            name = skip_bad(suggest['name'])
            body = skip_bad(suggest['body'])
            id_ = uniqid()
            cur.execute("""
                INSERT INTO suggests
                (id, created, modified, name, body)
                VALUES
                (%s, current_timestamp, current_timestamp, %s, %s)
            """, (id_, name, body))
            conn.commit()
            succeeded = id_
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return succeeded


def insert_follow(conn, follow):
    succeeded = False
    try:
        cur = conn.cursor()
        with cur:
            suggest_id = ensure_id(follow['suggest_id'])
            session_id = ensure_id(follow['session_id'])
            email = clean_email(follow.get('email'))
            user_id = None
            id_ = uniqid()
            cur.execute("""
                INSERT INTO suggests_followers
                (id, created, modified, suggest_id, email, session_id, user_id)
                VALUES
                (%s, current_timestamp, current_timestamp, %s, %s, %s, %s)
            """, (id_, suggest_id, email, session_id, user_id))
            conn.commit()
            succeeded = id_
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return succeeded


stylesheet = """
<style>
    * { font-family: Georgia, serif; }
    html { background: #f9f9f8; color: #31302c; }
    main { max-width: 600px; padding: 1em; margin: 0 auto; }
    a { color: #517b9e; }
    a:hover { color: #76b1e2; }
    h1, h2, h3 { font-weight: normal; }
    h1 { margin-bottom: 0; }
    button, .button { background: #517b9e;
        background-image: linear-gradient(#5d88ac,#486e8d);
        color: white; text-decoration: none; padding: 0.5em 1em;
        border-radius: 2px; border: 0; cursor: pointer; }
    button:hover, .button:hover { background: #76b1e2; color: white;
        background-image: linear-gradient(#83b2da,#5b9ace);
    }
    input[type="text"], input[type="email"], textarea {
        display: block; font-size: 16px; padding: 0.25em 0.5em;
        width: 30em;
        border: 1px solid #a09e91;
    }
    button { display: block; font-size: 16px; }
    .subjects { list-style: none; padding: 0; margin-top: 3em; }
    .subjects li { border-bottom: 1px solid #a09e91; }
    .subjects h3 { margin-bottom: 0; }
    .subjects .count { font-size: 2em; }
    .subjects .votes { float: left; width: 6em; text-align: center; }
    .subjects .info { margin-left: 6em; }
</style>
"""

analytics = """
<script>
    var _gaq = [['_setAccount', 'UA-40497674-1'], ['_trackPageview']];
    (function(d, t) {
        var g = d.createElement(t),
            s = d.getElementsByTagName(t)[0];
        g.src = '//www.google-analytics.com/ga.js';
        s.parentNode.insertBefore(g, s);
    }(document, 'script'));
</script>
"""


def serve(environ, start_response):
    """
    Handle a WSGI request and response.
    """

    try:
        conn = psycopg2.connect(
            "host=localhost dbname=sagefy user=postgres password=postgres"
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print("I cannot connect to PostgresQL.")
        print(error)
    try:
        method = environ['REQUEST_METHOD']
        path = environ['SCRIPT_NAME'] + environ['PATH_INFO']
        if method == 'GET' and path.startswith('/suggest/add'):
            return get_add_form_route(conn, environ, start_response)
        if method == 'POST' and path.startswith('/suggest/add'):
            return post_subject_route(conn, environ, start_response)
        if method == 'GET' and path.startswith('/suggest/upvote'):
            return get_upvote_form(conn, environ, start_response)
        if method == 'POST' and path.startswith('/suggest/upvote'):
            return post_upvote_form(conn, environ, start_response)
        if method == 'GET' and path.startswith("/suggest"):
            return get_homepage_route(conn, environ, start_response)
        start_response('404 Not Found', [
            ('Content-Type', 'text/html; charset=utf-8')
        ])
        html = "404 Not Found"
        conn.close()
        return [html.encode()]
    except Exception as error:  # TODO only locally!!!
        start_response('500 Server Error', [
            ('Content-Type', 'text/html; charset=utf-8')
        ])
        return [str(error).encode()]


def get_homepage_route(conn, environ, start_response):
    """

    """

    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8')
    ])
    suggests = list_suggests(conn)
    suggests_html = '<p><em>No subjects added yet.</em></p>'
    if suggests:
        session_id = get_session_id(environ)
        my_follows = list_my_follows(conn, session_id)
        suggests_html = ''
        for suggest in suggests:
            upvote_html = """
                <p><a href="/suggest/upvote/{id}">+1 Upvote</a></p>
            """.format(id=ensure_id(suggest['id']))
            if suggest['id'] in my_follows:
                upvote_html = """<p><em>√ Upvoted</em></p>"""
            suggests_html += """
                <li>
                    <div class="votes">
                        <span class="count">{count}</span>
                        {upvote_html}
                        <!-- TODO condition if already upvoted -->
                    </div>
                    <div class="info">
                        <h3>{name}</h3>
                        <small>Created {created}</small>
                        <p>{body}</p>
                    </div>
                </li>
            """.format(
                count=(suggest['count']
                       if isinstance(suggest['count'], int)
                       else 0),
                upvote_html=upvote_html,
                name=html_escape(suggest['name']),
                created='{:%Y-%m-%d %H:%M}'.format(suggest['created']),
                body=html_escape(suggest['body'])
            )
        suggests_html = '<ul class="subjects">' + suggests_html + '</ul>'
    html = """
    <!doctype html>
    <title>Suggest Subjects - by Sagefy</title>
    {stylesheet}
    <main>
        <h1>
            Suggest Subjects
            <small>&ndash; by <a href="/">
                <img src="/astrolabe.svg" width="24" /> Sagefy</a></small>
        </h1>
        <p><strong>Can't find a free online learning experience
           for what you want to learn? <br />
           <em>Request and upvote here!</em></strong>
           No sign-up or log-in required.</p>
        <a class="button" href="/suggest/add">
            + Add a new subject
        </a>
        {suggests_html}
        <p><small>You can also post here if you're thinking about building
                  a new online learning experience... see if there's interest.
                  </small></p>
        <p><small>&copy; Copyright 2017 Sagefy.
            All rights reserved.</small></p>
    </main>
    {analytics}
    """.format(
        stylesheet=stylesheet,
        suggests_html=suggests_html,
        analytics=analytics
    )
    return [html.encode()]


def get_add_form_route(conn, environ, start_response):
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
    {analytics}
    """.format(stylesheet=stylesheet, analytics=analytics)
    return [html.encode()]


def post_subject_route(conn, environ, start_response):
    """

    """

    d = read_post_form_data(environ)
    session_id = get_session_id(environ)
    suggest_id = insert_suggest(conn, {
        'name': skip_bad(d.get('name')),
        'body': skip_bad(d.get('body')),
    })
    if not suggest_id:
        start_response('400 Bad Request', [
            ('Content-Type', 'text/html; charset=utf-8')
        ])
        return ['Failed. Press back and try again.'.encode()]
    insert_follow(conn, {
        'email': clean_email(d.get('email')),
        'suggest_id': ensure_id(suggest_id),
        'session_id': session_id,
    })
    start_response('302 Found', [
        get_set_cookie_header(session_id),
        ('Location', '/suggest'),
    ])
    return ['...'.encode()]


def get_upvote_form(conn, environ, start_response):
    """

    """

    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8')
    ])
    path = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    id_ = path.rsplit('/', 1)[-1]
    id_ = ensure_id(id_)
    html = """
    <!doctype html>
    <title>Upvote a Subject - Suggest by Sagefy</title>
    {stylesheet}
    <main>
        <h1>Upvote a Subject</h1>
        <h2>Suggest Subjects by Sagefy</h2>
        <form method="POST">
            <input type="hidden" value="{id}" name="suggest_id" />
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
    {analytics}
    """.format(stylesheet=stylesheet, id=id_, analytics=analytics)
    return [html.encode()]


def read_post_form_data(environ):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)
    d = {k.decode(): v[0].decode() for k, v in d.items()}
    return d


def post_upvote_form(conn, environ, start_response):
    """

    """

    d = read_post_form_data(environ)
    session_id = get_session_id(environ)
    insert_follow(conn, {
        'email': clean_email(d.get('email')),
        'suggest_id': ensure_id(d.get('suggest_id')),
        'session_id': session_id,
    })
    start_response('302 Found', [
        get_set_cookie_header(session_id),
        ('Location', '/suggest'),
    ])
    return ['...'.encode()]
