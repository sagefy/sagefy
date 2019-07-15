import HomePage from './HomePage'

describe('HomePage', () => {
  it('should render the home page', () => {
    expect(HomePage({ role: 'sg_anonymous' })).toMatchSnapshot()
  })

  it('should render the logged in home page', () => {
    expect(HomePage({ role: 'sg_user' })).toMatchSnapshot()
  })
})
