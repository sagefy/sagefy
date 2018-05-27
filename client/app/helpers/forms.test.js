const { parseFormValues } = require('../../app/helpers/forms')

describe('form', () => {
  it('should parse form values into service friendly data', () => {
    const values = {
      a: 1,
      'b.a': 2,
      'b.b.a': 3,
      'c.0': 4,
      'c.1': 5,
      'd.0.a': 6,
      'd.0.b': 7,
      'd.1.a': 8,
      'd.1.b': 9,
    }

    expect(parseFormValues(values)).toEqual({
      a: 1,
      b: {
        a: 2,
        b: {
          a: 3,
        },
      },
      c: [4, 5],
      d: [{ a: 6, b: 7 }, { a: 8, b: 9 }],
    })
  })
})
