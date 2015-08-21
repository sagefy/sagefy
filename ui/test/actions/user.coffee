UserModel = require('../../app/models/user')

validate = (model, search) ->
    errors = model.validate()
    for error in errors
        if error.name is search
            return error

describe('user actions', ->
    beforeEach(->
        @xhr = sinon.useFakeXMLHttpRequest()
        @requests = []
        @xhr.onCreate = (xhr) =>
            @requests.push(xhr)
        @user = new UserModel()
    )

    afterEach(->
        delete @user
        @xhr.restore()
    )

    it('should define the appropriate fields', ->
        expect(UserModel::schema).to.contain.keys('name')
            .and.to.contain.keys('email')
            .and.to.contain.keys('password')
    )

    it('should validate the name field correctly', ->
        @user.set('name', '')
        expect(validate(@user, 'name')).to.be.an('object')
        @user.set('name', 'abcd')
        expect(validate(@user, 'name')).to.not.exist
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

    it('should log in a user', ->
        spy = sinon.spy()
        @user.on('logIn', spy)
        @user.logIn({name: 'abcd', password: 'asdfasdf'})
        @requests[0].respond(
            204
            {'Content-Type': 'application/json'}
            ''
        )
        expect(spy).to.be.called
    )

    it('should log out a user', ->
        spy = sinon.spy()
        @user.on('logOut', spy)
        @user.logOut()
        @requests[0].respond(
            204
            {'Content-Type': 'application/json'}
            ''
        )
        expect(spy).to.be.called
    )

    it('should get a new password token', ->
        spy = sinon.spy()
        @user.on('passwordToken', spy)
        @user.getPasswordToken()
        @requests[0].respond(
            204
            {'Content-Type': 'application/json'}
            ''
        )
        expect(spy).to.be.called
    )
)
