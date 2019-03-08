import FormErrorsField from './FormErrorsField'

describe('FormErrorsField component', () => {
  it('should render a FormErrorsField null', () => {
    expect(FormErrorsField({ formErrors: {}, field: 'all' })).toMatchSnapshot()
  })

  it('should render a FormErrorsField data', () => {
    expect(
      FormErrorsField({
        formErrors: {
          all: [{ message: 'Hello' }],
        },
        field: 'all',
      })
    ).toMatchSnapshot()
  })
})
