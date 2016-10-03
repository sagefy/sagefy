const Events = require('../../app/modules/events')

describe('Events', () => {
    beforeEach(() => {
        this.e = new Events()
        this.ting = false
        this.f = (a) => {
            this.ting = a || true
        }
        this.z = new Events()
    })

    after(() => {
        delete this.e
    })

    it('should register an event', () => {
        this.e.on('poke', this.f)
        expect(this.e.events.poke).to.be.an('array')
        expect(this.e.events.poke[0]).to.be.a('function')
    })

    it('should register only one binding per event', () => {
        this.e.on('poke', this.f)
        this.e.on('poke', this.f)
        expect(this.e.events.poke).to.have.length(1)
    })

    it('should emit an event', () => {
        this.e.on('poke', this.f)
        expect(this.ting).to.be.false
        this.e.emit('poke')
        expect(this.ting).to.be.true
    })

    it('should ignore emitting an event with no handlers', () => {
        this.e.emit('poke')
        expect(this.ting).to.be.false
    })

    it('should provide arguments when emitting an event', () => {
        this.e.on('poke', this.f)
        expect(this.ting).to.be.false
        this.e.emit('poke', 'mushroom')
        expect(this.ting).to.equal('mushroom')
    })

    it('should remove an event', () => {
        this.e.on('poke', this.f)
        expect(this.e.events.poke).to.have.length(1)
        this.e.off('poke', this.f)
        expect(this.e.events.poke).to.be.empty
    })

    it('should remove all events', () => {
        this.e.on('poke', this.f)
        expect(this.e.events).to.not.be.empty
        this.e.off()
        expect(this.e.events).to.be.empty
    })

    it('should remove all events of a given type', () => {
        this.e.on('poke', this.f)
        this.e.on('sway', this.f)
        this.e.off('poke')
        expect(this.e.events.poke).to.be.empty
        expect(this.e.events.sway).to.have.length(1)
    })
})
