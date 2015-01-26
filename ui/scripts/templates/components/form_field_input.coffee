module.exports = (data) ->
    return """
    <input
        id="#{data.name}"
        name="#{data.name}"
        placeholder="#{data.placeholder or ''}"
        type="#{data.type}"
        value="#{data.value or ''}"
    >
    """
