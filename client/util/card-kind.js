const CARD_KIND = {
  CHOICE: {
    name: 'Choice',
    icon: 'choice',
    url: 'choice',
    page: 'Choice',
  },
  VIDEO: {
    name: 'Video',
    icon: 'video',
    url: 'video',
    page: 'Video',
  },
  PAGE: {
    name: 'Page',
    icon: 'page',
    url: 'page',
    page: 'Page',
  },
  UNSCORED_EMBED: {
    name: 'Embed',
    icon: 'embed',
    url: 'unscored-embed',
    page: 'UnscoredEmbed',
  },
}

CARD_KIND.choice = CARD_KIND.CHOICE
CARD_KIND.video = CARD_KIND.VIDEO
CARD_KIND.page = CARD_KIND.PAGE
CARD_KIND['unscored-embed'] = CARD_KIND.UNSCORED_EMBED

module.exports = CARD_KIND
