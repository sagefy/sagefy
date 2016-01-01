require('../setup')
{
    isLoggedIn
    ucfirst
    underscored
    mergeArraysByKey
    parseFormValues
} = require('../../app/modules/auxiliaries')
cookie = require('../../app/modules/cookie')

describe('Auxiliaries', ->
    it('should detect log in', ->
        cookie.set('logged_in', '1')
        expect(isLoggedIn()).to.be.true
        cookie.set('logged_in', '0')
        expect(isLoggedIn()).to.be.false
        cookie.unset('logged_in')
    )

    it('should capitalize the first letter of a string', ->
        expect(ucfirst('unicorn')).to.equal('Unicorn')
    )

    it('should underscore a name', ->
        expect(underscored('hip-po potu Mus'))
            .to.equal('hip_po_potu_mus')
    )

    it('should merge two arrays by a key', ->
        A = [{k: 0, v: 1}, {k: 1, v: 1}, {k: 3, v: 1}, {k: 7, v: 1}]
        B = [{k: 1, v: 2}, {k: 2, v: 2}, {k: 7, v: 2}, {k: 8, v: 2}]

        expect(mergeArraysByKey(A, B, 'k')).to.deep.equal([
            {k: 0, v: 1}
            {k: 1, v: 2}
            {k: 3, v: 1}
            {k: 2, v: 2}
            {k: 7, v: 2}
            {k: 8, v: 2}
        ])

    )

    it('should parse form values into service friendly data', ->
        values = {
            a: 1
            'b.a': 2
            'b.b.a': 3
            'c.0': 4
            'c.1': 5
            'd.0.a': 6
            'd.0.b': 7
            'd.1.a': 8
            'd.1.b': 9
        }

        expect(parseFormValues(values)).to.deep.equal({
            a: 1
            b: {
                a: 2
                b: {
                    a: 3
                }
            }
            c: [4, 5]
            d: [
                {a: 6, b: 7}
                {a: 8, b: 9}
            ]
        })
    )
)
