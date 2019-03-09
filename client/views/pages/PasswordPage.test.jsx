import PasswordPage from './PasswordPage'

describe('PasswordPage', () => {
  it('should render the PasswordPage 0', () => {
    expect(PasswordPage({ gqlErrors: {}, state: 0 })).toMatchSnapshot()
  })

  it('should render the PasswordPage 1', () => {
    expect(PasswordPage({ gqlErrors: {}, state: 1 })).toMatchSnapshot()
  })

  it('should render the PasswordPage 2', () => {
    expect(PasswordPage({ gqlErrors: {}, state: 2 })).toMatchSnapshot()
  })
})
