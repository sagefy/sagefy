const { iframe } = require('../../modules/tags')

module.exports = data =>
    iframe({
        className: 'video',
        src:
            data.data.site === 'youtube'
                ? `https://www.youtube.com/embed/${data.data.video_id}` +
                  '?autoplay=1&modestbranding=1&rel=0'
                : data.data.site === 'vimeo'
                  ? `https://player.vimeo.com/video/${data.data.video_id}`
                  : '',
        width: 672,
        height: 336,
        allowfullscreen: true,
    })
