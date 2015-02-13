Sagefy = require('./modules/sagefy')

document.addEventListener('DOMContentLoaded', ->
    app = new Sagefy(
        require('./adapters/sign_up')
        require('./adapters/log_in')
        require('./adapters/log_out')
        require('./adapters/password')
        require('./adapters/styleguide')
        require('./adapters/terms')
        require('./adapters/contact')
        require('./adapters/settings')
        require('./adapters/notices')
        require('./adapters/search')
        require('./adapters/topic_form')  # Must be before `topic`
        require('./adapters/post_form')
        require('./adapters/topic')
        require('./adapters/card')
        require('./adapters/unit')
        require('./adapters/set')
        require('./adapters/follows')
        require('./adapters/my_sets')
        require('./adapters/choose_unit')
        require('./adapters/card_learn')
        require('./adapters/index')  # Must be 2nd to last
        require('./adapters/error')  # Must be last
    )
    app.route(window.location.pathname)
)
