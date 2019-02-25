const fs = require('fs')
const request = require('../request')

const gql = {
  rootNewUser: fs.readFileSync(
    '../shared/graphql/root-new-user.graphql',
    'utf8'
  ),
}

const UUID_REGEXP = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

describe('New User', () => {
  it('should sign up a new users', async () => {
    const response = await request(
      JSON.stringify({
        query: gql.rootNewUser,
        variables: {
          name: 'hilda',
          email: 'hilda@example.com',
          password: 'hilda123',
        },
      })
    )
    expect(response.data.signUp.user.id).toMatch(UUID_REGEXP)
  })

  it.skip('should error if name not unique', () => {
    expect(true).toBe(false)
  })

  it.skip('should trim name', () => {
    expect(true).toBe(false)
  })

  it.skip('should error if email not unique', () => {
    expect(true).toBe(false)
  })

  it.skip('should trim email', () => {
    expect(true).toBe(false)
  })

  it.skip('should require passwords >8 char', () => {
    expect(true).toBe(false)
  })

  it.skip('should encrypt the password', () => {
    expect(true).toBe(false)
  })

  it.skip('should notify the email address', () => {
    expect(true).toBe(false)
  })

  it.skip('should only be available to anonymous users', () => {
    expect(true).toBe(false)
  })
})
