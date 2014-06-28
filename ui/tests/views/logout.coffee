UserModel = require('../../scripts/models/user')
LogoutView = require('../../scripts/views/logout')
$ = require('jquery')
require('jquery.cookie')

describe('Logout View', ->
    beforeEach(->
        $.cookie('logged_in', '1', {expires: 7, path: '/'})
    )

    after(->
        $.removeCookie('logged_in', {path: '/'})
    )

    it('should log out a user', ->
        stub = sinon.stub(LogoutView::, 'logout')
        ajaxStub = sinon.stub(jQuery, 'ajax', -> $({}).promise())
        model = new UserModel()
        view = new LogoutView({model: model})
        expect(ajaxStub).to.have.been.called
        expect(stub).to.have.been.called
        stub.restore()
        ajaxStub.restore()
    )
)
