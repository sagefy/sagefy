import Index, { output } from './Index'

describe('Index view', () => {
  it('should render a page', () => {
    expect(Index({ location: '/', cacheHash: '_' })).toMatchSnapshot()
  })

  it('should be a function that returns a string', () => {
    expect(output('a')()).toEqual('a')
  })
})
