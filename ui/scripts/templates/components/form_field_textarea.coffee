module.exports = (data) ->
    return """
    <textarea
        id="#{data.name}"
        name="#{data.name}"
        placeholder="#{data.placeholder or ''}"
        size="#{data.size or ''}"
    >#{data.value or ''}</textarea>
    """
