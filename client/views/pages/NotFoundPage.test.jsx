import NotFoundPage from './NotFoundPage'

describe('NotFoundPage', () => {
  it('should render the not found page', () => {
    expect(NotFoundPage()).toMatchSnapshot()
  })
})
