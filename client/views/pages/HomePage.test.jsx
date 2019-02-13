import HomePage from './HomePage'

describe('HomePage', () => {
  it('should render the home page', () => {
    expect(HomePage()).toMatchSnapshot()
  })
})
