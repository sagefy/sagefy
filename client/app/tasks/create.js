/* eslint-disable camelcase */
const {dispatch, getState} = require('../modules/store')
const tasks = require('../modules/tasks')
const {copy} = require('../modules/utilities')

module.exports = tasks.add({
    resetCreate() {
        dispatch({type: 'RESET_CREATE'})
    },

    updateCreateRoute({kind, step}) {
        dispatch({type: 'UPDATE_CREATE_ROUTE', kind, step})
    },

    createSubjectData(values) {
        dispatch({
            type: 'CREATE_SUBJECT_DATA',
            values,
        })
    },

    addMemberToCreateSubject({kind, id, name, body}) {
        dispatch({
            type: 'ADD_MEMBER_TO_CREATE_SUBJECT',
            kind,
            id,
            name,
            body,
        })
    },

    addMemberToAddUnits({id, name, body, language = 'en', require_ids = []}) {
        dispatch({
            type: 'ADD_MEMBER_TO_ADD_UNITS',
            id,
            name,
            body,
            language,
            require_ids,
        })
    },

    addMemberToAddCards(values) {
        dispatch({
            type: 'ADD_MEMBER_TO_ADD_CARDS',
            values,
        })
    },

    removeMemberFromCreateSubject({id}) {
        // TODO-2 switch to undo
        if(window.confirm('Remove member?')) {  // eslint-disable-line
            dispatch({
                type: 'REMOVE_MEMBER_FROM_CREATE_SUBJECT',
                id,
            })
        }
    },

    removeUnitFromSubject({index}) {
        // TODO-2 switch to undo
        if(window.confirm('Remove unit?')) {  // eslint-disable-line
            dispatch({
                type: 'REMOVE_UNIT_FROM_SUBJECT',
                index,
            })
        }
    },

    removeCardFromUnit({index}) {
        // TODO-2 switch to undo
        if(window.confirm('Remove card?')) {  // eslint-disable-line
            dispatch({
                type: 'REMOVE_CARD_FROM_UNIT',
                index,
            })
        }
    },

    createChooseSubjectForUnits({id, name}) {
        dispatch({
            type: 'CREATE_CHOOSE_SUBJECT_FOR_UNITS',
            id,
            name,
        })
    },

    createChooseUnitForCards({id, name}) {
        dispatch({
            type: 'CREATE_CHOOSE_UNIT_FOR_CARDS',
            id,
            name,
        })
    },

    stowProposedUnit({name, language, body, require_ids}) {
        dispatch({
            type: 'STOW_PROPOSED_UNIT',
            name,
            language,
            body,
            require_ids,
        })
    },

    stowProposedCard(values) {
        dispatch({
            type: 'STOW_PROPOSED_CARD',
            values,
        })
    },

    addRequireToProposedUnit({id, name, body, kind}) {
        dispatch({
            type: 'ADD_REQUIRE_TO_PROPOSED_UNIT',
            id,
            name,
            body,
            kind
        })
    },

    createSubjectProposal(data) {
        let topicId
        tasks.createTopic({topic: data.topic})
            .then((topicResponse) => {
                topicId = topicResponse.topic.id
                return tasks.createNewSubjectVersion(data.subject)
            })
            .then((subjectResponse) => {
                const post = copy(data.post)
                post.topic_id = topicId
                post.entity_versions = [{
                    kind: 'subject',
                    id: subjectResponse.version.id
                }]
                return tasks.createPost({post})
            })
    },

    createUnitsProposal() {
        /* const state = getState()
        const {selectedSubject} = state.create
        const topic = {
            name: 'Add Units to This Subject',
            entity: {
                id: selectedSubject.id,
                kind: 'subject',
            },
        }

        let topicId
        return tasks.createTopic({topic})
            .then((topicResponse) => {
                topicId = topicResponse.topic.id
                const units = state.create.units.filter(unit => !unit.entity_id)
                return tasks.createNewUnitVersions(units)
            })
            .then((unitsResponse) => {
                const subject = {
                    entity_id: selectedSubject.id,
                    members: selectedSubject.units.map(unit => ({
                        kind: 'unit',
                        id: unit.entity_id /* or from unitsResponse /,
                    }))
                }
                return tasks.createExistingSubjectVersion(subject)
            })
            .then((subjectResponse) => {
                const post = {
                    kind: 'proposal',
                    body: 'Add Units to Subject',
                    topic_id: topicId,
                    entity_versions: [{
                        kind: 'subject',
                        id: subjectResponse.version.id
                    }, /* ...units /],
                }
                return tasks.createPost({post})
            }) */
    },

    createCardsProposal() {
        const state = getState()
        const {selectedUnit} = state.create
        const topic = {
            name: 'Add Cards to This Unit',
            entity: {
                id: selectedUnit.id,
                kind: 'unit',
            },
        }
        let topicId
        return tasks.createTopic({topic})
            .then((topicResponse) => {
                topicId = topicResponse.topic.id
                let {cards} = state.create
                cards = cards.map(card => Object.assign({}, card, {
                    unit_id: selectedUnit.id,
                }))
                return tasks.createNewCardVersions(cards)
            })
            .then((cardsResponse) => {
                const post = {
                    kind: 'proposal',
                    body: 'Add Cards to Unit',
                    topic_id: topicId,
                    entity_versions: cardsResponse.cards.map(card => ({
                        id: card.id,
                        kind: 'card',
                    })),
                }
                return tasks.createPost({post})
            })
    }
})
