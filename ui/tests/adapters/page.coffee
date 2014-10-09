PageAdapter = require('../../scripts/adapters/page')

describe('Page Adapter', ->
    beforeEach(->
        @page = document.createElement('div')
        @page.classList.add('page')
        @page.innerHTML = 'test'
        document.body.appendChild(@page)
    )

    afterEach(->
        document.body.removeChild(@page)
    )

    it('should clear the page', ->
        x = new PageAdapter()
        expect(@page.innerHTML).to.equal('')
    )

    it('should should a given title', ->
        class X extends PageAdapter
            title: 'Foo'
        x = new X()
        expect(document.title).to.equal('Foo – Sagefy')
    )
)
