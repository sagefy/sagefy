import TermsPage from './TermsPage'

describe('TermsPage', () => {
  it('should render the terms page', () => {
    expect(TermsPage()).toMatchSnapshot()
  })
})
