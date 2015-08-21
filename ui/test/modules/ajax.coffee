
describe('ajax', ->
    beforeEach(->
        @xhr = sinon.useFakeXMLHttpRequest()
        @requests = []
        @xhr.onCreate = (xhr) =>
            @requests.push(xhr)
    )

    afterEach(->
        @xhr.restore()
    )

    it('should make a GET request with no data', ->
        test = {}
        Model::ajax({
            method: 'GET'
            url: '/foo'
            done: (json) -> test = json
        })
        @requests[0].respond(
            200
            {'Content-Type': 'application/json'}
            '{"foo":{"id": 23}}'
        )
        expect(test).to.deep.equal({foo: {id: 23}})
    )

    it('should make a POST request with data', ->
        Model::ajax({
            method: 'POST'
            url: '/foo'
            data: {id: 23}
            done: (json) -> test = json
        })
        expect(@requests[0].requestBody).to.equal(JSON.stringify({id: 23}))
        @requests[0].respond(
            200
            {'Content-Type': 'application/json'}
            '{"foo":{"id": 23}}'
        )
        expect(@requests[0].status).to.equal(200)
    )
)

it('should parse an Ajax error', ->
    expect(Model::parseAjaxErrors({
        responseText: '{"errors":[{"name":"a"}]}'
    })).to.eql([{name: 'a'}])
    expect(Model::parseAjaxErrors({responseText: 'crepe'}))
        .to.equal('crepe')
)
