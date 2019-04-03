import SearchSubjectsPage from './SearchSubjectsPage'

describe('SearchSubjectsPage', () => {
  it('should render the search subjects page', () => {
    expect(SearchSubjectsPage({ query: {} })).toMatchSnapshot()
  })
})
