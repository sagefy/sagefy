import SettingsPage from './SettingsPage'

describe('SettingsPage', () => {
  it('should render the SettingsPage', () => {
    expect(SettingsPage({ gqlErrors: {}, prevValues: {} })).toMatchSnapshot()
  })
})
