FormAdapter = require('./form')
FormLayoutView = require('../views/layouts/form')
FormView = require('../views/components/form')
PostModel = require('../models/post')

class CreatePostAdapter extends FormAdapter
    url: '/posts/create'
    title: 'Create a New Post'

    render: ->
        return if @requireLogIn()
        super

module.exports = CreatePostAdapter
