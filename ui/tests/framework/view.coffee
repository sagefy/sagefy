View = require('../../scripts/framework/view')

describe('View', ->
    it('should call setElement on create', ->
        spy = sinon.spy(View::, 'setElement')
        v = new View()
        expect(spy).to.be.called
        v.remove()
        spy.restore()
    )

    it('should call setRegion on create if region', ->
        spy = sinon.spy(View::, 'setRegion')
        v = new View({region: document.createElement('div')})
        expect(spy).to.be.called
        v.remove()
        spy.restore()
    )

    it('should set the template if provided on create', ->
        template = ->
        v = new View({template: template})
        expect(v.template).to.equal(template)
        v.remove()
    )

    it('should save a provided region', ->
        v = new View()
        region = document.createElement('div')
        v.setRegion(region)
        expect(v.region).to.equal(region)
        v.remove()
    )

    it('should set the el to the region html', ->
        v = new View()
        region = document.createElement('div')
        v.setRegion(region)
        expect(v.region.contains(v.el)).to.be.true
        v.remove()
    )

    it('should set to a provided element', ->
        el = document.createElement('div')
        v = new View()
        v.setElement(el)
        expect(v.el).to.equal(el)
        v.remove()
    )

    it('should create a new element', ->
        class V extends View
            tagName: 'li'
            className: 'notification'
            id: 'first'
        v = new V()
        expect(v.el).to.exist
        expect(v.el.id).to.equal('first')
        expect(v.el.className).to.equal('notification')
        expect(v.el.tagName).to.equal('LI')
        v.remove()
    )

    it('should render with no data', ->
        v = new View()
        expect(-> v.render()).to.not.throw
        v.remove()
    )

    it('should render with data, but no template', ->
        v = new View()
        data = {a: 1}
        v.render(data)
        expect(v.data).to.deep.equal(data)
        v.remove()
    )

    it('should render with data and template', ->
        v = new View({template: (data) -> data.a})
        data = {a: 1}
        v.render(data)
        expect(v.data).to.deep.equal(data)
        expect(v.el.innerHTML).to.equal('' + data.a)
        v.remove()
    )

    it('should delegate events on render', ->
        spy = sinon.spy(View::, 'delegateEvents')
        v = new View()
        v.render()
        expect(spy).to.be.called
        v.remove()
        spy.restore()
    )

    it('should select elements', ->
        class V extends View
            elements: {
                a: '.a'
                b: '#b'
            }
            template: ->
                return '<span class="a"></span><span id="b"></span>'

        v = new V()
        v.render()
        expect(v.a).to.be.instanceof(Element)
        expect(v.b).to.be.instanceOf(Element)
        v.remove()
    )

    it('should unselect elements', ->
        class V extends View
            elements: {
                a: '.a'
                b: '#b'
            }
            template: ->
                return '<span class="a"></span><span id="b"></span>'

        v = new V()
        v.render()
        v.unselectElements()
        expect(v.a).to.not.exist
        expect(v.b).to.not.exist
        v.remove()
    )

    it('should be okay to call delegateEvents with no events', ->
        v = new View()
        expect(-> v.delegateEvents()).to.not.throw
        v.remove()
    )

    it('should delegate a list of events', ->
        class V extends View
            domEvents: {
                'click .button': 'make'
                'submit form': 'submit'
            }
            make: ->
            submit: ->
        v = new V()
        v.render()
        expect(v.domEventKeys).to.contain('click')
        expect(v.domEventKeys).to.contain('submit')
        v.remove()
    )

    it('should trigger a delegated event', ->
        class V extends View
            domEvents: {
                'click .button': 'make'
            }
            make: ->

        spy = sinon.spy(V::, 'make')
        region = document.createElement('div')
        document.body.appendChild(region)
        v = new V({
            template: -> '<a class="button"></a>'
            region: region
        })
        v.render()
        #####
        # This is the deprecated form, but Phantom doesn't like the updated
        # https://github.com/ariya/phantomjs/issues/11289
        evt = document.createEvent('MouseEvent')
        evt.initEvent('click', true, true)
        v.el.querySelector('.button').dispatchEvent(evt)
        #####
        expect(spy).to.be.called  # Why not triggered click?
        v.remove()
        spy.restore()
        document.body.removeChild(region)
    )

    it('should ensure child selector is correct ' +
       'when triggering a delegated event', ->
        class V extends View
            domEvents: {
                'click .button': 'make'
                'click .nottub': 'ekam'
            }
            make: ->
            ekam: ->

        region = document.createElement('div')
        document.body.appendChild(region)
        spy1 = sinon.spy(V::, 'make')
        spy2 = sinon.spy(V::, 'ekam')
        v = new V({
            template: -> '<a class="button"></a><a class="nottub"></a>'
            region: region
        })
        v.render()
        #####
        # This is the deprecated form, but Phantom doesn't like the updated
        # https://github.com/ariya/phantomjs/issues/11289
        evt = document.createEvent('MouseEvent')
        evt.initEvent('click', true, true)
        v.el.querySelector('.button').dispatchEvent(evt)
        #####
        expect(spy2).to.not.be.called
        expect(spy1).to.be.called
        v.remove()
        spy1.restore()
        spy2.restore()
        document.body.removeChild(region)
    )

    it('should be okay to call undelegateEvents ' +
       'with no events', ->
        v = new View()
        expect(-> v.undelegateEvents()).to.not.throw
        v.remove()
    )

    it('should undelegate events', ->
        class V extends View
            domEvents: {
                'click .button': 'make'
                'submit form': 'submit'
            }
        v = new V()
        v.render()
        expect(v.domEventKeys).to.have.length(2)
        v.undelegateEvents()
        expect(v.domEventKeys).to.have.length(0)
        v.remove()
    )
)
