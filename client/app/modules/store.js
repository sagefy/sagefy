// TODO-2 try to load the state from local storage.
// BUT if there's no cookie, then act like local storage isn't there.
// Also, state changes `change` should update the data in local storage as well.

const store = {
    data: window.preload || {},
    tasks: {},

    init: function (fn) {
        fn.call(store)
    },

    add: function (obj) {
        Object.keys(obj).forEach(key => {
            const fn = obj[key]
            store.tasks[key] = fn.bind(store)
        })
        return obj
    },

    bind: function (fn) {
        return store.callback = fn
    },

    change: function () {
        if (store.callback) {
            return store.callback(store.data)
        }
    }
}

module.exports = store
