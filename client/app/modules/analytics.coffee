ga = (window.ga ?= ->
    (window.ga.q ?= []).push(arguments))

startGoogleAnalytics = ->
    window.GoogleAnalyticsObject = 'ga'
    window.ga.l = 1 * new Date()
    a = document.createElement('script')
    a.async = 1
    a.src = '//www.google-analytics.com/analytics.js'
    m = document.getElementsByTagName('script')[0]
    m.parentNode.insertBefore(a, m) if m
    document.body.appendChild(a) unless m

    ga('create', 'UA-40497674-1', 'auto')
    ga('send', 'pageview')

trackEvent = (name, args...) ->
    if name is 'route'
        ga('send', {
            hitType: 'pageview'
            page: args[0]
        })
        ga('set', {
            page: args[0]
        })
    else
        ga('send', {
            hitType: 'event'
            eventCategory: 'Sagefy'
            eventAction: name
            eventLabel: JSON.stringify(args)
        })

module.exports = {startGoogleAnalytics, trackEvent}
