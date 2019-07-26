import ChooseStepPage from './ChooseStepPage'

describe('ChooseStepPage', () => {
  it('should render ChooseStepPage', () => {
    expect(ChooseStepPage({ subject: {} })).toMatchSnapshot()
  })
})
