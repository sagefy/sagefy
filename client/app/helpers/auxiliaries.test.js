const {
  mergeArraysByKey,
  parseFormValues,
} = require('../../app/helpers/auxiliaries')

describe('Auxiliaries', () => {
  it('should merge two arrays by a key', () => {
    const A = [{ k: 0, v: 1 }, { k: 1, v: 1 }, { k: 3, v: 1 }, { k: 7, v: 1 }]
    const B = [{ k: 1, v: 2 }, { k: 2, v: 2 }, { k: 7, v: 2 }, { k: 8, v: 2 }]

    expect(mergeArraysByKey(A, B, 'k')).toEqual([
      { k: 0, v: 1 },
      { k: 1, v: 2 },
      { k: 3, v: 1 },
      { k: 2, v: 2 },
      { k: 7, v: 2 },
      { k: 8, v: 2 },
    ])
  })

  it('should merge into an empty array', () => {
    const A = []
    const B = [{ k: 1, v: 2 }, { k: 2, v: 2 }, { k: 7, v: 2 }, { k: 8, v: 2 }]

    expect(mergeArraysByKey(A, B, 'k')).toEqual(B)
  })

  it('should merge an empty array', () => {
    const A = [{ k: 1, v: 2 }, { k: 2, v: 2 }, { k: 7, v: 2 }, { k: 8, v: 2 }]
    const B = []

    expect(mergeArraysByKey(A, B, 'k')).toEqual(A)
  })

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
