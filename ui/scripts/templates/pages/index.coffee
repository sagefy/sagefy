module.exports = (data) ->
    html = """
    <img src="/astrolabe.svg" id="logo" />
    <hgroup>
        <h1>Sagefy</h1>
        <h3 class="subheader">
            Adaptive, collaborative, and open learning platform.
        </h3>
    </hgroup>
    """
    if data.isLoggedIn
        html += """
        <ul class="font-size-accent">
            <li>
                <a href="/learn"><i class="fa fa-puzzle-piece"></i> Learn</a>
            </li>
            <li>
                <a href="/contribute"><i class="fa fa-edit"></i> Contribute</a>
            </li>
            <li>
                <a href="/mentor"><i class="fa fa-heart"></i> Mentor</a>
            </li>
            <li>
                <a href="/moderate"><i class="fa fa-group"></i> Moderate</a>
            </li>
            <li>
                <a href="/analyze"><i class="fa fa-bar-chart-o"></i> Analyze</a>
            </li>
        </ul>
        """
    else
        html += """
        <p class="leading">
            <a href="/login">Login</a> or <a href="/signup">Signup</a>
        </p>
        """
    return html
