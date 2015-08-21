queryString = require('../../app/modules/query_string')

describe('Query String', ->
    it('should parse the query string', ->
        qs = queryString.get('a=1&b=test&c=true&d=false&e=1.1')
        expect(qs).to.deep.equal({
            a: 1
            b: 'test'
            c: true
            d: false
            e: 1.1
        })
    )
)
