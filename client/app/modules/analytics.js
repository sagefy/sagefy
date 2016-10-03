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
    if (m) { m.parentNode.insertBefore(a, m) }
    if (!m) { document.body.appendChild(a) }

    ga('create', 'UA-40497674-1', 'auto')
    ga('send', 'pageview')
}

const trackEvent = (name, ...args) => {
    if (name === 'route') {
        ga('send', {
            hitType: 'pageview',
            page: args[0],
        })
        ga('set', {
            page: args[0]
        })
    } else {
        ga('send', {
            hitType: 'event',
            eventCategory: 'Sagefy',
            eventAction: name,
            eventLabel: JSON.stringify(args),
        })
    }
}

module.exports = {startGoogleAnalytics, trackEvent}
