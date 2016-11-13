// TODO-2 try to load the state from local storage.
// BUT if there's no cookie, then act like local storage isn't there.
// Also, state changes `change` should update the data in local storage as well.

const recorder = require('./recorder')

const store = {
    data: window.preload || {},

    bind: function bind(fn) {
        store.callback = fn
        return fn
    },

    change: function change() {
        if (store.callback) {
            return store.callback(store.data)
        }
    },

    update: function update(key, reducer, action) {
        store.data[key] = reducer(store.data[key], action)
        if (action.message) {
            recorder.emit(action.message)
        }
        store.change()
    }
}

module.exports = store
