import DashboardPage from './DashboardPage'

describe('DashboardPage', () => {
  it('should render the dashboard page', () => {
    expect(DashboardPage()).toMatchSnapshot()
  })
})
