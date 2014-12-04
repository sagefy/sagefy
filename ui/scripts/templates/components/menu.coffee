# TODO: move copy to content directory
module.exports = ->
    return """
    <div class="menu__overlay"></div>
    <a href="#" class="menu__trigger" data-title="Menu">
        <div class="menu__logo"></div>
        <i class="menu__close fa fa-times-circle"></i>
    </a>
    <ul class="menu__items"></ul>
    """
