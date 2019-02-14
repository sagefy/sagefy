import Icon from './Icon'

describe('Icon component', () => {
  it('should render an icon', () => {
    expect(Icon({ i: 'home', s: 'xxl' })).toMatchSnapshot()
  })

  it('should render an icon with default size', () => {
    expect(Icon({ i: 'home' })).toMatchSnapshot()
  })
})
