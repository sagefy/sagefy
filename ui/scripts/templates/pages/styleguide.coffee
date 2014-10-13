# TODO: trans
module.exports = (data) ->
    return """
    <h1>Style Guide &amp; Component Library</h1>
    <p class="leading">
        Welcome to the Sagefy Style Guide. This page covers the styling and
        conventions of Sagefy user interfaces. This guide also include commonly
        used components. Suggestions are welcome via pull requests.
    </p>
    #{data.html}
    """
