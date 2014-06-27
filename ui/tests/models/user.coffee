UserModel = require('../../scripts/models/user')
_ = require('underscore')

validate = (model, search) ->
    return _.findWhere(
        model.validate(model.toJSON(), {
            fields: Object.keys(model.fields)
        })
        {name: search}
    )

describe('User Model', ->
    before(->
        @ajaxStub = sinon.stub($, 'ajax', -> $({}).promise())
        @user = new UserModel()
    )

    after(->
        @ajaxStub.restore()
        delete @user
    )

    it('should define the appropriate fields', ->
        expect(UserModel::fields).to.contain.keys('username')
            .and.to.contain.keys('email')
            .and.to.contain.keys('password')
    )

    it('should validate the username field correctly', ->
        @user.set('username', '')
        expect(validate(@user, 'username')).to.be.an('object')
        @user.set('username', 'abcd')
        expect(validate(@user, 'username')).to.not.exist
    )

    it('should validate the email address correctly', ->
        @user.set('email', 'asdf')
        expect(validate(@user, 'email')).to.be.an('object')
        @user.set('email', 'a@b.c')
        expect(validate(@user, 'email')).to.not.exist
    )

    it('should validate the password field correctly', ->
        @user.set('password', 'asdf')
        expect(validate(@user, 'password')).to.be.an('object')
        @user.set('password', 'asdfasdf')
        expect(validate(@user, 'password')).to.not.exist
    )

    it('should login a user', ->
        spy = sinon.spy()
        @user.on('login', spy)
        @user.login({username: 'abcd', password: 'asdfasdf'})
        expect(spy).to.be.called
    )

    it('should logout a user', ->
        spy = sinon.spy()
        @user.on('logout', spy)
        @user.logout()
        expect(spy).to.be.called
    )

    it('should get a new password token', ->
        spy = sinon.spy()
        @user.on('passwordToken', spy)
        @user.getPasswordToken()
        expect(spy).to.be.called
    )
)
