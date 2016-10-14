const Events = require('../../app/modules/events')

let e
let ting
let f

describe('Events', function () {
    beforeEach(function () {
        e = new Events()
        ting = false
        f = function (a) {
            ting = a || true
        }
    })

    after(function () {
        e = null
    })

    it('should register an event', function () {
        e.on('poke', f)
        expect(e.events.poke).to.be.an('array')
        expect(e.events.poke[0]).to.be.a('function')
    })

    it('should register only one binding per event', function () {
        e.on('poke', f)
        e.on('poke', f)
        expect(e.events.poke).to.have.length(1)
    })

    it('should emit an event', function () {
        e.on('poke', f)
        expect(ting).to.be.false
        e.emit('poke')
        expect(ting).to.be.true
    })

    it('should ignore emitting an event with no handlers', function () {
        e.emit('poke')
        expect(ting).to.be.false
    })

    it('should provide arguments when emitting an event', function () {
        e.on('poke', f)
        expect(ting).to.be.false
        e.emit('poke', 'mushroom')
        expect(ting).to.equal('mushroom')
    })

    it('should remove an event', function () {
        e.on('poke', f)
        expect(e.events.poke).to.have.length(1)
        e.off('poke', f)
        expect(e.events.poke).to.be.empty
    })

    it('should remove all events', function () {
        e.on('poke', f)
        expect(e.events).to.not.be.empty
        e.off()
        expect(e.events).to.be.empty
    })

    it('should remove all events of a given type', function () {
        e.on('poke', f)
        e.on('sway', f)
        e.off('poke')
        expect(e.events.poke).to.be.empty
        expect(e.events.sway).to.have.length(1)
    })
})
