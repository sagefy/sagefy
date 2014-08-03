UserModel = require('../../scripts/models/user')
SignupView = require('../../scripts/views/signup')
$ = require('jquery')
require('jquery.cookie')

describe('Signup View', ->
    beforeEach(->
        $.removeCookie('logged_in', { path: '/' })
        @model = new UserModel()
        @$test = $('#test')
        @view = new SignupView({
            model: @model
            $region: @$test
        })
        @ajaxStub = sinon.stub($, 'ajax', -> $({}).promise())
    )

    afterEach(->
        @view.remove()
        @$test.empty()
        delete @model
        @ajaxStub.restore()
    )

    it('should error on empty name', ->
        @view.$form.submit()
        expect(@view.$('#name').closest('.form-field'))
            .to.have.class('form-field--error')
    )

    it('should error on invalid email address', ->
        @view.$('#email').val('fdsa')
        @view.$form.submit()
        expect(@view.$('#email').closest('.form-field'))
            .to.have.class('form-field--error')
    )

    it('should error if password less than 8 characters', ->
        @view.$('#password').val('fdsa')
        @view.$form.submit()
        expect(@view.$('#password').closest('.form-field'))
            .to.have.class('form-field--error')
    )

    it('should error if email address already used', ->
        @view.$('#name').val('used')
        @view.$('#email').val('used@example.com')
        @view.$('#password').val('example1')
        @view.$form.submit()
        @model.trigger('error', @model, {
            responseText: '{"errors":[{"name":"email","message":"a"}]}'
        })
        expect(@view.$('#email').closest('.form-field'))
            .to.have.class('form-field--error')
    )

    it('should create user when the form is submitted', ->
        stub = sinon.stub(SignupView::, 'sync')
        @view.$('#name').val('testuser')
        @view.$('#email').val('testuser@example.com')
        @view.$('#password').val('example1')
        @view.$form.submit()
        @model.trigger('sync')
        # TODO: expect(stub).to.have.been.called
        stub.restore()
    )
)
