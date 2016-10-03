// TODO-3 move copy to content directory
const {div, h1, h2, p} = require('../../modules/tags')
const terms = require('./terms.txt')

module.exports = () =>
    div(
        {id: 'terms'},
        h1('Sagefy Privacy Policy & Terms of Service'),
        terms.split('\n\n').map((t) => {
            if (t.indexOf('##') > -1) {
                return h2(t.replace('##', ''))
            }
            return p(t)
        })
    )
