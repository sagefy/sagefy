import FormErrorsTop from './FormErrorsTop'

describe('FormErrorsTop component', () => {
  it('should render a FormErrorsTop null', () => {
    expect(FormErrorsTop({ formErrors: {} })).toMatchSnapshot()
  })

  it('should render a FormErrorsTop data', () => {
    expect(
      FormErrorsTop({
        formErrors: {
          all: [{ message: 'Hello' }],
        },
      })
    ).toMatchSnapshot()
  })
})
