module.exports = (data) -> return """
    <li class="menu__item">
        <a href="#{data.url}">
            <i class="fa fa-#{data.icon}"></i>
            <div class="menu__item__title">#{data.title}</div>
        </a>
    </li>
"""
