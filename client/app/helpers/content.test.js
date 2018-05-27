const content = require('../../app/helpers/content')

describe('Content', () => {
  it('should get content', () => {
    expect(content.get('required')).toEqual('Required.')
    expect(content.get('required', 'eo')).toEqual('Postulo.')
  })
})
