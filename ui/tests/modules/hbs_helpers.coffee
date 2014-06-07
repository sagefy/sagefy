hbs = require('handlebars')
require('../../scripts/modules/hbs_helpers')(hbs)

describe('Handlebars Helpers', ->
    ###
    N.B.: In this file we will tests specifically
    that Handlebars has these capabilities.
    We will not test if the functions run independently. See `mixins`.
    ###

    before(->
        @render = (template, values) ->
            return hbs.compile(template)(values)
    )

    after(->
        @render = null
    )

    it('should add commas to a number', ->
        expect(@render('{{addCommas 1000}}')).to.equal('1,000')
    )

    it('should truncate numbers', ->
        expect(@render('{{toFixed num 1}}', {num: 0.444})).to.equal('0.4')
        expect(@render('{{toPrecision num 1}}', {num: 0.444})).to.equal('0.4')
    )

    it('should format dates and times', ->
        expect(@render('{{dateFormat date "L"}}', {date: new Date()}))
            .to.match(/\d{2}\/\d{2}\/\d{4}/)
    )

    it('should describe the time since an event', ->
        expect(@render('{{timeAgo date}}', {date: new Date()}))
            .to.equal('a few seconds ago')
    )

    it('should lowercase a string', ->
        expect(@render('{{lowercase "ABC"}}')).to.equal('abc')
    )

    it('should uppercase a string', ->
        expect(@render('{{uppercase "abc"}}')).to.equal('ABC')
    )

    it('should capitalize the first letter of a string', ->
        expect(@render('{{ucfirst "abc"}}')).to.equal('Abc')
    )

    it('should titlecase a string', ->
        expect(@render('{{titlecase "abc"}}')).to.equal('Abc')
    )

    it('should sentencecase a string', ->
        expect(@render('{{sentencecase "abc"}}')).to.equal('Abc')
    )

    it('should truncate a string', ->
        expect(@render('{{truncate "abcdefg" 6 "..."}}')).to.equal('abc...')
    )

    it('should parse markdown within HTML', ->
        expect(@render('{{#markdown}}**bold**{{/markdown}}'))
            .to.equal('<p><strong>bold</strong></p>\n')
    )

    it('should do something on any array element being true', ->
        expect(@render('{{#any arr}}a{{else}}b{{/any}}', {arr: []}))
            .to.equal('b')
        expect(@render('{{#any arr}}a{{/any}}', {arr: [true]}))
            .to.equal('a')
    )

    it('should get elements on the right side of an array', ->
        expect(@render('{{after arr 1}}', {arr: [1, 2, 3]}))
            .to.equal('2,3')
    )

    it('should do something with elements on the right side of an array', ->
        tmpl = '{{#withAfter arr 1}}{{this}}{{/withAfter}}'
        expect(@render(tmpl, {arr: [1, 2, 3]}))
            .to.eql('23')
    )

    it('should get elements on the left side of an array', ->
        expect(@render('{{before arr 1}}', {arr: [1, 2, 3]}))
            .to.equal('1,2')
    )

    it('should do something with elements on the left side of an array', ->
        tmpl = '{{#withBefore arr 1}}{{this}}{{/withBefore}}'
        expect(@render(tmpl, {arr: [1, 2, 3]}))
            .to.equal('12')
    )

    it('should get the first element of an array', ->
        expect(@render('{{first arr}}', {arr: [1, 2, 3]}))
            .to.equal('1')
    )

    it('should do something with the first element of an array', ->
        tmpl = '{{#withFirst arr}}{{this}}{{/withFirst}}'
        expect(@render(tmpl, {arr: [1, 2, 3]}))
            .to.eql('1')
    )

    it('should get the last element of an array', ->
        expect(@render('{{last arr}}', {arr: [1, 2, 3]}))
            .to.equal('3')
    )

    it('should do something with the last element of an array', ->
        tmpl = '{{#withLast arr}}{{this}}{{/withLast}}'
        expect(@render(tmpl, {arr: [1, 2, 3]}))
            .to.eql('3')
    )

    it('should join an array into a string', ->
        expect(@render('{{join arr " "}}', {arr: [1, 2, 3]}))
            .to.equal('1 2 3')
    )

    it('should join an array into a sentence string', ->
        expect(@render('{{joinSentence arr ", and "}}', {arr: [1, 2, 3]}))
            .to.equal('1, 2, and 3')
    )

    it('should compute the array length', ->
        expect(@render('{{length arr}}', {arr: [1, 2, 3]}))
            .to.equal('3')
    )

    it('should do something if an array is empty', ->
        expect(@render('{{#empty arr}}true{{/empty}}', {arr: []}))
            .to.equal('true')
    )

    it('should do something if an array contains a specified element', ->
        expect(
            @render('{{#contains arr 1}}true{{/contains}}', {arr: [1, 2, 3]})
        )
            .to.equal('true')
    )

    it('should iterate over an array and provide indexes', ->
        tmpl = '{{#eachIndex arr}}{{index}}{{item}}{{/eachIndex}}'
        expect(@render(tmpl, {arr: ['a', 'b', 'c']}))
            .to.equal('0a1b2c')
    )

    it('should do something if two values are both true', ->
        expect(@render('{{#and true true}}true{{/and}}'))
            .to.equal('true')
    )

    it('should do something if either of two values are true', ->
        expect(@render('{{#or true false}}true{{/or}}'))
            .to.equal('true')
    )

    it('should do something if two values are equal', ->
        expect(@render('{{#is true true}}true{{/is}}'))
            .to.equal('true')
    )

    it('should do something if two values are not equal', ->
        expect(@render('{{#isnt true false}}true{{/isnt}}'))
            .to.equal('true')
    )

    it('should do something if one value is greater than another', ->
        expect(@render('{{#gt 2 1}}true{{/gt}}'))
            .to.equal('true')
    )

    it('should do something if one value is less than another', ->
        expect(@render('{{#lt 1 2}}true{{/lt}}'))
            .to.equal('true')
    )
)
