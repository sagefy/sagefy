const { render } = require('ultradom')
const format = require('./format')
const { div } = require('./tags')

const singleLineExample = 'This is some really great text.'
const paragraphExample = `
This is some really great text.

And some more even really great text.

Finally, the last of it.
`
const paragraphHtml =
  '<div><p>This is some really great text.</p><p>And some more even really great text.</p><p>Finally, the last of it.</p></div>'
const headingExample = `
# I love _headings_

Hooray!

Great text.
`
const headingHtml =
  '<div><h1>I love <em>headings</em></h1><p>Hooray!</p><p>Great text.</p></div>'
const inlineExample = 'I _love_ **examples**.'
const inlineHtml = '<div>I <em>love</em> <strong>examples</strong>.</div>'
const imageExample = 'I love ![An Image](https://example.com/.img) images.'
const imageHtml =
  '<div>I love <img src="https://example.com/.img" title="An Image"> images.</div>'

expect.extend({
  toMatchDOM(node, html) {
    document.body.innerHTML = ''
    render(node, document.body)
    expect(document.body.innerHTML).toBe(html.replace(/\s{2,}/g, ''))
    return { pass: true }
  },
})

describe('format', () => {
  it('should not paragraph a single line of text', () => {
    expect(format(singleLineExample)).toMatchDOM(singleLineExample)
  })

  it('should format paragraphs', () => {
    expect(div(format(paragraphExample))).toMatchDOM(paragraphHtml)
  })

  it('should format a heading', () => {
    expect(div(format(headingExample))).toMatchDOM(headingHtml)
  })

  it('should format inliners', () => {
    expect(div(format(inlineExample))).toMatchDOM(inlineHtml)
  })

  it('should format inline images', () => {
    expect(div(format(imageExample))).toMatchDOM(imageHtml)
  })
})
