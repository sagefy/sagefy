import LearnPagePage from './LearnPagePage'

describe('LearnPagePage', () => {
  it('should render LearnPagePage', () => {
    expect(LearnPagePage({ card: { data: {} } })).toMatchSnapshot()
  })
})
