import ServerErrorPage from './ServerErrorPage'

describe('ServerErrorPage', () => {
  it('should render the ServerErrorPage', () => {
    expect(ServerErrorPage()).toMatchSnapshot()
  })
})
