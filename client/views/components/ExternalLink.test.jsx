import React from 'react'
import ExternalLink from './ExternalLink'

describe('ExternalLink component', () => {
  it('should render an external link', () => {
    expect(
      ExternalLink({
        href: 'https://example.com',
        children: <span>Hello!</span>,
      })
    ).toMatchSnapshot()
  })
})
