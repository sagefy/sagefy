import LearnPagePage from './LearnPagePage'

describe('LearnPagePage', () => {
  it('should render LearnPagePage', () => {
    expect(LearnPagePage({})).toMatchSnapshot()
  })
})
