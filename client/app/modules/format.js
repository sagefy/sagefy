/*
Phase 1:
- [√] Block: Paragraphs
- [√] Block: Heading 1
- [√] Inline: Emphasis: Italic, Bold
- [√] Inline: Inline Images
Remaining:
- [ ] Inline: Strikethrough
- [ ] Inline: Monospace
- [ ] Block: Horizontal Rule
- [ ] Block: Heading 2 & 3
- [ ] Block: Unordered and ordered lists, nesting
- [ ] Inline: Links: inline, ref
- [ ] Inline: Ref images
- [ ] Inline: Footnotes
- [ ] Block: iFrames
- [ ] Block: Code blocks ```
- [ ] Block: Blockquote
- [ ] Block: Tables
Later:
- [ ] Block: Syntax highlighting?
- [ ] Inline: Emoji?
- [ ] Inline: Inline TeX?
- [ ] Inline: Super/sub? Small? Quotes? Date/times?
- [ ] Inline: Image description?
*/
const { h1, h2, p, img, em, strong } = require('./tags')

const headings = [h1, h2]

const INLINE_RE = /(_)|(\*\*)|(!\[.*\]\(.*\))/g
const INLINE_IMAGE_RE = /!\[(.*)\]\((.*)\)/  // dont use `g` flag with exec!

function inline(s) {
    const startIndex = s.search(INLINE_RE)
    if (startIndex === -1) { return s }
    if (s[startIndex] === '_') {
        const endIndex = startIndex + 1 + s.substring(startIndex + 1).indexOf('_')
        return [
            s.substring(0, startIndex),
            em(s.substring(startIndex + 1, endIndex)),
            inline(s.substring(endIndex + 1)),
        ]
    }
    if (s[startIndex] === '*') {
        const endIndex = startIndex + 2 + s.substring(startIndex + 2).indexOf('**')
        return [
            s.substring(0, startIndex),
            strong(s.substring(startIndex + 2, endIndex)),
            inline(s.substring(endIndex + 2)),
        ]
    }
    if (s[startIndex] === '!') {
        const endIndex = startIndex + s.substring(startIndex).indexOf(')')
        console.log('###', s)
        console.log('s', startIndex)
        console.log('e', endIndex)
        const match = INLINE_IMAGE_RE.exec(s)
        console.log('m', match)
        if (!match) {
            return [
                s.substring(0, endIndex),
                inline(s.substring(endIndex + 1)),
            ]
        }
        const title = match[1]
        const src = match[2]
        return [
            s.substring(0, startIndex),
            img({ src, title }),
            inline(s.substring(endIndex + 1)),
        ]
    }
}

function block(s, config = {}) {
    if (s[0] === '#') {
        const highestHeading = config.highestHeading - 1 || 0
        return headings[highestHeading](inline(s.substring(1).trimLeft()))
    }
    return p(inline(s))
}

module.exports = function format(full, config = {}) {
    full = full.trim()
    if (full.indexOf('\n') === -1) { return inline(full, config) }
    return full.split('\n\n').map(s => block(s, config))
}
