module.exports = (data) ->
    html = ''

    if data.title
        html += "<h1>#{data.title}</h1>"

    if data.description
        html += "<p>#{data.description}</p>"

    html += '<div class="form"></div>'

    return html
