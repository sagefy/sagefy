PageAdapter = require('./page')
StyleguideView = require('../views/styleguide')

class StyleguideAdapter extends PageAdapter
    url: '/styleguide'
    View: StyleguideView

module.exports = StyleguideAdapter
