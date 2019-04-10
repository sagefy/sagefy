import LogInPage from './LogInPage'

describe('LogInPage', () => {
  it('should render the LogInPage', () => {
    expect(LogInPage({ gqlErrors: {}, body: {}, query: {} })).toMatchSnapshot()
  })
})
