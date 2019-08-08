import React from 'react'
import { arrayOf, shape, string } from 'prop-types'
import Icon from './Icon'

export default function Menu({ items, current }) {
  return (
    <small className="Menu ta-r">
      <ul className="ls-i">
        {items.map(({ href, icon, name, ...props }) => (
          <li key={`Menu-items-${name}`}>
            {current === name ? (
              <span {...props}>
                <Icon i={icon} s="s" /> {name}
              </span>
            ) : (
              <a href={href} {...props}>
                <Icon i={icon} s="s" /> {name}
              </a>
            )}
          </li>
        ))}
      </ul>
    </small>
  )
}

Menu.propTypes = {
  items: arrayOf(
    shape({
      href: string.isRequired,
      icon: string.isRequired,
      name: string.isRequired,
    })
  ).isRequired,
  current: string,
}

Menu.defaultProps = {
  current: '',
}
