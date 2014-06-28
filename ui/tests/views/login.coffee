UserModel = require('../../scripts/models/user')
LoginView = require('../../scripts/views/login')
$ = require('jquery')
require('jquery.cookie')

describe('Login View', ->
    beforeEach(->
        $.removeCookie('logged_in', { path: '/' })
        @model = new UserModel()
        @$test = $('#test')
        @view = new LoginView({
            model: @model
            $region: @$test
        })
    )

    after(->
        @view.remove()
        @$test.empty()
        delete @model
    )

    it('should error if form is submitted empty', ->
        @view.$form.submit()
        expect(@view.$form).to.have('.form-field--error')
    )

    it('should error if password is wrong', ->
        @view.$form.find('#username').val('testuser')
        @view.$form.find('#password').val('wrongpassword')
        @view.loginError([{
            name: 'password'
            message: 'Wrong Password'
        }])
        expect(@view.$form.find('#password').closest('.form-field'))
            .to.have.class('form-field--error')
    )

    it('should login if correct username and email', ->
        ajaxStub = sinon.stub(jQuery, 'ajax', -> $({}).promise())
        @view.$form.find('#username').val('testuser')
        @view.$form.find('#password').val('example1')
        @view.$form.submit()
        expect(ajaxStub).to.have.been.called
        ajaxStub.restore()
    )
)
