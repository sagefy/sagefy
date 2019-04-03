import LearnChoicePage from './LearnChoicePage'

describe('LearnChoicePage', () => {
  it('should render LearnChoicePage', () => {
    expect(LearnChoicePage({ data: { options: {} } })).toMatchSnapshot()
  })
})
