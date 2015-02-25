from models.cards.slideshow_card import SlideshowCard


def test_slideshow_site(app, cards_table):
    """
    Expect a slideshow card to require a site.
    """

    card, errors = SlideshowCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'slideshow_id': 'JKLfjkld950',
    })
    assert len(errors) == 1
    card, errors = card.update({'site': 'slideshare'})
    assert len(errors) == 0


def test_slideshow_id(app, cards_table):
    """
    Expect a slideshow card to require a slideshow_id.
    """

    card, errors = SlideshowCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'site': 'slideshare',
    })
    assert len(errors) == 1
    card, errors = card.update({'slideshow_id': 'JofO48J'})
    assert len(errors) == 0
