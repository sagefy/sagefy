const { div } = require('../../modules/tags')
const {
    previewCommon,
    previewRequires,
    previewTags,
} = require('./preview_shared.fn')

// TODO-2 show diff option

module.exports = function previewUnitContent({
    status,
    available,
    created,
    language,
    requires,
    tags,
}) {
    return div(
        { className: 'preview--unit__content' },
        previewCommon({ created, status, available, language }),
        previewRequires(requires),
        previewTags(tags)
    )
}
