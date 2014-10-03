PageAdapter = require('../../scripts/adapters/page')

describe('Page Adapter', ->
    it('should clear the page', ->
        page = document.createElement('div')
        page.classList.add('page')
        page.innerHTML = 'test'
        document.body.appendChild(page)
        x = new PageAdapter()
        expect(page.innerHTML).to.equal('')
        document.body.removeChild(page)
    )

    it.skip('should should a given title', ->

    )
)
