const { mergeArraysByKey } = require('../../app/helpers/auxiliaries')

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
})
