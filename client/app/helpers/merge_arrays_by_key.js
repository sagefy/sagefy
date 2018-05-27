const compact = require('lodash.compact')

/* eslint-disable max-statements */
module.exports = function mergeArraysByKey(A, B, key = 'id') {
  let a = 0
  let b = 0
  const C = []

  A = compact(A)
  B = compact(B)

  while (a < A.length) {
    let b2 = b
    let found = false

    while (b2 < B.length) {
      if (A[a][key] === B[b2][key]) {
        while (b <= b2) {
          C.push(B[b])
          b += 1
        }
        found = true
        break
      }
      b2 += 1
    }

    if (!found) {
      C.push(A[a])
    }

    a += 1
  }

  while (b < B.length) {
    C.push(B[b])
    b += 1
  }

  return C
}
/* eslint-enable max-statements */
