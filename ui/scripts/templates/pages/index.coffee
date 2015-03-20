# TODO move copy to content directory

module.exports = ->
    return '''
    <img src="/astrolabe.svg" id="logo" />
    <hgroup>
        <h1>Sagefy</h1>
        <h3 class="subheader">
            Adaptive, collaborative, and open learning platform.
        </h3>
    </hgroup>
    <p>
        <a href="/log_in">Log In</a> or <a href="/sign_up">Sign Up</a>
    </p>
    <p class="legal">
        &copy; Copyright 2015 Sagefy.
        <a href="/terms">Privacy &amp; Terms</a>.
    </p>
    '''
