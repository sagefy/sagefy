const ga = window.ga = window.ga || (() => {
    window.ga.q = window.ga.q || []
    window.ga.q.push(arguments)
})

const startGoogleAnalytics = () => {
    window.GoogleAnalyticsObject = 'ga'
    window.ga.l = 1 * new Date()
    const a = document.createElement('script')
    a.async = 1
    a.src = '//www.google-analytics.com/analytics.js'
    const m = document.getElementsByTagName('script')[0]
    if (m) {
        m.parentNode.insertBefore(a, m)
    }
    if (!m) {
        document.body.appendChild(a)
    }

    ga('create', 'UA-40497674-1', 'auto')
    ga('send', 'pageview')
}

const trackEvent = (action) => {
    if (action.type === 'SET_ROUTE') {
        ga('send', {
            hitType: 'pageview',
            page: action.route,
        })
        ga('set', {
            page: action.route
        })
    } else {
        ga('send', {
            hitType: 'event',
            eventCategory: 'Sagefy',
            eventAction: action.type,
            eventLabel: JSON.stringify(action),
        })
    }
}

module.exports = {startGoogleAnalytics, trackEvent}
