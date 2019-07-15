import EmailPage from './EmailPage'

describe('EmailPage', () => {
  it('should render the EmailPage 0', () => {
    expect(EmailPage({ gqlErrors: {}, state: 0 })).toMatchSnapshot()
  })

  it('should render the EmailPage 1', () => {
    expect(EmailPage({ gqlErrors: {}, state: 1 })).toMatchSnapshot()
  })

  it('should render the EmailPage 2', () => {
    expect(EmailPage({ gqlErrors: {}, state: 2 })).toMatchSnapshot()
  })
})
