const cookie = require('../../app/modules/cookie')

describe('Cookie', () => {
    it('should parse a cookie value', () =>
        expect(cookie.read('"\"+"')).to.equal('" ')
    )

    it('should get a cookie', () => {
        document.cookie = 'test=abcd;path=/;max-age=30'
        expect(cookie.get('test')).to.equal('abcd')
        cookie.unset('test')
    })

    it('should set a cookie', () => {
        cookie.set('test', 'abcd')
        expect(document.cookie).to.contain('test=abcd')
        cookie.unset('test')
    })

    it('should unset a cookie', () => {
        cookie.set('test', 'abcd')
        expect(document.cookie).to.contain('test=abcd')
        cookie.unset('test')
        expect(document.cookie).to.not.contain('test=abcd')
    })
})
