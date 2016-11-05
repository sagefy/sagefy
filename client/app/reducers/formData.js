module.exports = function formData(state = {}, action = {type: ''}) {
    if(action.type === 'RESET_FORM_DATA') {
        return {}
    }
    if(action.type === 'SET_FORM_DATA') {
        return action.data
    }
    if(action.type === 'ADD_LIST_FIELD_ROW') {
        let maxIndex = -1
        const {name, columns} = action
        Object.keys(state).forEach(key => {
            if (key.indexOf(name) === 0) {
                key = key.replace(`${name}.`, '')
                const index = parseInt(key.match(/^\d+/))
                if (index > maxIndex) { maxIndex = index }
            }
        })
        const newIndex = maxIndex + 1
        const newState = {}
        columns.forEach(column => {
            newState[`${name}.${newIndex}.${column}`] = ''
        })
        return newState
    }
    if(action.type === 'REMOVE_LIST_FIELD_ROW') {
        const {name, index} = action
        const parseKey = (key) => {
            const matches = key.match(/^(.*)\.(\d+)\.(.*)$/)
            if (matches) {
                const [, pre, rowIndex, col] = matches
                return [pre, rowIndex, col]
            }
        }

        const getKeyIndex = (key) => {
            key = parseKey(key)
            if(key) { key = key[1] }
            return parseInt(key)
        }

        const newState = {}
        Object.keys(state)
            .filter((key) => key.indexOf(name) === 0)
            .sort((keyA, keyB) => getKeyIndex(keyA) - getKeyIndex(keyB))
            .forEach((key) => {
                const rowIndex = getKeyIndex(key)
                if (rowIndex > index) {
                    const [pre, , col] = parseKey(key)
                    newState[`${pre}.${rowIndex - 1}.${col}`] =
                        state[key]
                }
                if (rowIndex >= index) {
                    delete newState[key]
                }
            })
        return newState
    }
    return state
}
