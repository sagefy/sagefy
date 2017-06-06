module.exports = function cards(state = {}, action = { type: '' }) {
    if(action.type === 'GET_CARD_SUCCESS') {
        const card = action.card
        ;['topics', 'versions', 'card_parameters'].forEach((r) => {
            card[r] = action[r]
        })
        card.relationships = [{
            kind: 'belongs_to',
            entity: action.unit,
        }]
        ;['requires', 'required_by'].forEach(r =>
            action[r].forEach(e =>
                card.relationships.push({
                    kind: r,
                    entity: e,
                })
            )
        )
        state[action.id] = card
        return state
    }
    if(action.type === 'LIST_POSTS_SUCCESS' && action.entity === 'card') {
        state[action.card.entity_id] = action.card
        return state
    }
    return state
}
