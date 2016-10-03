const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')
const {closest} = require('../../modules/utilities')

module.exports = broker.add({
    'click #search [type="submit"]': (e, el) =>{
        if(e) {e.preventDefault()}
        const form = closest(el, 'form')
        const input = form.querySelector('input')
        tasks.search({q: input.value})
    },

    'click .add-to-my-sets': (e, el) => {
        if(e) {e.preventDefault()}
        tasks.addUserSet(el.id)
    },

    // TEMPORARY
    'click .add-intro-ele-music': (e) => {
        if(e) {e.preventDefault()}
        const entityID = 'CgDRJPfzJuTR916HdmosA3A8'
        tasks.addUserSet(entityID)
    }
    // TEMPORARY
})
