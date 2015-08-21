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
