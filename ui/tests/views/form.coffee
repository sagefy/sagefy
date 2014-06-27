$ = require('jquery')
Handlebars = require('hbsfy/runtime')
hbsHelpers = require('../../scripts/modules/hbs_helpers')(Handlebars)
Backbone = require('backbone')
mixins = require('../../scripts/modules/mixins')
FormView = require('../../scripts/views/form')

class XModel extends Backbone.Model
    url: '/'

    fields: {
        name: {
            title: 'Name'
            type: 'text'
            validations: {
                required: true
            }
        }
        other: {
            title: 'Other'
            type: 'text'
            validations: {
                required: true
            }
        }
    }

    validate: mixins.validateModelFromFields
    parseAjaxErrors: mixins.parseAjaxErrors

class XForm extends FormView
    title: 'X'
    fields: ['name']

describe('Form View', ->
    beforeEach(->
        @$test = $('#test')
        @model = new XModel()
        @form = new XForm({
            model: @model
            $region: @$test
        })
        @ajaxStub = sinon.stub($, 'ajax', -> $({}).promise())
    )

    afterEach(->
        @ajaxStub.restore()
        @model = null
        @form.remove()
        @$test.empty()
    )

    it('should retrieve the model in edit mode', ->
        XForm::mode = 'edit'
        stub = sinon.stub(XModel::, 'fetch')
        @form = new XForm({
            model: @model
            $region: @$test
        })
        expect(stub).to.have.been.called
        stub.restore()
        XForm::mode = null
    )

    it('should render a HTML field for each requested field in the model', ->
        expect(@$test.find('.form-field--text')).to.exist
        expect(@$test.find('input#name')).to.exist
    )

    it('should only use the fields specified by the child view', ->
        expect(@$test.find('input#other')).to.not.exist
    )

    it('should validate fields after submitting form', ->
        stub = sinon.stub(XModel::, 'validate')
        @form.$form.submit()
        expect(stub).to.have.been.called
        stub.restore()
    )

    it('should save the model when the fields are completely valid', ->
        @form.$form.find('input#name').val('something')
        expect(@$test.find('input#name').val()).to.equal('something')
        @form.$form.submit()
        expect(@ajaxStub).to.have.been.called
    )

    it('should show errors when the model can\'t be saved', ->
        @model.trigger('error', @model, {
            responseText: '{"errors":[{"name":"name","message":"a"}]}'
        })
        expect(@$test).to.have('.form-field--error')
    )

    it('should show errors when the field fails validation', (done) ->
        @form.$form.find('input').keyup()
        setTimeout(=>  # TODO: how to get around debounce?
            expect(@$test.find('.form-field--error')).to.exist
            done()
        , 110)
    )

    it('should show valid when the field is valid', (done) ->
        @form.$form.find('input').val('something').keyup()
        setTimeout(=>  # TODO: how to get around debounce?
            expect(@$test.find('.form-field--success')).to.exist
            done()
        , 110)
    )
)
