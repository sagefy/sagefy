from models.cards.video_card import VideoCard


def test_site(app, cards_table):
    """
    Expect a video card to require a site.
    """

    card, errors = VideoCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'video_id': 'Ajklfjl4',
    })
    assert len(errors) == 1
    card, errors = card.update({'site': 'youtube'})
    assert len(errors) == 0


def test_video_id(app, cards_table):
    """
    Expect a video card to require a video_id.
    """

    card, errors = VideoCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'site': 'youtube'
    })
    assert len(errors) == 1
    card, errors = card.update({'video_id': 'JFKl94jl'})
    assert len(errors) == 0
