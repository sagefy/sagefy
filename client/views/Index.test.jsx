import Index from './Index'

describe('Index view', () => {
  it('should render a page', () => {
    expect(Index({ location: '/' })).toMatchSnapshot()
  })
})
