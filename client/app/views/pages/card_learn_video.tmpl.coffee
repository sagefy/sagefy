{div, iframe} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return [
        iframe(
            {
                className: 'video'
                src: if data.site is 'youtube' \
                     then "https://www.youtube.com/embed/#{data.video_id}" \
                     else if data.site is 'vimeo' \
                     then "https://player.vimeo.com/video/#{data.video_id}"
                width: 672
                height: 336
                allowfullscreen: true
            }
        )
    ]
