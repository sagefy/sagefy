const { iframe } = require('../../modules/tags')

module.exports = data =>
    iframe({
        className: 'video',
        src: data.site === 'youtube' ?
             `https://www.youtube.com/embed/${data.video_id}` +
               '?autoplay=1&modestbranding=1&rel=0' :
             data.site === 'vimeo' ?
             `https://player.vimeo.com/video/${data.video_id}` :
             '',
        width: 672,
        height: 336,
        allowfullscreen: true,
    })
