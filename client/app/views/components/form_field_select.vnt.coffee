broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{debounce} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'click .select .clear': (e, el) ->
        e.preventDefault()
        # TODO-3 clear options

    # 'change input[type="search"]': debounce((e, el) ->
        # TODO-3 search options
    # , 200)

    'change input[type="radio"], input[type="checkbox"]': (e, el) ->
        # TODO-3 update .select__selected to show list of selected names
})
