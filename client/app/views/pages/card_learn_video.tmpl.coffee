{div, iframe} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div(
        {className: 'card-learn-video'}
        iframe(
            {
                src: if site is 'youtube' \
                     then "https://www.youtube.com/embed/#{data.video_id}" \
                     else if site is 'vimeo' \
                     then "https://player.vimeo.com/video/#{data.video_id}"
                width: 560
                height: 325
                allowfullscreen: true
            }
        )
    )
