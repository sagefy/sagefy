import LearnVideoPage from './LearnVideoPage'

describe('LearnVideoPage', () => {
  it('should render LearnVideoPage', () => {
    expect(LearnVideoPage({ card: { data: {} } })).toMatchSnapshot()
  })
})
