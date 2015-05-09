module.exports = (data) ->
    html = ''
    html += "<h1>#{data.title}</h1>" if data.title
    html += "<p>#{data.description}</p>" if data.description
    html += '<div class="form"></div>'
    return html
