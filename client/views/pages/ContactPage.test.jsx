import ContactPage from './ContactPage'

describe('ContactPage', () => {
  it('should render the contact page', () => {
    expect(ContactPage()).toMatchSnapshot()
  })
})
