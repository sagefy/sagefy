module.exports = (store, broker) => {
  broker.add({
    'click .select .clear'(e) {
      e.preventDefault()
      // TODO-3 clear options
    },

    // 'change input[type="radio"], input[type="checkbox"]': (e, el) =>
    // TODO-3 update .select__selected to show list of selected names
  })
}
